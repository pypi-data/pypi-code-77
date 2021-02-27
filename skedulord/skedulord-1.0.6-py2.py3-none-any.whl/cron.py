import typer
import subprocess
from clumper import Clumper
from crontab import CronTab


def clean_cron(user):
    cron = CronTab(user=user)
    cron.remove_all()
    cron.write()


def parse_job_from_settings(settings, name):
    if len(settings) == 0:
        print(f"The name `{name}` doesn't appear in supplied schedule config.")
        raise typer.Exit(code=1)
    arguments = " ".join([f"--{k} {v}" for k, v in settings.get('arguments', {}).items()])
    return f"{settings['command']} {arguments}"


class Cron:
    def __init__(self, settings_path):
        self.settings = Clumper.read_yaml(settings_path).unpack("schedule").collect()

    def grab_nums(self, setting):
        return int("".join([s for s in setting["every"] if s.isdigit()]))

    def parse_cmd(self, setting_dict):
        """
        Parse settings into elaborate command for CRON.
        """
        # If no venv is given we assume the one you're currently in.
        python = "python"
        if "venv" not in setting_dict.keys():
            output = subprocess.run(["which", "python"], capture_output=True)
            python = output.stdout.decode("ascii").replace("\n", "")
        # Set base values.
        retry = setting_dict.get("retry", 2)
        wait = setting_dict.get("wait", 60)
        # We only want to replace python if it is at the start.
        cmd = parse_job_from_settings(setting_dict, setting_dict["name"])
        if cmd.startswith("python"):
            cmd = cmd.replace("python", python, 1)
            print(f"Parsed command:\n{cmd}")
        big_cmd = f'{python} -m skedulord run {setting_dict["name"]} "{cmd}" --retry {retry} --wait {wait}'
        return big_cmd

    def set_new_cron(self):
        cron = CronTab(user=self.settings[0]["user"])
        cron.remove_all()

        for s in self.settings:
            s["name"] = s["name"].replace(" ", "-")
            cmd = self.parse_cmd(setting_dict=s)
            job = cron.new(command=cmd, comment=s["name"])
            job.setall(s["cron"])
        cron.write()
