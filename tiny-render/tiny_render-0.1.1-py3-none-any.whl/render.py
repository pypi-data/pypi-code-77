# -*- coding: utf-8 -*-

from datetime import datetime
import os
import json
import subprocess

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

class Render(object):
    """A simple Jinja2 wrapper to provide the build-in variables
    `_gitsha` - git short sha
    `_date_str` - yyyymmdd string
    `_time_str` - yyyymmddHHMMSS string
    """
    def __init__(self, template_dir: str):
        """Init the Render by giving a directory contains your template
        """
        if not os.path.isdir(template_dir):
            raise ValueError(f"{template_dir} is not a valid directory")

        self._dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def __repr__(self):
        return f"Render({self._dir})"

    @staticmethod
    def get_shortsha():
        short_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        short_hash = str(short_hash, "utf-8").strip()

        return short_hash

    def go(self, template: str, *args, **kwargs) -> str:
        """ Do the actual rendering process, and print the renderred content
        """
        current_date = datetime.now()
        template = self.env.get_template(template)
        kwargs["_gitsha"] = Render.get_shortsha()
        kwargs["_date_str"] = current_date.strftime("%Y%m%d")
        kwargs["_time_str"] = current_date.strftime("%Y%m%d%H%M%S")

        return template.render(*args, **kwargs)