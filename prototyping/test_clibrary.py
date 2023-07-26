import ctypes
from ctypes import CDLL
from ctypes.util import find_library

import pytest

from src.compiler import compile_lib, SRC
from src.structs import Point

lib_filename = find_library("clibrary")
lib = CDLL(lib_filename)


@pytest.fixture
def cdll():
    source = SRC / "clibrary.cpp"
    compile_lib(source)

    yield CDLL(str(source.with_suffix(".so")))


def test_get_point(capsys):
    cdll = lib
    cdll.getPoint.restype = ctypes.POINTER(Point)
    cdll.getPoint.argtype = ctypes.POINTER(Point)
    point_a = Point(10, 20)
    p = cdll.getPoint(point_a)

    # Print point members and assert values are right
    print(p.contents.x, p.contents.y)
    captured = capsys.readouterr()
    assert captured.out == "20 30\n"
