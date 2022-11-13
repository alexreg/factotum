import subprocess


def test_missing_command():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "factotum_cli [OPTIONS]"
    assert "Error: Missing command." in result.stderr


def test_missing_command_utils():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "utils",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "factotum_cli utils [OPTIONS]"
    assert "Error: Missing command." in result.stderr
