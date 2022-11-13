from factotum import *

cli = Factum()


@cli.callback(invoke_without_command=True)
def callback(ctx: Context, verbose: bool = verbose_option()):
    pass


@cli.command()
def hello():
    """
    Say hello
    """

    ctx = get_current_context()
    if ctx and ctx.verbose:
        echo("Running `hello` command...")

    echo("Hello World")
