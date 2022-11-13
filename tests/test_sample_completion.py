import os
import subprocess


def test_script_completion_run():
    result = subprocess.run(
        ["coverage", "run", "-m", "factotum_cli"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "___MAIN__.PY_COMPLETE": "complete_bash",
            "_PYTHON _M FACTOTUM_CLI_COMPLETE": "complete_bash",
            "COMP_WORDS": "factotum --path tests/assets/sample.py run hello --",
            "COMP_CWORD": "5",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "--name" in result.stdout
