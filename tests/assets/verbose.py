from factotum import *

factum = Factum()


@factum.callback(invoke_without_command=True)
def callback(ctx: Context, verbose: bool = verbose_option()):
    pass


@factum.command()
def hello():
    """Say hello"""
    ctx = get_current_context()
    if ctx is not None and ctx.verbose:
        echo("Running `hello` command...")

    echo("Hello World")
