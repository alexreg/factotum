import subprocess
from typing import IO, Optional

import click


class CalledProcessError(click.ClickException):
    def __init__(self, error: subprocess.CalledProcessError):
        self.message = str(error)
        self.exit_code = error.returncode

    def show(self, file: Optional[IO] = None) -> None:
        pass
