from pathlib import Path
from typing import *

import click
import cloup
import typer_cloup as typer
from cloup.constraints import mutually_exclusive
from typer_cloup import colors, constraint
from typer_cloup.core import TyperCommand, TyperGroup, TyperOption

import factotum.main
from factotum.main import Factum, FactumContext

from . import __version__
from .typer_patch import *

app = typer.Typer(
    context_settings=typer.Context.settings(
        help_option_names=["--help", "-h"],
    ),
)
utils_app = typer.Typer(help="Utility commands")
app.add_sub(utils_app, name="utils")

script_mode: bool = False
script_name: str


class AppContext(typer.Context):
    @property
    def command_path(self) -> str:
        if self.invoked_subcommand is None:
            return super().command_path

        command_path = super().command_path
        root_ctx = super(typer.Context, self).find_root()
        path_param = root_ctx.params["path"]
        module_param = root_ctx.params["module"]
        if path_param is not None:
            return f"{command_path} --path {path_param}"
        elif module_param is not None:
            return f"{command_path} --module {module_param}"
        else:
            return f"{command_path}"


class AppGroup(TyperGroup):
    context_class: Type[typer.Context] = AppContext

    _run_added: bool = False

    def __init__(
        self, *args: Any, show_subcommand_aliases: Optional[bool] = None, **kwargs: Any
    ):
        super().__init__(
            *args, show_subcommand_aliases=show_subcommand_aliases, **kwargs
        )

        self.add_command(
            TyperCommand("run", aliases=["r"], help="Run the given Factum.")
        )

    def list_commands(self, ctx: click.Context) -> List[str]:
        self.maybe_add_run(ctx)
        return super().list_commands(ctx)

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        self.maybe_add_run(ctx)
        return super().get_command(ctx, name)

    def invoke(self, ctx: click.Context) -> Any:
        self.maybe_add_run(ctx)
        return super().invoke(ctx)

    def maybe_add_run(self, ctx: click.Context) -> None:
        if self._run_added:
            return
        else:
            self._run_added = True

        path_param: Path = ctx.params["path"]
        module_param: str = ctx.params["module"]

        if path_param is not None or module_param is not None:
            factum = load_factum(ctx)
            if factum is not None:
                command = typer.main.get_command(factum)
                command.name = "run"
                command.callback = get_run_callback(command.callback)
                if not script_mode and isinstance(command, cloup.Command):
                    command.aliases = ["r"]

                del self._default_section.commands["run"]
                self.add_command(command)


# Dummy class just for monkey-patching
class FactumHostContext(FactumContext):
    @property
    def _is_root(self) -> bool:
        return self.parent is not None and isinstance(self.parent.command, AppGroup)

    @property
    def command_path(self) -> str:
        if script_mode and self._is_root:
            return script_name

        return super(typer.Context, self).command_path


FactumContext._is_root = FactumHostContext._is_root  # type: ignore
FactumContext.command_path = FactumHostContext.command_path  # type: ignore


def load_factum(ctx: click.Context) -> Optional[Factum]:
    import importlib.machinery
    import importlib.util

    root_ctx = ctx.find_root()
    verbose: bool = root_ctx.params["verbose"]
    path: Path = root_ctx.params["path"]
    module: str = root_ctx.params["module"]

    spec = None
    if module is not None:
        if verbose:  # pragma: no cover
            typer.secho(f"Loading Factum from module `{module}`...", fg=colors.GREEN)

        spec = importlib.util.find_spec(module)  # type: ignore
    else:
        path = path or Path("Factum")
        module = path.name

        if verbose:  # pragma: no cover
            typer.secho(f"Loading Factum from path `{path}`...", fg=colors.GREEN)

        spec = importlib.util.spec_from_loader(
            module,
            importlib.machinery.SourceFileLoader(module, str(path)),
        )

    if spec is None:
        if module is not None:
            typer.echo(f"Could not import `{module}` as Python module", err=True)
        else:
            assert False  # pragma: no cover
        raise typer.Exit(1)

    module_obj = importlib.util.module_from_spec(spec)
    assert spec.loader is not None

    factotum.main.run_path = Path(module_obj.__file__) if module_obj.__file__ else None

    spec.loader.exec_module(module_obj)

    factum: Optional[Factum] = getattr(module_obj, "factum", None)
    if factum is None:
        return None

    factum._add_completion = False

    return factum


def get_run_callback(callback: Optional[Callable[..., Any]]) -> Callable[..., Any]:
    def run_callback(*args: Any, **kwargs: Any) -> None:
        ctx = click.get_current_context()
        ctx.find_root()

        if callback is not None:
            callback(*args, **kwargs)

    return run_callback


def get_docs_for_command(
    *,
    obj: click.Command,
    ctx: typer.Context,
    indent: int = 0,
    name: str = "",
    call_prefix: str = "",
) -> str:
    docs = "#" * (1 + indent)

    command_name = name or obj.name
    if call_prefix:
        command_name = f"{call_prefix} {command_name}"

    title = f"`{command_name}`" if command_name else "Factum"
    docs += f" {title}\n\n"

    if obj.help:
        docs += f"{obj.help}\n\n"

    usage_pieces = obj.collect_usage_pieces(ctx)
    if usage_pieces:
        docs += "**Usage**:\n\n"
        docs += "```console\n"
        docs += "$ "
        if command_name:
            docs += f"{command_name} "
        docs += f"{' '.join(usage_pieces)}\n"
        docs += "```\n\n"

    args = []
    opts = []

    for param in obj.get_params(ctx):
        rv = param.get_help_record(ctx)
        if rv is not None:
            if param.param_type_name == "argument":
                args.append(rv)
            elif param.param_type_name == "option":
                opts.append(rv)
    if args:
        docs += f"**Arguments**:\n\n"

        for arg_name, arg_help in args:
            docs += f"* `{arg_name}`"
            if arg_help:
                docs += f": {arg_help}"
            docs += "\n"

        docs += "\n"
    if opts:
        docs += f"**Options**:\n\n"

        for opt_name, opt_help in opts:
            docs += f"* `{opt_name}`"
            if opt_help:
                docs += f": {opt_help}"
            docs += "\n"

        docs += "\n"
    if obj.epilog:
        docs += f"{obj.epilog}\n\n"
    if isinstance(obj, click.Group):
        group: click.Group = cast(click.Group, obj)
        subcommand_names = group.list_commands(ctx)

        if subcommand_names:
            docs += f"**Commands**:\n\n"
            for subcommand_name in subcommand_names:
                subcommand = group.get_command(ctx, subcommand_name)
                assert subcommand
                docs += f"* `{subcommand.name}`"
                subcommand_help = subcommand.get_short_help_str()
                if subcommand_help:
                    docs += f": {subcommand_help}"
                docs += "\n"
            docs += "\n"

        for subcommand_name in subcommand_names:
            subcommand = group.get_command(ctx, subcommand_name)
            assert subcommand
            use_prefix = ""
            if command_name:
                use_prefix += f"{command_name}"
            docs += get_docs_for_command(
                obj=subcommand, ctx=ctx, indent=indent + 1, call_prefix=use_prefix
            )

    return docs


def print_version(ctx: typer.Context, param: TyperOption, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    typer.echo(f"Factotum v{__version__}")
    raise typer.Exit()


@app.callback(cls=AppGroup)
@constraint(mutually_exclusive, "path", "module")
def callback(
    ctx: typer.Context,
    *,
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        file_okay=True,
        dir_okay=True,
        help="Read PATH as the Factum file/directory.",
    ),
    module: Optional[str] = typer.Option(
        None,
        "--module",
        "-m",
        metavar="MODULE",
        help="Read MODULE as the Factum module.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Write verbose output.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=print_version,
        is_eager=True,
        help="Print version and exit.",
    ),
) -> None:
    """Factotum: a generic task runner and build tool based on Python scripting"""


@utils_app.command()
def docs(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="The name of the CLI program to use in docs.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        file_okay=True,
        dir_okay=False,
        help="The file to write docs to.",
    ),
) -> None:
    """Generate Markdown documentation for the given factum."""
    root_ctx = ctx.find_root()

    factum = load_factum(root_ctx)
    if factum is None:
        typer.echo(f"No Factum found", err=True)
        raise typer.Exit(1)

    name = name or f"{root_ctx.command_path} run"

    command = typer.main.get_command(factum)
    docs = get_docs_for_command(obj=command, ctx=ctx, name=name or "")
    clean_docs = f"{docs.strip()}\n"

    if output is not None:
        output.write_text(clean_docs)
        typer.echo(f"Docs written to `{output}`.")
    else:
        typer.echo(clean_docs)


def main() -> Any:
    return app()


def script() -> Any:
    import sys

    path = Path(sys.argv[1])
    argv = ["--path", path, "run"] + sys.argv[2:]

    global script_mode, script_name
    script_mode = True
    script_name = path.name

    return app(argv)
