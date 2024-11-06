# tests/test_main.py

from app.main import add, subtract


def test_add():
    assert add(10, 5) == 15
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2


def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 0) == 0
    assert subtract(-1, 1) == -2
    assert subtract(-1, -1) == 0
