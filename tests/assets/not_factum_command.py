import typer_cloup as typer

from factotum import *

cli = Factum()


@cli.command(cls=typer.main.TyperCommand)
def command():  # pragma: no cover
    pass
