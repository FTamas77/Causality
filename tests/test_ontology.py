import sys
import pytest

from ontology import hello


def test_go_to_tmpdir(request):
    b = hello()
    assert b == 5
