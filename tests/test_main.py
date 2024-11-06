# tests/test_main.py

from app.main import add, subtract, multiply


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


def test_multiply():
    assert multiply(10, 5) == 50
    assert multiply(0, 0) == 0
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1
