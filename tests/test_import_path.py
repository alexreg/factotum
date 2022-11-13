import subprocess


def test_script_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/import_path.py",
            "run",
            "imported",
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
            "tests/assets/import_path.py",
            "run",
            "imported",
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
            "tests/assets/import_path.py",
            "run",
            "imported",
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
            "tests/assets/import_path.py",
            "run",
            "imported",
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
            "tests/assets/import_path.py",
            "run",
            "imported",
            "bye",
            "--friend",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Goodbye, my friend" in result.stdout


def test_script_default():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/import_path.py",
            "run",
            "imported",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/import_path.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "factotum_cli --path tests/assets/import_path.py run" in result.stdout
    assert "Imports sample CLI" in result.stdout
    assert "Commands" in result.stdout
    assert "imported" in result.stdout


def test_script_imported_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/import_path.py",
            "run",
            "imported",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert (
        "factotum_cli --path tests/assets/import_path.py run imported" in result.stdout
    )
    assert "Sample script" in result.stdout
    assert "bye" in result.stdout
    assert "Say bye" in result.stdout
    assert "hello" in result.stdout
    assert "Say hello  [default]" in result.stdout
