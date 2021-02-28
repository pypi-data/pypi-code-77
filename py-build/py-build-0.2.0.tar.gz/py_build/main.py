from py_build import Builder
import logging
import importlib
import sys

def main(package: str, *targets) -> int:
    for target in targets:
        module = "{}.{}".format(package, target)
        try:
            build_steps = importlib.import_module(module).build_steps
        except ModuleNotFoundError as ex:
            print("Module `{}` not found".format(module), file=sys.stderr)
            logging.getLogger(__name__).error("Module `%s` not found", module)
            return 1
        builder = Builder()
        build_steps(builder)
        builder.build()
    return 0