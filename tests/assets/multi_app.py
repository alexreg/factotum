from factotum import *

factum = Factum(help="Demo App", epilog="The end")
subfactum = Factum()
factum.add_sub(subfactum, name="sub")

variable = "Some text"


@subfactum.command()
def hello(name: str = "World", age: int = Option(0, help="The age of the user")):
    """
    Say Hello
    """
    echo(f"Hello {name}")


@subfactum.command()
def hi(user: str = Argument("World", help="The name of the user to greet")):
    """
    Say hello
    """


@subfactum.command()
def bye():
    """
    Say bye
    """
    echo("sub bye")


@factum.command()
def top():
    """
    Top command
    """
    echo("top")
