<!--
    =====================================
    generator=datazen
    version=1.2.1
    hash=f455d448e3b84c87b53d15f7c13b0642
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

TODO: we need `datazen` support for capturing the `-h` / `--help` output to
fill this in.

# Targets

Note that the full invocation for a target's command is:

```
mk [options] <prefix>-<command> [ARG1=val1 ARG2=val2]
```

## datazen

*Targets for use with the [datazen](https://pypi.org/project/datazen/) package.*

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
