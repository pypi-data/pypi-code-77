import click
import logging
import yaml
import json
import sys
import ast
from collections import defaultdict
from functools import reduce
import os
from nb2workflow.nbadapter import notebook_short_name, NotebookAdapter
import odacc
import re

logger = logging.getLogger(__name__)

class UnsetDict:
    def __init__(self, data):
        self._data = data

    def get(self, k, default):
        return self.__getitem__(k)

    def __getitem__(self, k):
        return self.__class__(
                    self._data.get(
                            k,
                            self.__class__({}),
                        )
                )

    def __str__(self):
        if self._data == {}:
            return "unset"
        return str(self._data)


@click.group()
@click.option("-d", "--debug", is_flag=True, default=False)
@click.option("-C", "--change-dir")
@click.pass_context
def cli(ctx, debug, change_dir=None):
    ctx.obj = {}
    obj = ctx.obj

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    if change_dir is None:
        change_dir = os.getcwd()

    try:
        obj["change_dir"] = change_dir

        obj["oda_yaml"] = yaml.load(open(os.path.join(change_dir, "oda.yaml")), Loader=yaml.SafeLoader)

        logging.debug("loaded: %s", obj['oda_yaml'])
    except Exception as e:
        logging.warning("can not load oda.yaml: not test case based call")


@cli.command()
@click.pass_obj
def inspect(obj):
    pass

@cli.command()
@click.argument("path")
@click.argument("default")
@click.pass_obj
def get(obj, path, default):
    try:
        click.echo(reduce(
                lambda x, y: x[y],
                [obj['oda_yaml']] + path.split(".")))
    except (KeyError, TypeError) as e:
        click.echo(default)


@cli.command()
@click.argument("template")
@click.option("-n", "--notebook", default=None)
@click.option("-e", "--from-env", default=None)
@click.pass_obj
def format(obj, template, notebook, from_env):
    if from_env:
        if from_env in os.environ:
            pars=ast.literal_eval(os.environ[from_env])
        else:
            logger.warning("\033[31mERROR: parameters requested from env variable %s, but variable not set! Using default {}.\033[0m", from_env)
            pars={}
    elif notebook:
        n = notebook_short_name(notebook)
        nba = NotebookAdapter(notebook)
        pars = nba.extract_parameters()
    else:
        pars=json.load(open(os.path.join(obj["change_dir"], "pars.json")))

    if template == "AUTO":
        click.echo("_".join([f"{k}{v}" for k, v in pars.items()]))
    else:
        click.echo(
            template.format(
                pars=UnsetDict(pars)
            )
        )

@cli.command()
@click.option("-c", "--check", default=None)
@click.pass_obj
def version(obj, check):
    print("version:", odacc.__version__)
    if check:
        v = re.search('version = "(.*?)",', open(os.path.join(check, "setup.py")).read()).groups()[0]
        if v != odacc.__version__:
            print(f"mismatch! found version {v} module version {odacc.__version__}")
            sys.exit(1)
        else:
            print(f"version matches in {check}")


@cli.command()
@click.argument("bucket")
def annotate_explain_bucket(bucket):
    import odakb.datalake

    m, d = odakb.datalake.restore(bucket, return_metadata=True)

    print(m)

    odakb.sparql.insert(f'oda:{bucket} a oda:ccbucket; oda:bucket "{bucket}"')

    funcbase = m["query"].replace("http://", "").replace(".io/", "").replace("/", "-") 
    func = funcbase + m['version']

    x  = f'oda:{bucket} oda:curryingOf oda:{func} .'
    x += f'oda:{func} oda:curryingOf oda:{funcbase} .'
    print(x)
    odakb.sparql.insert(x)

    for k, v in m['kwargs'].items():
        x = f'oda:{bucket} oda:curryied_input_{k} "{v}"'
        print(">>", x)
        odakb.sparql.insert(x)


if __name__ == "__main__":
    cli()
