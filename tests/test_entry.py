
"""
datazen - Test the program's entry-point.
"""

# built-in
from multiprocessing import Process
import os
import signal
import time

# module under test
from vmklib.entry import main as mk_main

# internal
from . import get_resource, get_args


def test_interrupt():
    """ Test interrupting the process. """

    with get_args() as base_args:
        good_base_args = base_args + ["-f", get_resource("Makefile"), "sleep"]
        proc = Process(target=mk_main, args=[good_base_args])
        proc.start()
        time.sleep(0.5)
        os.kill(proc.pid, signal.SIGINT)
        proc.join()


def test_entry():
    """ Test some basic command-line argument scenarios. """

    with get_args() as base_args:
        good_base_args = base_args + ["-f", get_resource("Makefile")]
        assert mk_main(good_base_args + ["test"]) == 0
        assert mk_main(good_base_args + ["--proj", "test", "test"]) == 0
        assert mk_main(good_base_args + ["-p", "prefix", "test"]) == 0
        assert mk_main(good_base_args + ["test_bad"]) != 0
        assert mk_main(good_base_args + ["--weird-option", "yo"]) != 0
        assert mk_main(base_args + ["-f", "nah"]) != 0
        assert mk_main(base_args) == 0
