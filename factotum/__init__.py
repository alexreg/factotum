"""Factotum: a generic task runner and build tool based on Python scripting"""

from importlib import metadata

from typer_cloup import Abort as Abort
from typer_cloup import Argument as Argument
from typer_cloup import BadParameter as BadParameter
from typer_cloup import CallbackParam as CallbackParam
from typer_cloup import Context as Context
from typer_cloup import Exit as Exit
from typer_cloup import FileBinaryRead as FileBinaryRead
from typer_cloup import FileBinaryWrite as FileBinaryWrite
from typer_cloup import FileText as FileText
from typer_cloup import FileTextWrite as FileTextWrite
from typer_cloup import Option as Option
from typer_cloup import clear as clear
from typer_cloup import colors as colors
from typer_cloup import confirm as confirm
from typer_cloup import constraint as constraint
from typer_cloup import echo as echo
from typer_cloup import echo_via_pager as echo_via_pager
from typer_cloup import edit as edit
from typer_cloup import format_filename as format_filename
from typer_cloup import get_app_dir as get_app_dir
from typer_cloup import get_binary_stream as get_binary_stream
from typer_cloup import get_text_stream as get_text_stream
from typer_cloup import getchar as getchar
from typer_cloup import launch as launch
from typer_cloup import open_file as open_file
from typer_cloup import option_group as option_group
from typer_cloup import pause as pause
from typer_cloup import progressbar as progressbar
from typer_cloup import prompt as prompt
from typer_cloup import run as run
from typer_cloup import secho as secho
from typer_cloup import style as style
from typer_cloup import unstyle as unstyle

from .main import FactotumError
from .main import Factum as Factum
from .main import FactumCommand as Command
from .main import FactumContext as Context
from .main import FactumGroup as Group
from .main import exit as exit
from .main import get_current_context, import_module, is_entry_point, param, run_path
from .main import verbose_option as verbose_option

__version__ = metadata.version("factotum")
