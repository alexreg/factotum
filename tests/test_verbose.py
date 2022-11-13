import subprocess


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/verbose.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "-v, --verbose" in result.stdout


def test_script_verbose():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/verbose.py",
            "run",
            "--verbose",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Running `hello` command..." in result.stdout
    assert "Hello World" in result.stdout
