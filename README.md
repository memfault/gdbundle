# GDBundle - Plugin Manager for GDB and LLDB

[![PyPI version](https://badge.fury.io/py/gdbundle.svg)](https://badge.fury.io/py/gdbundle)

gdbundle is short for GDB bundle and is a plugin manager for GDB and LLDB.

For detailed info about the origin story of gdbundle, read the announcement on Interrupt: 
[gdbundle - GDB's Missing Plugin Manager](https://interrupt.memfault.com/blog/gdbundle-plugin-manager)

## Benefits

There are a handful of indisputable benefits of using gdbundle over manually modifying `.gdbinit` and `.lldbinit` files.

1. Just `pip install gdbundle-<plugin-name>`. No more manually editing your
   `~/.gdbinit` in specific ways depending on the extension.
2. It enables developers to use virtual environments (and encourages it!).
3. Personal projects and team projects can have project-specific
   `requirements.txt` and `.gdbinit` files. With these two in place, a new
   developer would just need to `pip install -r requirements.txt`.
4. Discoverability. Check out this
   [PyPi filter](https://pypi.org/search/?q=gdbundle) to find new plugins.
5. Dependency management and version tracking is now done automatically by
   Python's packaging infrastructure.

## Published Plugins

Published ones can be found on [PyPi](https://pypi.org/search/?q=gdbundle)

For now, a list is kept here as well:

- [example](https://github.com/memfault/gdbundle-example)
- [gdb-dashboard](https://github.com/memfault/gdbundle-gdb-dashboard)
- [PyCortexMDebug](https://github.com/memfault/gdbundle-PyCortexMDebug)
- [voltron](https://github.com/memfault/gdbundle-voltron)

## Quickstart

> NOTE: The Python compiled with GDB should be the same major version as 
> the Python in the local virtual, Conda, or local environment that 
> you are installing gdbundle and plugins into. 

To check both versions of Python, you can run the following:

```
$ gdb
(gdb) pi
>>> import sys; sys.version
'3.6.9 (default, Nov  7 2019, 10:44:02) \n[GCC 8.3.0]'

$ python --version
Python 3.6.9
```

### Install gdbundle

Install `gdbundle` from PyPi first. Using a
[virtual environment](https://docs.python.org/3/library/venv.html) is
recommended.

```
$ pip install gdbundle
```

If you'd rather not use a virtual environment, it's advised to use `--user` when
installing the package.

```
$ pip install --user gdbundle
```

Just, whatever you do, don't use `sudo ...`. And don't let your friends either.

### Amend Init Scripts

Placing the following in the appropriate file will load all installed gdbundle
plugins by default. If you would like to selectively load certain ones, please
refer to the [Configuration](#Configuration) section.

#### GDB's `.gdbinit`

Append the following to your `~/.gdbinit` or to a project-specific `.gdbinit`
that is loaded with `gdb --command .gdbinit`

```
# -- gdbundle_BEGIN
python
import os,sys,subprocess
# Execute a Python using the user's shell and pull out the sys.path (for site-packages)
paths = subprocess.check_output('python -c "import os,sys;print(os.linesep.join(sys.path).strip())"',shell=True).decode("utf-8").split()
# Extend GDB's Python search path
sys.path.extend(paths)

# Initialize gdbundle
import gdbundle
gdbundle.init()
end
# -- gdbundle_END
```

#### LLDB's `.lldbinit`

Copy the `sample_lldbinit.py` somewhere. For now, let's assume it's at
`/path/to/gdbundle_lldbinit.py`

```
# /path/to/gdbundle_lldbinit.py

# -- gdbundle_BEGIN
import os,subprocess,sys
# Execute a Python using the user's shell and pull out the sys.path (for site-packages)
paths = subprocess.check_output('python -c "import os,sys;print(os.linesep.join(sys.path).strip())"',shell=True).decode("utf-8").split()
# Extend LLDB's Python search path
sys.path.extend(paths)

# Initialize gdbundle
import gdbundle
gdbundle.init()
# -- gdbundle_END
```

Append the following to your `~/.lldbinit` or to project-specific `.lldbinit`
file that is loaded with `lldb -s .lldbinit`.

```
# .lldbinit

command script import '/path/to/gdbundle_lldbinit.py'
```

## Background

GDB has
[built-in support for extensions](https://sourceware.org/gdb/current/onlinedocs/gdb/Extending-GDB.html#Extending-GDB)
written in in Python, Guile, or GDB's command language. However, there is no
convenient way to package, distribute, and install these scripts.

GDB does provide a few mechanisms:

- Place scripts in /usr/local/share/gdb/auto-load or similar
- Use `gdb --command ...` to load the scripts on invocation
-

GDB's documentation gives us the following:

> Python scripts used by GDB should be installed in data-directory/python, where
> data-directory is the data directory as determined at GDB startup

This leaves a lot to be desired, because a user would have to copy-paste script
files to this directory. There are many drawbacks to this method, including:

- Requires manual intervention to install scripts to `data-directory`
- Scripts become out of date since they were copy-pasted
- `data-directory` is usually in a directory next to GDB's installation path,
  usually in `/usr/local`. Everyone should do their best not to manually edit
  files there.

There _has_ to be a better way, and thankfully, there is! It's called
`gdbundle`.

## Installing Packages

Packages are prefixed with `gdbundle-` and are installing through `pip` from
PyPi.

```
$ pip install gdbundle-example
```

## Configuration

`gdbundle` today is simple and has only a few configuration knobs. Configuration
is passed into the `gdbundle.init(...)` function call.

> NOTE: The names passed into `include` and `exclude` should be the package name
> minus `gdbundle_`, and hyphens are underscores. (e.g. `gdbundle-gdb-dashboard`
> becomes `gdb_dashboard`)

```py
# .gdbinit

import gdbundle

# Configure which packages to include
include = [
    # List of packages to load.
    # e.g. "example"
]

exclude = [
    # List of packages to exclude.
    # Useful if the same virtual environment is used for multiple
    #  projects and not all packages should be loaded
    # e.g. "example"
]
# Load the configured packages
gdbundle.init(include=include, exclude=exclude)
```

If you've created a Python package that has the necessary gdbundle hooks (e.g.
`gdbundle.gdb_loader.gdbundle_load()`), you can manually load it using
`gdbundle.load_module()`.

```
# gdbundle will import this module and attempt to run `my_package.gdb_loader.gdbundle_load()`
gdbundle.load_module("my_package")
```

## Creating and Distributing Packages

The goal was to keep `gdbundle` packages as simple as possible. A package only
has a few responsibilities:

1. Define dependencies in the `pyproject.toml` so they are automatically
   installed.
2. Provide a version so users can easily pin and upgrade to specific versions.
3. Provide a hook `gdb_loader.gdbundle_load()` and/or
   `lldb_loader.gdbundle_load()` which is called by gdbundle, which should
   either:
   - Load the script into the debugger context by calling
     `gdb.execute("source <file>")` or
     `lldb.debugger.HandleCommand("command script import <file>"`
   - Import the Python module which does the sourcing itself:
     `from mypackage import HelloWorld; HelloWorld()`

To investigate a real package that works with both GDB and LLDB, check out the
[gdbundle-example plugin](https://github.com/memfault/gdbundle-example).

Let's go over each piece quickly.

### `pyproject.toml`

A standard `setup.py` file. The main thing to note here is that our package
`name` will be `gdbundle-<something>`, but our Python package will be called
`gdbundle_<something>`.

```python
[tool.poetry]
name = "gdbundle-example"
version = "0.0.1"
description = ""
authors = ["Tyler Hoffman <tyler@memfault.com>"]
readme = "README.md"
include = ["gdbundle_example/scripts/*"]
license = "MIT"
classifiers = [
    [...]
]

[tool.poetry.dependencies]
python = "*"

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"

```

### `gdbundle_example/gdb_loader.py`

```python
import gdb
import os

PACKAGE_DIR = os.path.dirname(__file__)

SCRIPT_PATHS = [
    [PACKAGE_DIR, 'scripts', 'example_gdb.gdb'],
    [PACKAGE_DIR, 'scripts', 'example_gdb.py']
]

def _abs_path(path):
    return os.path.abspath(os.path.join(*path))

def gdbundle_load():
    for script_path in SCRIPT_PATHS:
        gdb.execute("source {}".format(_abs_path(script_path)))
```

### `gdbundle_example/scripts/`

Place the script files here!

## How It Works

If the GDB/LLDB executable you are using was downloaded rather than compiled
from source, it's likely that it is linked against a system Python library and
`site-packages` directory, rather than against a virtual environment, Conda
environment, or another user installed version of Python.

For example, if we start `arm-none-eabi-gdb-py` downloaded from
[ARM](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain),
we'll see that it is searching within the system Python's `site-packages` folder
for packages:

```
$ arm-none-eabi-gdb-py
(gdb) python-interactive
>>> import sysconfig
>>> sysconfig.get_paths()['purelib']
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages'
```

Similar with LLDB:

```
$ lldb
(lldb) script
Python Interactive Interpreter. To exit, type 'quit()', 'exit()' or Ctrl-D.
>>> import sysconfig; sysconfig.get_paths()['purelib']
'/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.7/lib/python3.7/site-packages'

```

When a user installs packages with an `apt` or `brew` Python, or one from a
Conda or virtual environment, GDB will **not** automatically find those packages
since Python's configured `sys.path` is only looking in the system's
`site-packages` folder.

There are three recommended (but _very bad_) ways to handle this:

- Override `PYTHONPATH` on init or in the users shell.
- Create sym-links between the virtual environment and the system python
  installation.
- Deal with it, as said in LLDB's
  [Python Caveat](https://lldb.llvm.org/resources/caveats.html) docs. Install
  the packages in the same installation anyways.

We want something that edits _only_ GDB's Python context, and only appends to
Python's `sys.path`, not overrides it.

The best solution I've found and have been using (along with 100 other engineers
at my previous employer) is to shell out from within GDB, ask the local shell
environment what the configured Python executable is, get its `sys.path`
entries, and then append those to our current GDB session's Python environment.
This allows GDB to find and use packages that are installed into a Conda or
virtualenv environment, as well as any other user installed Python environment.

## Who uses GDB Python Scripts

Many companies and projects use and include GDB scripts with their large
open-source projects. They are usually buried in the repo, difficult to source,
and built and used in various ways. They usually require the developer to
discover that they exist, manually source them, and then look at the source code
to figure out how they work.

Check out the gdbundle announcement for a list of ones that are public and
open-source.

[Neat GDB Script Repositories](https://interrupt.memfault.com/blog/gdbundle-plugin-manager#neat-gdb-script-repositories)
