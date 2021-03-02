#!/usr/bin/env python3
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import TextIO

import click
import json5
from pymavlink import mavutil
from tqdm import tqdm

from .data_types import Backup
from .data_types import Parameter


DEBUG = False


def debug(message: str) -> None:
    """Print a message if DEBUG is True."""
    if DEBUG:
        click.echo(message)


def load_backup_from_file(backup_file: TextIO) -> Backup:
    """Load a list of parameters from a file."""
    data = json5.load(backup_file)
    return Backup.from_dict(data)


def save_backup_to_file(backup: Backup, outfile: TextIO) -> None:
    """Save a list of parameters to a file."""
    # Brace yourselves, we're going to perform some horrible hacks to
    # format the file for readability.

    # Write the status comment.
    outfile.write(backup.status_str)

    backup_dict = backup.as_dict()

    # Pop the parameters from the backup dict so we can write them later.
    parameters = backup_dict.pop("parameters")
    backup_dict["parameters"] = {}

    # Write the top-level backup.
    backup_str = json5.dumps(backup_dict, indent=2)

    param_str = "".join(
        (
            "    " + json5.dumps({name: data})[1:-1] + ",\n"
            for name, data in parameters.items()
        )
    )

    # Insert the param_str into the rest of the file and write it.
    outfile.write(backup_str[:-4] + "\n" + param_str + "  " + backup_str[-4:])


def read_backup_from_craft(socket: str) -> Backup:
    """Read all the parameters from a craft."""
    # From https://www.ardusub.com/developers/pymavlink.html.
    master = mavutil.mavlink_connection(socket)
    master.wait_heartbeat()
    master.mav.param_request_list_send(master.target_system, master.target_component, 1)
    backup = Backup()
    pbar = tqdm(total=1, dynamic_ncols=True, disable=DEBUG)
    while True:
        # Read all messages, as AP eventually freezes if we try to
        # ignore too many message types.
        message = master.recv_match(blocking=True).to_dict()
        debug(message)

        # We don't want any status messages received after parameters have started coming in.
        if message.get("mavpackettype", "") == "STATUSTEXT" and not backup.parameters:
            backup.status.append(message["text"])
        elif message.get("mavpackettype", "") == "PARAM_VALUE":
            name, value, type, count, index = (
                message["param_id"],
                message["param_value"],
                message["param_type"],
                message["param_count"],
                message["param_index"],
            )
            pbar.total = count
            pbar.update(1)
            backup.parameters[name] = Parameter(value, index, type)
            if index == count - 1:
                break
    pbar.close()
    return backup


@click.group()
@click.option("--debug", is_flag=True, help="Print debug information.")
def cli(debug):
    global DEBUG
    DEBUG = debug


@cli.command(help="Back up all the parameters from a craft to a file.")
@click.argument("craft_name")
@click.option(
    "-s",
    "--socket",
    default="/dev/ttyACM0",
    show_default=True,
    help="Path to the USB socket.",
)
@click.option(
    "-o",
    "--outdir",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="Directory to write the backup file to.",
)
def backup(craft_name, socket, outdir):
    click.echo(f"Reading parameters from {socket}...")
    backup = read_backup_from_craft(socket)
    click.echo("Writing to file...")
    filename = Path(outdir) / (
        f"{craft_name}_" f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}" ".chute"
    )
    # Write the actual backup.
    with filename.open("w") as outfile:
        save_backup_to_file(backup, outfile)
    click.echo("Done.")


@cli.command(help="Filter parameters by a regular expression.")
@click.argument("regex")
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def filter(regex, backup_file, output_file):
    click.echo("Filtering based on regular expression...")
    backup = load_backup_from_file(backup_file)
    try:
        backup.filter(regex)
    except re.error as e:
        sys.exit("Regex error: " + str(e))
    save_backup_to_file(backup, output_file)
    click.echo("Done.")


@cli.group(help="Convert a Parachute backup into another format.")
@click.option(
    "-f",
    "--filter",
    default="",
    help="Filter commands to process based on a regex.",
)
@click.pass_context
def convert(ctx, filter):
    ctx.ensure_object(dict)

    ctx.obj["FILTER"] = filter


@convert.command(help='Convert into a QGroundControl ".params" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def qgc(ctx, backup_file, output_file):
    click.echo("Converting to a QGroundControl compatible file...")
    backup = load_backup_from_file(backup_file)

    try:
        backup.filter(ctx.obj["FILTER"])
    except re.error as e:
        sys.exit("Regex error: " + str(e))

    output_file.write("# Vehicle-Id Component-Id Name Value Type\n")
    output_file.writelines(
        f"1\t1\t{name}\t{parameter.value:.18g}\t{parameter.type}\n"
        for name, parameter in sorted(backup.parameters.items())
    )


@convert.command(help='Convert into a Mission Planner ".param" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def mp(ctx, backup_file, output_file):
    click.echo("Converting to a Mission Planner compatible file...")
    backup = load_backup_from_file(backup_file)

    try:
        backup.filter(ctx.obj["FILTER"])
    except re.error as e:
        sys.exit("Regex error: " + str(e))

    output_file.writelines(
        f"{name},{parameter.value}\n"
        for name, parameter in sorted(backup.parameters.items())
    )


if __name__ == "__main__":
    cli()
