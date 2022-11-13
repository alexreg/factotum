from factotum import *

cli = Factum(help="Demo App", epilog="The end")
sub_cli = Factum()
cli.add_sub(sub_cli, name="sub")

variable = "Some text"


@sub_cli.command()
def hello(name: str = "World", age: int = Option(0, help="The age of the user")):
    """
    Say Hello
    """
    echo(f"Hello {name}")


@sub_cli.command()
def hi(user: str = Argument("World", help="The name of the user to greet")):
    """
    Say hello
    """


@sub_cli.command()
def bye():
    """
    Say bye
    """
    echo("sub bye")


@cli.command()
def top():
    """
    Top command
    """
    echo("top")
