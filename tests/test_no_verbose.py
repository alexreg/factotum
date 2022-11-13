import subprocess


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/no_verbose.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "-v, --verbose" not in result.stdout


def test_script_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/no_verbose.py",
            "run",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Verbose: None" in result.stdout
    assert "Hello World" in result.stdout
