import ctypes
from ctypes import CDLL
from ctypes.util import find_library

import pytest

from src.compiler import compile_lib, SRC
from src.structs import Point

lib_filename = find_library("libc.so.6")
lib = CDLL(lib_filename)


@pytest.fixture
def wrapper():
    source = SRC / "clibrary.c"
    compile_lib(source)

    yield CDLL(str(source.with_suffix(".so")))


def test_get_point(wrapper, capsys):
    wrapper.getPoint.restype = ctypes.POINTER(Point)
    p = wrapper.getPoint()
    print(p.contents.x, p.contents.y)
    captured = capsys.readouterr()
    assert captured.out == "50 10\n"
