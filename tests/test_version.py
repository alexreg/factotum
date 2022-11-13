import subprocess

import factotum_cli


def test_script_version():
    result = subprocess.run(
        ["coverage", "run", "-m", "factotum_cli", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert f"Factotum v{factotum_cli.__version__}" in result.stdout
