import subprocess


def test_script():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/not_factum_context.py",
            "run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert (
        "TypeError: `context_class` is not instance of `FactotumContext`"
        in result.stderr
    )
