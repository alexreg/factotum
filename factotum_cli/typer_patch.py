from functools import wraps

import click
import typer_cloup as typer

old_get_short_help_str = typer.main.TyperCommand.get_short_help_str


@wraps(typer.main.TyperCommand.get_short_help_str)
def new_get_short_help_str(self: click.Command, limit: int = 45) -> str:
    help = old_get_short_help_str(self, limit)
    if getattr(self.callback, "__factotum_is_default__", False):
        help = f"{help}  [default]" if help else f"[default]"

    return help


typer.main.TyperCommand.get_short_help_str = new_get_short_help_str  # type: ignore
