from factotum import *

sample = import_path("sample.py")

cli = Factum()
cli.add_sub(sample.cli, name="imported")  # type: ignore


@cli.callback()
def callback() -> None:
    """
    Imports sample CLI
    """
