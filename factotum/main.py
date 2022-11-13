from copy import copy
from functools import cache, wraps
from os import PathLike
from pathlib import Path, PurePath
from types import ModuleType
from typing import *

import click
import cloup
import typer_cloup as typer
from typer_cloup import Typer, colors
from typer_cloup.main import TyperCommand, TyperGroup
from typer_cloup.models import CommandFunctionType, Default, DefaultPlaceholder
from varname import nameof

if TYPE_CHECKING:  # pragma: no cover
    from cloup.constraints import BoundConstraintSpec


class FactotumError(Exception):
    pass


class FactumContext(typer.Context):
    @cache
    def find_root(self) -> "FactumContext":
        """Find the outermost factum context."""
        node: Optional["click.Context"] = self

        while node is not None:
            if isinstance(node, FactumContext) and getattr(node, "_is_root", False):
                return node

            node = node.parent

        raise FactotumError("root context not found")  # pragma: no cover

    @property
    def verbose(self) -> Optional[bool]:
        """Return whether the "verbose" flag was passed to the root factum.

        The return value is `None` if the factum does not have a "verbose" flag.
        """
        root_ctx = self.find_root()
        return root_ctx.params.get("verbose")


class FactumCommand(TyperCommand):
    context_class: Type[typer.Context] = FactumContext

    def __init_subclass__(cls) -> None:
        if not issubclass(cls.context_class, FactumContext):
            raise TypeError(
                f"`{nameof(cls.context_class)}` is not instance of `{FactumContext.__name__}`"
            )

        return super().__init_subclass__()


class FactumGroup(FactumCommand, TyperGroup):
    pass


class Factum(Typer):
    """A factum: a CLI interface for a set of tasks."""

    _default_context_settings: ClassVar[Dict[str, Any]] = typer.Context.settings(
        help_option_names=["--help", "-h"],
    )

    @staticmethod
    def load(path: Union[str, PathLike]) -> "Factum":
        """Load a factum from the module located by the given path."""
        module = import_module(path)
        return getattr(module, "factum")

    _default_command_callback: Optional[Callable[..., Any]] = None

    def __init__(
        self,
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[TyperGroup]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        align_sections: Optional[bool] = Default(None),
        show_subcommand_aliases: Optional[bool] = Default(None),
        # Command
        aliases: Optional[Iterable[str]] = Default(None),
        section: Optional[cloup.Section] = Default(None),
        constraints: Sequence["BoundConstraintSpec"] = Default(()),
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        formatter_settings: Optional[Dict[str, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        align_option_groups: Optional[bool] = Default(None),
        show_constraints: Optional[bool] = Default(None),
        # Completion
        add_completion: bool = True,
    ):
        def check_cls(cls: Optional[Type]) -> None:
            if cls is not None and not issubclass(cls, FactumGroup):
                raise TypeError(
                    f"`{nameof(cls)}` is not `{FactumGroup.__name__}` or subclass"
                )

        if isinstance(cls, DefaultPlaceholder) and cls.value:
            check_cls(cls.value)  # pragma: no cover
        elif cls:
            check_cls(cls)

        resolved_context_settings = copy(self._default_context_settings)
        if context_settings:
            resolved_context_settings.update(context_settings)

        super().__init__(
            name=name,
            cls=cls or FactumGroup,
            invoke_without_command=invoke_without_command,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            align_sections=align_sections,
            show_subcommand_aliases=show_subcommand_aliases,
            aliases=aliases,
            section=section,
            constraints=constraints,
            context_settings=resolved_context_settings,
            formatter_settings=formatter_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            align_option_groups=align_option_groups,
            show_constraints=show_constraints,
            add_completion=add_completion,
        )

        @self.callback()
        def default_callback() -> None:
            pass

    def set_default(self, callback: Callable[..., Any]) -> None:
        """Set the default command, to be executed when no command is explicitly provided."""
        self._default_command_callback = callback
        callback.__factotum_is_default__ = True  # type: ignore

    def callback(
        self,
        name: Optional[str] = Default(None),
        *,
        cls: Optional[Type[TyperGroup]] = Default(None),
        invoke_without_command: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        aliases: Optional[Iterable[str]] = Default(None),
        constraints: Sequence["BoundConstraintSpec"] = Default(()),
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        formatter_settings: Optional[Dict[str, Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        no_args_is_help: bool = Default(False),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        align_option_groups: Optional[bool] = Default(None),
        show_constraints: Optional[bool] = Default(None),
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        """TODO"""

        def check_cls(cls: Optional[Type]) -> None:
            if cls is not None and not issubclass(cls, FactumGroup):
                raise TypeError(
                    f"`{nameof(cls)}` is not `{FactumGroup.__name__}` or subclass"
                )

        if isinstance(cls, DefaultPlaceholder) and cls.value:
            check_cls(cls.value)  # pragma: no cover
        elif cls:
            check_cls(cls)

        orig_decorator = super().callback(
            name,
            cls=cls or FactumGroup,
            invoke_without_command=True,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            aliases=aliases,
            constraints=constraints,
            context_settings=context_settings,
            formatter_settings=formatter_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            align_option_groups=align_option_groups,
            show_constraints=show_constraints,
        )

        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            import click

            @wraps(f)
            def callback(*args: Any, **kwargs: Any) -> Any:
                ctx = click.get_current_context()

                if invoke_without_command or ctx.invoked_subcommand is not None:
                    f(*args, **kwargs)

                if (
                    ctx.invoked_subcommand is None
                    and self._default_command_callback is not None
                ):
                    self.invoke(self._default_command_callback)

            return orig_decorator(cast(CommandFunctionType, callback))

        return decorator

    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[TyperCommand]] = None,
        aliases: Optional[Iterable[str]] = None,
        section: Optional[cloup.Section] = None,
        constraints: Sequence["BoundConstraintSpec"] = (),
        context_settings: Optional[Dict[Any, Any]] = None,
        formatter_settings: Optional[Dict[str, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        align_option_groups: Optional[bool] = None,
        show_constraints: Optional[bool] = None,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        """TODO"""

        def check_cls(cls: Optional[Type]) -> None:
            if cls is not None and not issubclass(cls, FactumCommand):
                raise TypeError(
                    f"`{nameof(cls)}` is not `{FactumCommand.__name__}` or subclass"
                )

        check_cls(cls)

        return super().command(
            name,
            cls=cls or FactumCommand,
            aliases=aliases,
            section=section,
            constraints=constraints,
            context_settings=context_settings,
            formatter_settings=formatter_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            align_option_groups=align_option_groups,
            show_constraints=show_constraints,
        )

    def add_sub(
        self,
        factum: Union["Typer", Union[str, PathLike]],  # type: ignore
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[TyperGroup]] = Default(None),
        invoke_without_command: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        aliases: Optional[Iterable[str]] = Default(None),
        section: Optional[cloup.Section] = Default(None),
        constraints: Sequence["BoundConstraintSpec"] = Default(()),
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        formatter_settings: Optional[Dict[str, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        no_args_is_help: bool = Default(False),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        align_option_groups: Optional[bool] = Default(None),
        show_constraints: Optional[bool] = Default(None),
    ) -> None:
        """TODO"""

        def check_cls(cls: Optional[Type]) -> None:
            if cls is not None and not issubclass(cls, FactumGroup):
                raise TypeError(
                    f"`{nameof(cls)}` is not `{FactumGroup.__name__}` or subclass"
                )

        if isinstance(cls, DefaultPlaceholder) and cls.value:
            check_cls(cls.value)  # pragma: no cover
        elif cls:
            check_cls(cls)

        if isinstance(factum, (str, PathLike)):
            factum = Factum.load(factum)

        return super().add_sub(
            factum,
            name=name,
            cls=cls or FactumGroup,
            invoke_without_command=invoke_without_command,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            aliases=aliases,
            section=section,
            constraints=constraints,
            context_settings=context_settings,
            formatter_settings=formatter_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            align_option_groups=align_option_groups,
            show_constraints=show_constraints,
        )


def verbose_option(help: str = "Write verbose output.") -> Any:
    """Create a CLI option for a "verbose" flag."""
    return typer.Option(
        False,
        "--verbose",
        "-v",
        help=help,
    )


def exit(code: int = 0) -> None:
    """Exit the factum immediately with the given process exit code."""
    raise typer.Exit(code)


def get_current_context(silent: bool = False) -> Optional[FactumContext]:
    """Return the current factum context. This can be used as a way to access the current context object from anywhere.

    :param silent: if set to `True` the return value is `None` if no context is available. The default behavior is to raise a :exc:`RuntimeError`.
    """
    ctx = click.get_current_context()

    assert isinstance(
        ctx, FactumContext
    ), f"current context is not {FactumContext.__name__}"
    return ctx


def import_module(path: Union[str, PathLike]) -> ModuleType:
    """Import the module located by the given path."""
    import importlib.machinery
    import importlib.util

    ctx = click.get_current_context()
    root_ctx = typer.Context.find_root(ctx)
    verbose = root_ctx.params["verbose"]

    if not isinstance(path, Path):
        path = PurePath(path)

    if run_path is not None:
        path = run_path.parent / path

    module_name = path.name

    if verbose:  # pragma: no cover
        typer.secho(f"Importing module from path `{path}`...", fg=colors.GREEN)

    spec = importlib.util.spec_from_loader(
        module_name,
        importlib.machinery.SourceFileLoader(module_name, str(path)),
    )
    assert spec is not None

    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    return module


run_path: Optional[Path] = None
