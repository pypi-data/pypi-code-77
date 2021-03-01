#!/usr/bin/env python3
# anonjail - Integrate Firejail sandboxing in the Linux desktop
# Copyright (C) 2015-2017 Rahiel Kasim (Shoutout to you mister Kasim :)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os.path
import getpass
import re
from difflib import get_close_matches
from shutil import which
import click
import platform
from subprocess import call
import sys

@click.version_option()
@click.group()
def cli():
    pass

def findStringInFile(file, stringtofind):
    """Check if a the specified file contains given string """
    if file is not None and os.path.exists(file):
        with open(file, "rb") as f: content = f.read()
        if re.search(stringtofind, content):
            return True
    return False         


def get_confd_apps():
    enabled = []
    disabled = []
    for p in installed:
        if findStringInFile(get_desktop(p), b"torjail") or findStringInFile(get_desktop(p), b"firejail"):
            enabled.append(p)
        else:
            disabled.append(p)
    for ap in applications:
        if findStringInFile(get_desktop(ap), b"torjail") or findStringInFile(get_desktop(ap), b"firejail"):
            enabled.append(ap)      
    return enabled, disabled

def get_config():
    """Get header and config."""
    header = "# list of enforced Firejail profiles\n"
    try:
        with open(config, "r") as f:
            conf = [l.strip() for l in f.readlines() if not l.startswith("#")]
    except FileNotFoundError:
        conf = []
    return header, conf

def write_config(programs, test, combine):
    """Write config to disk if necessary. Uses test to check if a program has to
    be added/removed from the config. Programs and conf are combined with combine.
    """
    header, conf = get_config()
    write = False
    for p in programs:
        if test(p, conf):
            write = True
            continue
    if write:
        lines = header + "\n".join(sorted(combine(programs, conf)))
        with open(config, "w") as f:
            f.writelines(lines)

def add_config(programs):
    """Add programs to config."""
    write_config(programs,
                 lambda program, conf: program not in conf,
                 lambda programs, conf: set(conf + programs))

def remove_config(programs):
    """Remove programs from config."""
    write_config(programs,
                 lambda program, conf: program in conf,
                 lambda programs, conf: set(conf) - set(programs))

def get_desktop(program):
    """Get path to program's desktop file."""
    path = os.path.join(application_path, program + ".desktop")
    if os.path.isfile(path):
        return path
    else:
        message = "Desktop file for %s does not exist." % program
        typo = get_close_matches(program, installed, n=1)
        if len(typo) > 0:
            message += "\n\nDid you mean %s?" % typo[0]

def replace(filename, condition, transform):
    """Replace lines in filename for which condition is true with transform."""
    newfile = []
    with open(filename, "rb") as f:
        for line in f:
            if condition(line):
                newfile.append(transform(line))
            else:
                newfile.append(line)

    with open(filename, "wb") as f:
        f.writelines([ele for ele in newfile])

def get_programs(program, all_programs=False):
    """Return list of programs to enable / disable."""
    if all_programs:
        program = installed

    if not os.access(get_desktop(installed[0]), os.W_OK):
        raise click.UsageError(
            message="Can't modify desktop files, please execute as root.")

    if len(program) == 0:
        raise click.ClickException("No program specified.")

    return list(program), [get_desktop(p) for p in program]

def symlink_enable(program):
    p = symlink_path + program
    if not os.path.exists(p):
        os.symlink(firejail, p)

def symlink_disable(program):
    p = symlink_path + program
    if os.path.exists(p):
        os.remove(p)

def switch_ExecState(filename, status=False):
    """Duplicate + comment the original Exec= line in the desktop file if status=True. Delete the custom Exec= line and uncomment the original one."""
    newfile = []  
    with open(filename, "rb") as f:
        for line in f:
            if line.startswith(b"Exec=") and status:
                newfile.append(line)
                newfile.append(b'#' + line)
            elif status:
                newfile.append(line)
            elif line.startswith(b"#Exec=") and not status:
                newfile.append(line[1:])
            elif not line.startswith(b"Exec=") and not status:
                newfile.append(line)
               
    with open(filename, "wb") as f:
        f.writelines([ele for ele in newfile])

def makeExec_cmd(program, torified):
    """Generate the Exec command going in the desktop file"""
    condition = lambda l: l.startswith(b"Exec=") and (b"firejail" or b"torjail" not in l)
    torified = b"Exec=/bin/sh -c 'sudo torjail -f $cmd'" if torified else b"Exec=/bin/sh -c 'firejail $cmd'"
    with open(program, "rb") as file:
        for line in file:
            if condition(line):
                if line.startswith(b"Exec=") and b'"' in line:
                    return (torified + b'\n').replace(b"$cmd", re.search(b'"(.*?)"', line).group(1))
                else:
                    return (torified + b'\n').replace(b"$cmd", line[line.find(b"=") + 1:-1]) 
    raise click.UsageError(
        message="Can't make a valid Exec command")


@cli.command(help="Enable anonjail for program")
@click.argument("program", type=click.STRING, nargs=-1)
@click.option("--all", "all_programs", is_flag=True, help="Enable Firejail for all supported programs.")
@click.option("--tor", "torify", is_flag=True, help="Enable Tor routing for the/all program(s)")
def enable(program, all_programs, torify=False, update_config=True):
    """Enable anonjail for program. Program is a sequence of program names."""
    programs, desktop_files = get_programs(program, all_programs)  # root access after this line
    os.makedirs("/usr/local/bin", mode=0o775, exist_ok=True)
    update_progs = []
    
    for p in programs:
        symlink_enable(p)

    for d,p in zip(desktop_files,programs):
        if not findStringInFile(d, b"#Exec="):
            symlink_enable(p)
            update_progs.append(p)
            cmd = makeExec_cmd(d, torify)
            switch_ExecState(d, True)
            replace(d, lambda l: l.startswith(b"Exec="), lambda l: cmd)
            if torify:
                replace(d, lambda l: l.startswith(b"Terminal="), lambda l: b"Terminal=true\n")
   
    if update_config:
        add_config(update_progs) 

@cli.command(help="disable anonjail for program")
@click.argument("program", type=click.STRING, nargs=-1)
@click.option("--all", "all_programs", is_flag=True, help="Disable Firejail for all programs.")
def disable(program, all_programs):
    """Disable Firejail for program. Program is a sequence of program names."""
    programs, desktop_files = get_programs(program, all_programs)  # root access after this line
    update_progs = []

    for p in programs:
        symlink_disable(p)

    for d,p in zip(desktop_files, programs):
        if findStringInFile(d, b"#Exec="):
            symlink_disable(p)
            update_progs.append(p)
            switch_ExecState(d, False)
            replace(d, lambda l: l.startswith(b"Terminal="), lambda l: b"Terminal=false\n")

    remove_config(update_progs)

@cli.command(help="show installed apps with no corresponding profile file")
def showapps():
    """Display availables apps started with the default Firejail profile."""
    enabled, disabled = get_confd_apps()
    availables = [app for app in applications if app not in (enabled + disabled)]
    click.echo("{:<2} Availables apps with no preconfigured Firejail profile (using default.profile)".format(len(availables)))
    for p in sorted(availables):
        click.echo("   %s" % p)


@cli.command(help="show status of Firejail profiles")
def status():
    """Display status of available Firejail profiles."""
    symlinks = []
    try:
        for p in os.scandir(symlink_path):
            if p.is_symlink() and os.path.realpath(p.path) == firejail:
                symlinks.append(p.name)
    except FileNotFoundError:
        pass

    enabled, disabled = get_confd_apps()
    header, conf = get_config()
    update_disabled = [p for p in conf if (p not in enabled or p not in symlinks)]
    disabled = [p for p in disabled if p not in update_disabled]

    try:
        longest_name = max(conf, key=len)
    except ValueError:
        longest_name = None     # when the list is empty

    def pad(s, l):
        """Right-pad s so it's the same length as l."""
        return s + " " * (len(l) - len(s))

    is_enabled = lambda p, l: pad("yes", "symlink") if p in l else click.style(pad("no", "symlink"), fg="red")
    padding = "    "

    click.echo("{:<2} Firejail profiles are enabled".format(len(enabled)))
    if conf:
        for p in sorted(conf):
            deskfile = get_desktop(p)
            click.secho("   " + pad("program", longest_name) + padding + "symlink"  + padding + "torified", bold=True)
            click.echo("   " + pad(p, longest_name) + padding + is_enabled(p, symlinks) + padding + 'Yes' if findStringInFile(deskfile, b"torjail") else 'No')
    print()

    click.echo("{:<2} Firejail profiles are disabled and availables".format(len(disabled)))
    for p in sorted(disabled):
        click.echo("   %s" % p)

    #Fix here
    if len(update_disabled) > 0:
        click.secho("\n{:<2} Firejail profiles are disabled by updates".format(len(update_disabled)), fg="red")
        for p in sorted(update_disabled):
            click.echo("   %s" % p)
        click.echo("Please run: " + click.style("sudo anonjail restore", bold=True))


@cli.command(help="restore Firejail profiles from config")
def restore():
    """Re-enable Firejail profiles for when desktop files get updated."""
    header, conf = get_config()
    removed = [c for c in conf if c not in installed]
    remove_config(removed)
    [conf.remove(c) for c in removed]

    for p in removed:
        symlink_disable(p)

    if len(conf) > 0:
        enable.callback(conf, all_programs=False, update_config=False)


@cli.command(help="install and config Anonjail dependencies")
def install():
    """Install and config Anonjail dependencies"""
    if os.path.exists("anonjail-install.bash"):
        call("anonjail-install.bash")
    else:
        raise FileNotFoundError

firejail = which("firejail")
torjail = which("torjail")

if not firejail or not torjail: #and cmd not install
    click.secho("Firejail and Torjail must be installed!", fg="red")
    answer = ""
    if os.geteuid() != 0:
        print("Be root mtf..")
        exit()
    while answer not in ["y", "n"]:
        answer = input("Wanna install and config deps [Y/N]? ").lower()
    if answer.lower() is 'n':
        raise click.UsageError(message="Please install Firejail and Torjail.. see the README or sudo anonjail install")
    else:
        install()

profile_path = "/etc/firejail/"
application_path = "/usr/share/applications/"
symlink_path = "/usr/local/bin/"
config = "/etc/firejail/anonjail.conf"

profiles = [os.path.splitext(file)[0]  for file in os.listdir(profile_path)]
applications = [os.path.splitext(f)[0] for f in os.listdir(application_path)]
installed = [app for profile in profiles for app in applications if profile == app]

if __name__ == "__main__":
    cli()