# simple note taker
# run with python to take and retrieve notes

import typer
import typer.colors as colours

app = typer.Typer()


@app.command()
def hello():
    person_name = typer.prompt("What's your name?")
    typer.secho(f"Hello {person_name}", fg=colours.BRIGHT_CYAN)


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.secho(f"Goodbye Ms. {name}. Have a good day.", fg=colours.GREEN)
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
