import click
from encrypedloader.loader import encrypt_file, gen_key

@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('key')
@click.argument('fp')
def encrypt(key, fp):
    encrypt_file(fp, key)
    click.echo('encrypted!')


@cmd.command()
@click.argument('expire')
def genkey(expire):
    gen_key(int(expire))


cli = click.CommandCollection(sources=[cmd,])


def main():
    cli()
