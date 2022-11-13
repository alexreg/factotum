import typer_cloup as typer

from factotum import *

factum = Factum()
factum.add_sub(Factum(), cls=typer.main.TyperGroup)
