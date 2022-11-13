# `multiapp`

Demo App

**Usage**:

```console
$ multiapp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-h, --help`: Show this message and exit.

The end

**Commands**:

* `sub`
* `top`: Top command

## `multiapp sub`

**Usage**:

```console
$ multiapp sub [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-h, --help`: Show this message and exit.

**Commands**:

* `bye`: Say bye
* `hello`: Say Hello
* `hi`: Say hello

### `multiapp sub bye`

Say bye

**Usage**:

```console
$ multiapp sub bye [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

### `multiapp sub hello`

Say Hello

**Usage**:

```console
$ multiapp sub hello [OPTIONS]
```

**Options**:

* `--name TEXT`: [default: World]
* `--age INTEGER`: The age of the user  [default: 0]
* `-h, --help`: Show this message and exit.

### `multiapp sub hi`

Say hello

**Usage**:

```console
$ multiapp sub hi [OPTIONS] [USER]
```

**Arguments**:

* `[USER]`: The name of the user to greet  [default: World]

**Options**:

* `-h, --help`: Show this message and exit.

## `multiapp top`

Top command

**Usage**:

```console
$ multiapp top [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.
