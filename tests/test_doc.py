import subprocess
from pathlib import Path


def test_doc():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "-m",
            "tests.assets.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    docs_path = Path(__file__).parent / "assets/multiapp-docs.md"
    docs = docs_path.read_text()
    assert docs in result.stdout
    assert "**Arguments**" in result.stdout


def test_doc_output(tmp_path):
    out_file = tmp_path / "out.md"
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "-m",
            "tests.assets.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
            "--output",
            str(out_file),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    docs_path = Path(__file__).parent / "assets/multiapp-docs.md"
    docs = docs_path.read_text()
    written_docs = out_file.read_text()
    assert docs in written_docs
    assert "Docs written to" in result.stdout


def test_doc_not_existing():
    result = subprocess.run(
        ["coverage", "run", "-m", "factotum_cli", "-m", "no_typer", "utils", "docs"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Could not import `no_typer` as Python module" in result.stderr


def test_doc_empty_script():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "tests/assets/empty_script.py",
            "utils",
            "docs",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert (
        "Module does not have `factum` or `create_factum` attribute." in result.stderr
    )


def test_doc_file_not_existing():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "factotum_cli",
            "--path",
            "assets/not_existing.py",
            "utils",
            "docs",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "No such file or directory" in result.stderr
