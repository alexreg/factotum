#!/usr/bin/env factotum-script
from factotum import *

factum = Factum(help="Sample script")


@factum.command()
def hello(name: str = "World", formal: bool = False):
    """Say hello"""
    if formal:
        echo(f"Good day, {name}")
    else:
        echo(f"Hello {name}")


@factum.command()
def bye(friend: bool = False):
    """Say bye"""
    if friend:
        echo("Goodbye, my friend")
    else:
        echo("Goodbye")
