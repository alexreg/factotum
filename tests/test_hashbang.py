import subprocess


def test_script_hello_name():
    result = subprocess.run(
        ["tests/assets/sample.py", "hello", "--name", "Joe Bloggs"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello Joe Bloggs" in result.stdout


def test_help():
    result = subprocess.run(
        ["tests/assets/sample.py", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "Usage: sample.py" in result.stdout
    assert "bye" in result.stdout
    assert "Say bye" in result.stdout
    assert "hello" in result.stdout
    assert "Say hello  [default]" in result.stdout
