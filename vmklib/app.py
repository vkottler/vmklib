"""
vmklib - This package's command-line entry-point application.
"""

# built-in
import argparse
from asyncio import set_event_loop
from contextlib import contextmanager, suppress
import logging
import os
from pathlib import Path
from platform import system
import subprocess
import tempfile
from typing import Callable, Dict, Iterator, List, Optional, Tuple, cast

# third-party
from vcorelib.dict import GenericStrDict
from vcorelib.io import ARBITER
from vcorelib.paths import find_file
from vcorelib.target import Substitutions
from vcorelib.task import TaskFailed
from vcorelib.task.manager import TaskManager

# internal
from vmklib import PKG_NAME
from vmklib.util import to_slug

LOG = logging.getLogger(__name__)
DEFAULT_FILE = Path("Makefile")


def project(path: Path, name: str = None) -> str:
    """
    If the project name wasn't provided, guess that it's either the name
    of the parent directory, or that name as a slug.
    """
    path = path.resolve()
    if name is None:
        parent_slug = to_slug(path.name)
        if path.joinpath(parent_slug).is_dir():
            name = parent_slug
        else:
            name = str(path.name)

    return name


@contextmanager
def build_makefile(
    user_file: Path,
    directory: Path,
    proj: str,
    data: GenericStrDict,
) -> Iterator[str]:
    """Build a temporary makefile and return the path."""

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w") as makefile:
        # build the necessary file data
        data["PROJ"] = proj
        data["$(PROJ)_DIR"] = cast(str, directory)
        data["MK_AUTO"] = 1
        data["$(PROJ)_MK_DIR"] = os.path.join(str(data["$(PROJ)_DIR"]), "mk")

        # get the path to this package's data to include our "conf.mk"
        include_strs = [
            "-include $($(PROJ)_MK_DIR)/init.mk",
            f"include {find_file('conf.mk', package=PKG_NAME)}",
            "-include $($(PROJ)_MK_DIR)/conf.mk",
        ]

        for key, item in data.items():
            makefile.write(f"{key} := {item}")
            makefile.write(os.linesep)
        for line in include_strs:
            makefile.write(line)
            makefile.write(os.linesep)

        makefile.write(os.linesep)

        # read the user's file
        with user_file.open(encoding="utf-8") as user_makefile:
            makefile.write(user_makefile.read())

        makefile.flush()
        yield makefile.name


#
# A function from an external module that's given:
#
# - project name
# - working directory (not necessarily the current one)
# - task manager to register tasks to
#
TaskRegister = Callable[[TaskManager, str, Path, Dict[str, str]], bool]


def initialize_task_manager(
    manager: TaskManager,
    proj: str,
    task_register: str,
    directory: Path,
    substitutions: Substitutions,
) -> None:
    """Load internal and external tasks to the task manager."""

    # register task-manager targets from this package
    conf = find_file("lib_tasks", "conf.py", package=PKG_NAME)
    assert conf is not None
    assert manager.script(
        conf, "register", proj, directory, substitutions
    ), "Couldn't register package tasks from '{get_resource(task_register)}'!"

    # register task-manager targets for the project
    proj_tasks = directory.joinpath(task_register)
    if proj_tasks.is_file():
        assert manager.script(
            proj_tasks,
            "register",
            proj,
            directory,
            substitutions,
        ), "Couldn't register project tasks from '{proj_tasks}'!"


def get_data(
    path: Path, targets: List[str], prefix: Optional[str] = None
) -> Tuple[Substitutions, List[str]]:
    """Load configuration data if it can be found."""

    # load configuration data, if configuration data is found
    data = {}
    if path.is_file():
        data = ARBITER.decode(path, require_success=True).data

    target_args = []
    for target in targets:
        # If an argument has an equal sign, treat it as a substitution and
        # environment variable to set.
        if "=" in target:
            key, val = target.split("=", maxsplit=1)
            data[key] = val
            os.environ[key] = val
            continue

        target_args.append(target)

    # build the list of targets to execute
    targets = target_args
    target_args = []
    for target in targets:
        target_str = target
        if prefix and "=" not in target_str:
            target_str = f"{prefix}-{target_str}"
        target_args.append(target_str)

    return cast(Substitutions, data), target_args


def entry(args: argparse.Namespace) -> int:
    """Execute the requested task."""

    if not args.file.is_file():
        if args.file.name != str(DEFAULT_FILE):
            LOG.error("'%s' not found", args.file)
            return 1
        args.file = find_file("data", "header.mk", package=PKG_NAME)

    # Add the default target early if nothing was specified.
    if not args.targets and args.default:
        args.targets.append(args.default)

    # load configuration data, if configuration data is found
    substitutions, targets = get_data(args.config, args.targets, args.prefix)

    proj = project(args.dir, args.proj)
    task_register = os.path.join("tasks", "conf.py")

    manager = TaskManager()
    set_event_loop(manager.eloop)
    initialize_task_manager(
        manager, proj, task_register, args.dir, substitutions
    )

    retcode = 1

    # execute tasks handled by the task manager
    try:
        unresolved = manager.execute(targets, **substitutions)
    except TaskFailed as exc:
        print(exc)
        manager.eloop.close()
        return retcode

    # Handle Make targets if it makes sense to run make.
    if unresolved and not args.disable_make:
        invocation_args = ["make", "-C", str(args.dir), "-f"]
        with build_makefile(
            args.file, args.dir, proj, substitutions
        ) as makefile:
            invocation_args.append(makefile)
            invocation_args += list(unresolved)
            LOG.debug(invocation_args)
            try:
                with suppress(KeyboardInterrupt):
                    result = subprocess.run(invocation_args, check=True)
                    retcode = result.returncode
            except subprocess.CalledProcessError as exc:
                retcode = exc.returncode

    # Set the return code to zero if all targets were resolved.
    elif not unresolved:
        retcode = 0
    else:
        print(
            f"The following targets were not resovled: {', '.join(unresolved)}"
        )

    return retcode


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """Add application-specific arguments to the command-line parser."""

    parser.add_argument("targets", nargs="*", help="targets to execute")
    parser.add_argument(
        "-p", "--prefix", default="", help="a prefix to apply to all targets"
    )
    parser.add_argument(
        "-d",
        "--disable-make",
        default=system() == "Windows",
        action="store_true",
        help=(
            "whether or not to allow GNU Make "
            "target resolution (default: '%(default)s')"
        ),
    )
    parser.add_argument(
        "-D",
        "--default",
        default="all",
        help=(
            "default target to make if none is "
            "specified (default: '%(default)s')"
        ),
    )
    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_FILE,
        type=Path,
        help=(
            "file to source user-provided recipes from "
            "(default: '%(default)s')"
        ),
    )
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_FILE.parent.joinpath(f"{PKG_NAME}.json"),
        type=Path,
        help=(
            "file to source user-provided variable definitions, ahead of "
            "loading package makefiles (default: '%(default)s')"
        ),
    )
    parser.add_argument(
        "-P", "--proj", type=str, help="project name for internal variable use"
    )
