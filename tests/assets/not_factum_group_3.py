import typer_cloup as typer

from factotum import *

cli = Factum()
cli.add_sub(Factum(), cls=typer.main.TyperGroup)
