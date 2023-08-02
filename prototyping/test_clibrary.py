from ctypes import CDLL
from ctypes.util import find_library

import pytest

from src.compiler import compile_lib
from src.point import get_point, process_point_vector


@pytest.fixture
def cdll():
    compile_lib()
    yield CDLL(find_library("clibrary"))


def test_get_point(cdll, capsys):

    # input_point = {"x": 10, "y": 20}
    # result_point = get_point(cdll, input_point)
    #
    # # Print point members and assert values are right
    # print(result_point["x"], result_point["y"])
    # captured = capsys.readouterr()
    # assert captured.out == "20 30\n"

    process_point_vector(cdll)
