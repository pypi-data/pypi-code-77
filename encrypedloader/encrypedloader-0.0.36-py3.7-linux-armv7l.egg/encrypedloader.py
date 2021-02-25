import click
from . import loader

@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('key')
@click.argument('fp')
def encrypt(key, fp):
    loader.encrypt_file(fp, key)
    click.echo('encrypted!')


@cmd.command()
@click.argument('expire')
def genkey(expire):
    loader.gen_key(int(expire))


cli = click.CommandCollection(sources=[cmd,])


def main():
    cli()
