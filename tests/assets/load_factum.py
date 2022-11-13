from factotum import *

factum = Factum.load("sample.py")


@factum.command()
def ciao(name: str = "Mondo"):
    """Say ciao"""
    echo(f"Ciao {name}")
