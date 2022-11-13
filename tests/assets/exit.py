from factotum import *

factum = Factum()


@factum.command()
def exit_good():
    exit()
    print("unreachable")  # pragma: no cover


@factum.command()
def exit_bad():
    exit(123)
    print("unreachable")  # pragma: no cover
