from factotum import *

cli = Factum()


@cli.command()
def exit_good():
    exit()
    print("unreachable")  # pragma: no cover


@cli.command()
def exit_bad():
    exit(123)
    print("unreachable")  # pragma: no cover
