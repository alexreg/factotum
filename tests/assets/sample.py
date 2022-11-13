#!/usr/bin/env factotum-script
from factotum import *

cli = Factum(help="Sample script")


@cli.command()
def hello(name: str = "World", formal: bool = False):
    """
    Say hello
    """

    if formal:
        echo(f"Good day, {name}")
    else:
        echo(f"Hello {name}")


@cli.command()
def bye(friend: bool = False):
    """
    Say bye
    """
    if friend:
        echo("Goodbye, my friend")
    else:
        echo("Goodbye")


cli.set_default(hello)
