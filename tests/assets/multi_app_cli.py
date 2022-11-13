from factotum import *

cli = Factum()
sub_cli = Factum()
cli.add_sub(sub_cli, name="sub")


@sub_cli.command()
def hello():
    echo("sub hello")


@sub_cli.command()
def bye():
    echo("sub bye")


@cli.command()
def top():
    echo("top")
