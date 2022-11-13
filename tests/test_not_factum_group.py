import subprocess


def test_script_1():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/not_factum_group_1.py",
            "run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "TypeError: `cls` is not `FactumGroup` or subclass" in result.stderr


def test_script_2():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/not_factum_group_2.py",
            "run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "TypeError: `cls` is not `FactumGroup` or subclass" in result.stderr


def test_script_3():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/not_factum_group_3.py",
            "run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "TypeError: `cls` is not `FactumGroup` or subclass" in result.stderr
