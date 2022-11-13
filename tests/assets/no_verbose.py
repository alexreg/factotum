from factotum import *

factum = Factum()


@factum.callback(invoke_without_command=True)
def callback(ctx: Context):
    pass


@factum.command()
def hello():
    """
    Say hello
    """

    ctx = get_current_context()
    if ctx is not None:
        echo(f"Verbose: {ctx.verbose}")

    echo("Hello World")
