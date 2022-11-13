from factotum import *

factum = Factum()
subfactum = Factum()
factum.add_sub(subfactum, name="sub")


@subfactum.command()
def hello():
    echo("sub hello")


@subfactum.command()
def bye():
    echo("sub bye")


@factum.command()
def top():
    echo("top")
