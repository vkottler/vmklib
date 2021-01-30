<!--
    =====================================
    generator=datazen
    version=1.3.0
    hash=7a321558fcf9457d6b68be49273939b1
    =====================================
-->

# vmklib

A collection of universal includes for setting up project workflows around
[GNU Make](https://www.gnu.org/software/make/).

This tool integrates with existing `Makefile`'s with zero additional
content or bootstrapping required.

There are many choices in technology or products for performing static
analysis on source code, building test infrastructure, or managing local
development environments. These are only a small subset of common, developer
tasks when building software. This package intends to aggregate recipes
(and their dependency relationships) for these tasks so that they can be
integrated into a project without re-building this infrastructure. Lessons
learned and improvements in each project can be back-propagated everywhere
else with simple package updates.

# Command-line Options

```
$ ./venv3.8/bin/mk -h

usage: mk [-h] [--version] [-v] [-C DIR] [-p PREFIX] [-f FILE] [-P PROJ]
          [targets [targets ...]]

Simplify project workflows by standardizing use of GNU Make.

positional arguments:
  targets               targets to execute

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set to increase logging verbosity
  -C DIR, --dir DIR     execute from a specific directory (default:
                        '/home/vkottler/Documents/git/workspace/vmklib')
  -p PREFIX, --prefix PREFIX
                        a prefix to apply to all targets
  -f FILE, --file FILE  file to source user-provided recipes from
  -P PROJ, --proj PROJ  project name for internal variable use

```

# Targets

Note that the full invocation for a target's command is:

```
mk [options] <prefix>-<command> [ARG1=val1 ARG2=val2]
```

## grip

Targets for rendering [GitHub Markdown](https://docs.github.com/en/rest/reference/markdown) with [grip](https://github.com/joeyespo/grip).


Prefix: `grip-`

### Optional Arguments

**SECRETHUB_GRIP_PATH** - The full path for the `secrethub read` command to source a [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) from, requires [secrethub](https://secrethub.io/).


**GRIP_PORT** - The `host:port` String to serve the rendered results on.

**GRIP_ENV** - Output file to write to for sourcing credentials.


### Commands

**check-env** - Checks that `GRIP_TOKEN` is set in the environment, errors if not.

**render** - Serve `README.md` with `grip`.


## pypi

Targets for uploading packages to [PyPI](https://pypi.org/).

Prefix: `pypi-`

### Optional Arguments

**UPLOAD_ENV** - Output file to write to for sourcing credentials.

**SECRETHUB_PYPI_PATH** - The full path for the `secrethub read` command to source a [PyPI API token](https://pypi.org/help/#apitoken) from, requires [secrethub](https://secrethub.io/).



### Commands

**check-env** - Enforces that `TWINE_USERNAME` and `TWINE_PASSWORD` are set in the environment, errors if not.


**upload** - Attempt to upload everything in `dist` to [PyPI](https://pypi.org/).


## datazen

Targets for use with the [datazen](https://pypi.org/project/datazen/) package.

Prefix: `dz-`

### Optional Arguments

**DZ_DIR** - Optionally override the `-C` argument.

**DZ_MANIFEST** - Optionally provide a non-default manifest file to `-m`.

**DZ_VERBOSE** - Setting this passes `-v`.


### Commands

**sync** - Run `dz`, executing the default target.

**clean** - Run `dz` with `-c` to clean the cache.

**describe** - Run `dz` with `-d` to describe cache contents.

**upgrade** - Upgrade `datazen` in the resolved virtual environment with `pip`.


## python

TODO

Prefix: `python-`

### Optional Arguments

**TODO** - TODO


### Commands

**lint** - TODO

**sa** - TODO

**test** - TODO

**view** - TODO

**host-coverage** - TODO

**all** - TODO

**clean** - TODO

**dist** - TODO

**upload** - TODO

**editable** - TODO
