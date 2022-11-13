from os import PathLike
from pathlib import Path, PurePath
from types import ModuleType
from typing import *

import click
import cloup
import typer_cloup as typer
from typer_cloup import Typer, colors
from typer_cloup.core import TyperArgument, TyperOption
from typer_cloup.main import TyperCommand, TyperGroup
from typer_cloup.models import CommandFunctionType, Default, DefaultPlaceholder
from varname import nameof

if TYPE_CHECKING:  # pragma: no cover
    from cloup.constraints import BoundConstraintSpec

    F = TypeVar("F", bound=Callable)

    def cache(f: F) -> F:
        pass

else:
    from functools import cache


T = TypeVar("T")


class FactotumError(Exception):
    pass


class FactumContext(typer.Context):
    def __init__(
        self,
        # click.Context
        command: "click.Command",
        parent: Optional["click.Context"] = None,
        info_name: Optional[str] = None,
        obj: Optional[Any] = None,
        auto_envvar_prefix: Optional[str] = None,
        default_map: Optional[Dict[str, Any]] = None,
        terminal_width: Optional[int] = None,
        max_content_width: Optional[int] = None,
        resilient_parsing: bool = False,
        allow_extra_args: Optional[bool] = None,
        allow_interspersed_args: Optional[bool] = None,
        ignore_unknown_options: Optional[bool] = None,
        help_option_names: Optional[List[str]] = None,
        token_normalize_func: Optional[Callable[[str], str]] = None,
        color: Optional[bool] = None,
        show_default: Optional[bool] = None,
        # cloup.Context
        align_option_groups: Optional[bool] = None,
        align_sections: Optional[bool] = None,
        show_subcommand_aliases: Optional[bool] = None,
        show_constraints: Optional[bool] = None,
        check_constraints_consistency: Optional[bool] = None,
        formatter_settings: Dict[str, Any] = {},
    ):
        auto_envvar_prefix = ""

        super().__init__(
            command=command,
            parent=parent,
            info_name=info_name,
            obj=obj,
            auto_envvar_prefix=auto_envvar_prefix,
            default_map=default_map,
            terminal_width=terminal_width,
            max_content_width=max_content_width,
            resilient_parsing=resilient_parsing,
            allow_extra_args=allow_extra_args,
            allow_interspersed_args=allow_interspersed_args,
            ignore_unknown_options=ignore_unknown_options,
            help_option_names=help_option_names,
            token_normalize_func=token_normalize_func,
            color=color,
            show_default=show_default,
            align_option_groups=align_option_groups,
            align_sections=align_sections,
            show_subcommand_aliases=show_subcommand_aliases,
            show_constraints=show_constraints,
            check_constraints_consistency=check_constraints_consistency,
            formatter_settings=formatter_settings,
        )

    @cache
    def find_root(self) -> "FactumContext":
        """Find the outermost factum context."""
        node: Optional["click.Context"] = self

        while node is not None:
            if isinstance(node, FactumContext) and getattr(node, "_is_root", False):
                return node

            node = node.parent

        raise FactotumError("root context not found")  # pragma: no cover

    @overload
    def param(self, name: str) -> Any:
        ...

    @overload
    def param(self, name: str, typ: Type[T]) -> T:
        ...

    @cache
    def param(self, name: str, typ: Optional[Type[T]] = None) -> T | Any:
        """Return the value of the given parameter in the hierarchy of factum contexts."""
        node: Optional["click.Context"] = self

        while node is not None:
            try:
                return node.params[name]
            except KeyError:
                pass

            if isinstance(node, FactumContext) and getattr(node, "_is_root", False):
                raise KeyError

            node = node.parent

        raise FactotumError("root context not found")  # pragma: no cover

    def invoke(
        __self,
        __callback: Union["click.Command", Callable[..., Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if cli_verbose():
            command = None
            if isinstance(__callback, click.Command):
                command = __callback
            else:
                command_info = getattr(__callback, "_command_info", None)
                if command_info is not None:
                    command = typer.main.get_command_from_info(command_info)

            if getattr(__self, "_is_root", False):
                typer.secho(f"Invoking root command...", fg=colors.GREEN)
            else:
                assert command is not None
                typer.secho(f"Invoking command `{command.name}`...", fg=colors.GREEN)

        return super().invoke(__callback, *args, **kwargs)

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

    def invoke(self, ctx: click.Context) -> Any:
        if cli_verbose():
            if getattr(ctx, "_is_root", False):
                typer.secho(f"Running root command...", fg=colors.GREEN)
            else:
                typer.secho(f"Running command `{self.name}`...", fg=colors.GREEN)

        return super().invoke(ctx)


class FactumGroup(FactumCommand, TyperGroup):
    pass


class FactumArgument(TyperArgument):
    def __init__(
        self,
        *,
        param_decls: List[str],
        type: Optional[Any] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        convertor: Optional[Any] = None,
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
    ):
        super().__init__(
            param_decls=param_decls,
            type=type,
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
            convertor=convertor,
            show_default=show_default,
            show_choices=show_choices,
            show_envvar=show_envvar,
            allow_from_autoenv=allow_from_autoenv,
            help=help,
            hidden=hidden,
        )


class FactumOption(TyperOption):
    def __init__(
        self,
        param_decls: List[str],
        type: Optional[Union[click.types.ParamType, Any]] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        convertor: Optional[Any] = None,
        show_default: Union[bool, str] = False,
        prompt: Union[bool, str] = False,
        confirmation_prompt: Union[bool, str] = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        group: Optional[cloup.OptionGroup] = None,
    ):
        super().__init__(
            param_decls=param_decls,
            type=type,
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
            convertor=convertor,
            show_default=show_default,
            prompt=prompt_required,
            confirmation_prompt=confirmation_prompt,
            prompt_required=prompt_required,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
            group=group,
        )


class Factum(Typer):
    """A factum: a CLI interface for a set of tasks."""

    default_context_settings: ClassVar[Dict[str, Any]] = typer.Context.settings(
        auto_envvar_prefix="",
        formatter_settings=cloup.HelpFormatter.settings(
            col1_max_width=40,
        ),
        help_option_names=["--help", "-h"],
        max_content_width=100,
    )

    @staticmethod
    def load(path: Union[str, PathLike]) -> "Factum":
        """Load a factum from the module located by the given path."""
        module = import_module(path)
        return getattr(module, "factum")

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

        context_settings = {
            **self.default_context_settings,
            **(context_settings or {}),
        }

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
            add_completion=add_completion,
        )

        @self.callback()
        def default_callback() -> None:
            pass

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
        def check_cls(cls: Optional[Type]) -> None:
            if cls is not None and not issubclass(cls, FactumGroup):
                raise TypeError(
                    f"`{nameof(cls)}` is not `{FactumGroup.__name__}` or subclass"
                )

        if isinstance(cls, DefaultPlaceholder) and cls.value:
            check_cls(cls.value)  # pragma: no cover
        elif cls:
            check_cls(cls)

        return super().callback(
            name,
            cls=cls or FactumGroup,
            invoke_without_command=invoke_without_command,
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


def is_entry_point() -> bool:
    import sys

    return sys._getframe(1).f_globals.get("__entry_point__", False)


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


def get_current_context(silent: bool = False) -> FactumContext:
    """Return the current factum context. This can be used as a way to access the current context object from anywhere.

    :param silent: if set to `True` the return value is `None` if no context is available. The default behavior is to raise a :exc:`RuntimeError`.
    """
    ctx = click.get_current_context()

    assert isinstance(
        ctx, FactumContext
    ), f"current context is not {FactumContext.__name__}"
    return ctx


@cache
def cli_verbose() -> Optional[bool]:
    ctx = click.get_current_context(silent=True)
    if ctx is None:
        return None

    root_ctx = typer.Context.find_root(ctx)
    if root_ctx is None:
        return None

    return root_ctx.params["verbose"]


@overload
def param(name: str) -> Any:
    ...


@overload
def param(name: str, typ: Type[T]) -> T:
    ...


@cache
def param(name: str, typ: Optional[Type[T]] = None) -> T | Any:
    """Return the value of the given parameter in the hierarchy of factum contexts."""
    return get_current_context().param(name)


def import_module(path: Union[str, PathLike]) -> ModuleType:
    """Import the module located by the given path."""
    import importlib.machinery
    import importlib.util

    if not isinstance(path, Path):
        path = PurePath(path)

    if run_path is not None:
        path = run_path.resolve().parent / path

    module_name = path.name

    if cli_verbose():  # pragma: no cover
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
