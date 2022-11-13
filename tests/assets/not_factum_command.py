import typer_cloup as typer

from factotum import *

factum = Factum()


@factum.command(cls=typer.main.TyperCommand)
def command():  # pragma: no cover
    pass
