import click
import datetime as dt
from covid_cloud.cli.utils import has_config, get_config
from covid_cloud.cli.auth.commands import cli_login

def assert_token(ctx):

    # there is no good way got telling if the server is authenticated yet,
    # so if the user does not have a token set up, assume that is is public and
    # don't do anything
    if not has_config(ctx,"oauth_token"):
        return

    oauth_token = get_config(ctx,"oauth_token")
    if oauth_token["expiry"] > dt.datetime.now(tz=dt.timezone.utc):
        cli_login(ctx, refresh=True)