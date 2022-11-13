import subprocess


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/multi_app.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "sub" in result.stdout
    assert "top" in result.stdout


def test_script_sub():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "hello" in result.stdout


def test_script_top():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/multi_app.py",
            "run",
            "top",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "top" in result.stdout


def test_script_sub_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_script_sub_bye():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "bye",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "sub bye" in result.stdout
