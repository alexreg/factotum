import typer_cloup as typer

from factotum import *

factum = Factum()


@factum.callback(cls=typer.main.TyperGroup)
def callback():  # pragma: no cover
    pass
