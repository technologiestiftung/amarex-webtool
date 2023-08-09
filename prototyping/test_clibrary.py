from ctypes import CDLL
from ctypes.util import find_library
import time

import pytest

from src.compiler import compile_lib
from src.point import process_input


@pytest.fixture
def cdll():
    compile_lib()
    yield CDLL(find_library("clibrary"))


def test_process_input(cdll):
    input_array = [[1, 2], [3, 4], [5, 6]]

    # Start timer
    start_time = time.time()

    # Call C++ function
    output_array = process_input(cdll, input_array)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.6f} seconds")

    assert input_array == output_array
