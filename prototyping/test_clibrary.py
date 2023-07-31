from ctypes import CDLL
from ctypes.util import find_library

import pytest

from src.compiler import compile_lib, SRC
from src.point import get_point


# @pytest.fixture
# def cdll():
#     source = SRC / "clibrary.cpp"
#     compile_lib(source)
#
#     yield CDLL(str(source.with_suffix(".so")))


def test_get_point(capsys):
    source = find_library("clibrary")
    cdll = CDLL(source)

    input_point = {"x": 10, "y": 20}
    result_point = get_point(cdll, input_point)

    # Print point members and assert values are right
    print(result_point["x"], result_point["y"])
    captured = capsys.readouterr()
    assert captured.out == "20 30\n"
