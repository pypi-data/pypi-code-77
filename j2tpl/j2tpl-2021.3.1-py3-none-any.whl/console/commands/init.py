import json
from pathlib import Path
from shutil import copy
from typing import Dict
from typing import List

import cleo
from cleo.commands.command import Command as BaseCommand
from jinja2 import Environment
from jinja2 import FileSystemLoader


class Command(BaseCommand):
    """
    Initialises target using a template

    init
        {source : Source template file or folder}
        {target : Target file or folder}
        {--f|force : Overwrite existing file(s)}
        {--x|exclude=* : Excluded path(s)}
        {--var=* : Variable in <comment>key=value</comment> format}
        {--var-file= : Variable file}
    """

    def handle(self) -> None:
        source = Path(self.argument("source"))
        target = Path(self.argument("target"))
        self._force = self.option("force")
        self._excludes = [x for x in self.option("exclude")]
        self._args = self._load_vars_from_file(self.option("var-file"))

        for o in self.option("var"):
            k, v = tuple(o.split("="))
            self._args[k] = v

        self._process_path(source, target)

    def _load_vars_from_file(self, var: Path) -> Dict[str, str]:
        data = {}
        if var:
            with open(var, "r") as f:
                data = json.loads(f.read())
        return data

    def _process_path(self, source: Path, target: Path) -> None:
        for p in source.iterdir():
            if p.name in self._excludes:
                self.line(f"'{p}' excluded source path")
                continue

            t = target / p.relative_to(source)
            if p.is_file():
                if t.exists() and not self._force:
                    self.line(f"'{t}' already exists")
                    # , verbosity=cleo.VERBOSITY_NORMAL)
                    continue

                if p.suffix == ".j2":
                    env = Environment(
                        loader=FileSystemLoader(p.parent),
                        # extensions=?
                        keep_trailing_newline=True,
                    )
                    with open(t.parent / t.stem, "w") as out:
                        tmpl = env.get_template(p.name)
                        out.write(tmpl.render(self._args))
                else:
                    copy(p, t)
            elif p.is_dir():
                if not t.exists():
                    t.mkdir()
                self._process_path(p, t)
