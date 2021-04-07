# -*- coding: utf-8 -*-

import pytest
from wt_failure_detection.skeleton import fib

__author__ = "alessandro.negrini@axa.it"
__copyright__ = "alessandro.negrini@axa.it"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
