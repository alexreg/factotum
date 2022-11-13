# Factotum: *do everything*

**Factotum is a generic task runner and build tool based on Python scripting.**

No DSL to learn, no strange execution model. Just simple Python.

A Factotum script (*factum*), or a set of tasks, is nothing more than a Python module that imports `factotum`. You define your tasks as functions and structure them like a CLI application. Factotum itself then gives you a user-friendly CLI for executing everything.

## Philosophy

Most task runners and build tools employ some sort of domain-specifc language that makes it easy to do things its designers had in mind, but awkward or even impossible to do anything else. Naturally, such software increases in complexity over time, as support for new scenarios and configurations is added. This tends to give rise to monstrosities of cumbersome syntax, unintuitive semantics, and manifold edge cases and bugs. One ends up with all of the vices and none of the virtues of a general-purpose programming language.

We cut to the chase and embrace the idea that a powerful and ergonomic task runner should at its heart be a general-purpose programming language. Except we ensure it's a first-rate scripting language by founding everything upon Python. Internally, we leverage the [typer-cloup] library for building CLI applications in order to provide a straightforward yet flexible and composable way to define tasks.

## Examples

```python
#!/usr/bin/env factotum-script
from factotum import *

factum = Factum(help="Sample script")


@factum.command()
def hello(name: str = "World", formal: bool = False):
    """Say hello"""
    if formal:
        echo(f"Good day, {name}")
    else:
        echo(f"Hello {name}")


@factum.command()
def bye(friend: bool = False):
    """Say bye"""
    if friend:
        echo("Goodbye, my friend")
    else:
        echo("Goodbye")
```

[typer-cloup]: https://github.com/alexreg/typer-cloup
