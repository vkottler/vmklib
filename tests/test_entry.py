"""
vmklib - Test the program's entry-point.
"""

# built-in
from multiprocessing import Process
import os
import signal
from subprocess import check_output
from sys import executable
import time

# third-party
from vcorelib.task.subprocess.run import is_windows

# internal
from tests import build_cleaned_resource, get_args, get_resource

# module under test
from vmklib import PKG_NAME
from vmklib.entry import main as mk_main


def test_interrupt():
    """Test interrupting the process."""

    with get_args() as base_args:
        good_base_args = base_args + ["-f", get_resource("Makefile"), "sleep"]
        proc = Process(target=mk_main, args=[good_base_args])
        proc.start()
        time.sleep(0.5)
        os.kill(proc.pid, signal.SIGINT)
        proc.join()


def test_entry():
    """Test some basic command-line argument scenarios."""

    if not is_windows():
        with get_args() as base_args:
            good_base_args = base_args + ["-f", get_resource("Makefile")]
            assert mk_main(good_base_args + ["test"]) == 0
            assert mk_main(good_base_args + ["--proj", "test", "test"]) == 0
            assert mk_main(good_base_args + ["-p", "prefix", "test"]) == 0
            assert mk_main(good_base_args + ["test_bad"]) != 0
            assert mk_main(good_base_args + ["--weird-option", "yo"]) != 0
            assert mk_main(base_args + ["-f", "nah"]) != 0
            assert mk_main(base_args) == 0


def test_package_entry():
    """Test the command-line entry through the 'python -m' invocation."""

    with get_args() as base_args:
        args = [executable, "-m"] + base_args
        check_output(args)


def test_entry_proj_slug():
    """Ensure that the slug-replacement logic takes effect."""

    if not is_windows():
        assert (
            mk_main([PKG_NAME, "-C", get_resource("test-scenario"), "test"])
            == 0
        )


def test_entry_python_tasks():
    """Ensure that we can run Python-based tasks."""

    with build_cleaned_resource("python-tasks") as test_dir:
        for _ in range(2):
            assert mk_main([PKG_NAME, "-C", test_dir, "-d", "venv"]) == 0

        for _ in range(2):
            assert (
                mk_main(
                    [PKG_NAME, "-C", test_dir, "-d", "python-install-yamllint"]
                )
                == 0
            )

        targets = [
            (
                "python-lint python-sa"
                f"{' yaml-lint-manifest.yaml' if not is_windows() else ''} "
                "python-build-once"
            ),
            "python-build",
            "python-test",
            "python-test-add",
            "dz-sync",
        ]
        for target in targets:
            assert (
                mk_main([PKG_NAME, "-C", test_dir, "-d", *target.split()]) == 0
            )

        assert mk_main([PKG_NAME, "-C", test_dir, "-d", "asdf"]) != 0
        assert mk_main([PKG_NAME, "-C", test_dir, "-d", "fail"]) != 0
