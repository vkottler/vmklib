
"""
vmklib - This package's command-line entry-point application.
"""

# built-in
import argparse
import logging
import os
import subprocess
import tempfile

# third-party
import pkg_resources

LOG = logging.getLogger(__name__)
DEFAULT_FILE = "Makefile"


def get_resource(resource_name: str) -> str:
    """ Locate the path to a package resource. """

    resource_path = os.path.join("data", resource_name)
    return pkg_resources.resource_filename(__name__, resource_path)


def build_makefile(user_file: str, directory: str,
                   project_name: str = None) -> str:
    """ Build a temporary makefile and return the path. """

    # create a temporary file
    makefile = tempfile.NamedTemporaryFile(mode="w", delete=False)

    # read the user's file
    with open(user_file) as user_makefile:
        user_data = user_makefile.read()

    # get the path to this package's data to include our "conf.mk"
    include_str = "include {}".format(get_resource("conf.mk"))

    # build the necessary file data
    if project_name is None:
        project_name = os.path.dirname(os.path.abspath(user_file))
    data = {"PROJ": os.path.basename(project_name),
            "$(PROJ)_DIR": directory,
            "MK_AUTO": "1"}

    write_data = ""
    for key, item in data.items():
        write_data += "{} := {}".format(key, item) + os.linesep
    write_data += include_str + os.linesep + os.linesep + user_data

    # write the file and return the path
    makefile.write(write_data)
    return makefile.name


def entry(args: argparse.Namespace) -> int:
    """ Execute the requested task. """

    if not os.path.isfile(args.file):
        if os.path.basename(args.file) != DEFAULT_FILE:
            LOG.error("'%s' not found", args.file)
            return 1
        args.file = get_resource(os.path.join("data", "header.mk"))

    # build the beginning of the invocation args
    invocation_args = ["make", "-C", args.dir, "-f"]
    makefile = build_makefile(args.file, args.dir, args.proj)
    invocation_args.append(makefile)

    # add each target to the list
    for target in args.targets:
        target_str = target
        if args.prefix and "=" not in target_str:
            target_str = "{}-{}".format(args.prefix, target_str)
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
    finally:
        os.remove(makefile)

    return retcode


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """ Add application-specific arguments to the command-line parser. """

    parser.add_argument("targets", nargs="*", help="targets to execute")
    parser.add_argument("-p", "--prefix", default="",
                        help="a prefix to apply to all targets")
    parser.add_argument("-f", "--file", default=DEFAULT_FILE,
                        help="file to source user-provided recipes from")
    parser.add_argument("-P", "--proj",
                        help="project name for internal variable use")
