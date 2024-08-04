"""
vmklib - Test the program's entry-point.
"""

# built-in
from contextlib import ExitStack, contextmanager, suppress
from multiprocessing import Process
import os
import signal
from subprocess import check_output
from sys import executable
import time
from typing import Iterator, List, Set

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
        assert isinstance(proc.pid, int)
        with suppress(PermissionError):
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

            assert mk_main(good_base_args) == 0

            # Shouldn't be able to resolve the default target.
            assert mk_main(base_args) != 0


def test_package_entry():
    """Test the command-line entry through the 'python -m' invocation."""

    with get_args() as base_args:
        args = [executable, "-m"] + base_args + ["--default", ""]
        check_output(args)


def test_entry_proj_slug():
    """Ensure that the slug-replacement logic takes effect."""

    if not is_windows():
        assert (
            mk_main([PKG_NAME, "-C", get_resource("test-scenario"), "test"])
            == 0
        )


def target_test(
    target: str,
    test_dir: str,
    should_pass: bool = True,
    relevant: bool = True,
) -> None:
    """Test a single target string."""

    result = mk_main([PKG_NAME, "-C", test_dir, "-d", *target.split()])
    if relevant:
        assert result == 0 if should_pass else result != 0


@contextmanager
def target_tests(
    scenario: str,
    passes: List[str],
    fails: List[str],
    irrelevant: Set[str] = None,
) -> Iterator[str]:
    """Test targets that should pass and fail for a given scenario."""

    if irrelevant is None:
        irrelevant = set()

    with ExitStack() as stack:
        test_dir = stack.enter_context(build_cleaned_resource(scenario))

        yield test_dir

        for target in passes:
            target_test(target, test_dir, True, target not in irrelevant)
        for target in fails:
            target_test(target, test_dir, False, target not in irrelevant)


def test_entry_python_tasks():
    """Ensure that we can run Python-based tasks."""

    scenario = "python-tasks"

    passes = [
        (
            "python-lint python-sa"
            f"{' yaml-lint-manifest.yaml' if not is_windows() else ''} "
            "python-build-once RANDOM_ENV_VAR=1"
        ),
        "python-build",
        "python-test",
        "python-test-add",
        "dz-sync",
    ]
    fails = ["python-deps", "python-editable", f"python-install-{scenario}"]

    with target_tests(scenario, passes, fails, set(fails)) as test_dir:
        for _ in range(2):
            assert mk_main([PKG_NAME, "-C", test_dir, "-d", "venv"]) == 0

        for _ in range(2):
            assert (
                mk_main(
                    [PKG_NAME, "-C", test_dir, "-d", "python-install-yamllint"]
                )
                == 0
            )

        assert mk_main([PKG_NAME, "-C", test_dir, "-d", "asdf"]) != 0
        assert mk_main([PKG_NAME, "-C", test_dir, "-d", "fail"]) != 0
