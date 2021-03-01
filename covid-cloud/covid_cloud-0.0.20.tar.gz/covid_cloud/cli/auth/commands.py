import click
from covid_cloud.client.auth import login
from covid_cloud.client import *
from covid_cloud.cli.utils import assert_config, get_config, set_config
import covid_cloud.constants
import yaml
import datetime as dt


@click.group()
@click.pass_context
def auth(ctx):
    pass


@auth.command("login")
@click.pass_context
def cli_login(ctx, refresh=False):
    personal_access_token = get_config(ctx, "personal_access_token")
    email = get_config(ctx, "email")
    client_id = get_config(ctx, "client-id")
    client_secret = get_config(ctx, "client-secret")
    client_redirect_uri = get_config(ctx, "client-redirect-uri")

    try:
        access_token = login(email, personal_access_token, client_id, client_secret, client_redirect_uri,
                             wallet_uri=get_config(ctx, 'wallet-url'), search_url=get_config(ctx, 'search-url'),
                             drs_url=get_config(ctx, "drs-url"))
    except:
        click.secho("There was an error generating an access token", fg='red')
        return

    # convert the expiry from a relative time to an actual timestamp
    access_token['expiry'] = (
                dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(minutes=access_token['expires_in'])).timestamp()
    del access_token['expires_in']

    set_config(ctx, 'oauth_token', access_token)

    # if we're refrshing the token, we don't want the user to see that we're refreshing
    if not refresh:
        click.secho('You are now logged in.', fg='green')
