from factotum import *

factum = Factum()
factum.add_sub("sample.py", name="imported")  # type: ignore


@factum.callback()
def callback() -> None:
    """Top-level CLI"""
