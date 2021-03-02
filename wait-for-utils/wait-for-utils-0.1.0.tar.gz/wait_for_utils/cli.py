"""run."""
import click

from wait_for_utils import wait_for_pg, config, __version__
from wait_for_utils.utils import clean_args


@click.command()
@click.help_option("--help")
@click.version_option(
    __version__, "-v", "--version", message="Version of wait_for_utils %(version)s"
)
@click.option("-p", "--port", type=int, help="Port")
@click.option("-d", "--database", type=str, help="Database name")
@click.option("-u", "--user", type=str, help="Database user")
@click.option(
    "--password",
    # prompt=True,
    # hide_input=True,
    help="Database password",
)
@click.option("-h", "--host", type=str, help="Host")
@click.option("-t", "--timeout", metavar="seconds", type=int, help="Check timeout")
@click.option("-i", "--interval", metavar="seconds", type=str, help="Check interval")
def wait_for_postgres(**kwargs):
    """Wait for service to be available.

    :return:
    """
    cfg = config.DBConfig(**clean_args(kwargs))
    return wait_for_pg.PGReady().is_ready(config=cfg)


if __name__ == "__main__":
    wait_for_postgres()
