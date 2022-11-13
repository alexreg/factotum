import subprocess


def test_script_exit_good():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/exit.py",
            "run",
            "exit-good",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "unreachable" not in result.stdout


def test_script_exit_bad():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/exit.py",
            "run",
            "exit-bad",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 123
    assert "unreachable" not in result.stdout
