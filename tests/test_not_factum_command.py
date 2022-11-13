import subprocess


def test_script():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/not_factum_command.py",
            "run",
            "command",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "TypeError: `cls` is not `FactumCommand` or subclass" in result.stderr
