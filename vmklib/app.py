"""
vmklib - This package's command-line entry-point application.
"""

# built-in
import argparse
from contextlib import contextmanager
import logging
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Iterator

# third-party
import pkg_resources

LOG = logging.getLogger(__name__)
DEFAULT_FILE = Path("Makefile")


def get_resource(resource_name: str) -> Path:
    """Locate the path to a package resource."""

    resource_path = os.path.join("data", resource_name)

    locations = [
        pkg_resources.resource_filename(__name__, resource_path),
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), resource_path
        ),
    ]

    resource = ""
    for location in locations:
        if os.path.isfile(location):
            resource = location
            break

    # ensure that the resource can actually be found
    assert resource, f"Couldn't load resource '{resource_name}'!"
    return Path(resource)


@contextmanager
def build_makefile(
    user_file: Path, directory: Path, project_name: str = None
) -> Iterator[str]:
    """Build a temporary makefile and return the path."""

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w") as makefile:
        # read the user's file
        with user_file.open(encoding="utf-8") as user_makefile:
            user_data = user_makefile.read()

        # get the path to this package's data to include our "conf.mk"
        include_str = f"include {get_resource('conf.mk')}"

        # if the project name wasn't provided, guess that it's either the name
        # of the parent directory, or that name as a "slug"
        if project_name is None:
            parent = user_file.resolve().parent
            parent_slug = parent.name.replace("-", "_")
            if Path(parent, parent_slug).is_dir():
                project_name = parent_slug
            else:
                project_name = str(parent)

        # build the necessary file data
        data = {
            "PROJ": os.path.basename(project_name),
            "$(PROJ)_DIR": str(directory),
            "MK_AUTO": "1",
        }

        write_data = ""
        for key, item in data.items():
            write_data += f"{key} := {item}" + os.linesep
        write_data += include_str + os.linesep + os.linesep + user_data

        # write the file and return the path
        makefile.write(write_data)
        makefile.flush()
        yield makefile.name


def entry(args: argparse.Namespace) -> int:
    """Execute the requested task."""

    if not args.file.is_file():
        if args.file.name != str(DEFAULT_FILE):
            LOG.error("'%s' not found", args.file)
            return 1
        args.file = get_resource(os.path.join("data", "header.mk"))

    # build the beginning of the invocation args
    invocation_args = ["make", "-C", str(args.dir), "-f"]
    with build_makefile(args.file, args.dir, args.proj) as makefile:
        invocation_args.append(makefile)

        # add each target to the list
        for target in args.targets:
            target_str = target
            if args.prefix and "=" not in target_str:
                target_str = f"{args.prefix}-{target_str}"
            invocation_args.append(target_str)

        # start the process
        LOG.debug(invocation_args)
        try:
            result = subprocess.run(invocation_args, check=True)
            retcode = result.returncode
        except subprocess.CalledProcessError as exc:
            retcode = exc.returncode
        except KeyboardInterrupt:
            retcode = 1

    return retcode


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """Add application-specific arguments to the command-line parser."""

    parser.add_argument("targets", nargs="*", help="targets to execute")
    parser.add_argument(
        "-p", "--prefix", default="", help="a prefix to apply to all targets"
    )
    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_FILE,
        type=Path,
        help="file to source user-provided recipes from",
    )
    parser.add_argument(
        "-P", "--proj", help="project name for internal variable use"
    )
