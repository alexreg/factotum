import typer_cloup as typer

from factotum import *

cli = Factum()


@cli.callback(cls=typer.main.TyperGroup)
def callback():  # pragma: no cover
    pass
