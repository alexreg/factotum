from factotum import *

sample = import_module("sample.py")

factum = Factum()
factum.add_sub(sample.factum, name="imported")  # type: ignore


@factum.callback()
def callback() -> None:
    """
    Imports sample factum
    """
