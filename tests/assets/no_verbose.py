from factotum import *

cli = Factum()


@cli.callback(invoke_without_command=True)
def callback(ctx: Context):
    pass


@cli.command()
def hello():
    """
    Say hello
    """

    ctx = get_current_context()
    if ctx:
        echo(f"Verbose: {ctx.verbose}")

    echo("Hello World")
