import subprocess


def test_script_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_script_hello_name():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "hello",
            "--name",
            "Joe Bloggs",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello Joe Bloggs" in result.stdout


def test_script_hello_name_formal():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "hello",
            "--name",
            "Joe Bloggs",
            "--formal",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Good day, Joe Bloggs" in result.stdout


def test_script_bye():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "bye",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Goodbye" in result.stdout


def test_script_bye_friend():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "bye",
            "--friend",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Goodbye, my friend" in result.stdout


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/sample.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "factotum_cli --path tests/assets/sample.py run" in result.stdout
    assert "Sample script" in result.stdout
    assert "bye" in result.stdout
    assert "Say bye" in result.stdout
    assert "hello" in result.stdout
    assert "Say hello" in result.stdout
