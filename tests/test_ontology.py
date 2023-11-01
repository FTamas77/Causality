import sys
import pytest

from ontology import hello


def test_ontology():
    b = hello()
    assert b == 5
