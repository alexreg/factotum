from typing import *

import typer_cloup as typer

from factotum import *

cli = Factum()


class CustomContext(typer.Context):
    pass


class CustomCommand(Command):
    context_class: Type[typer.Context] = CustomContext
