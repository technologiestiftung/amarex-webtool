from ctypes import CDLL
from ctypes.util import find_library
import time

import pytest

from src.compiler import compile_lib
from src import option_1, option_3


def create_dummy_vector(n_rows, n_columns):
    """
    Create a dummy 2D vector.

    :param n_rows: int, number of rows
    :param n_columns: int, number of columns
    :return: array, containing arrays of integers
    """
    vector = []
    row = []

    for i in range(n_rows):
        if len(row) < n_columns:
            row.append(i)
        else:
            vector.append(row)
            row = [i]

    return vector


def generate_powers_of_10(list_length):
    """
    Generate a list of powers of 10, i.e., [1, 10, 100, ...]

    :param list_length: int, wished list length
    :return: list, containing powers of 10
    """
    powers_of_10 = []
    power = 1
    while len(powers_of_10) < list_length:
        powers_of_10.append(power)
        power *= 10

    return powers_of_10


N_ROWS = generate_powers_of_10(8)


@pytest.fixture(params=N_ROWS)
def n_rows(request):
    """
    List with numbers of rows to use in the tests.
    """
    return request.param


@pytest.fixture
def cdll(request):
    """
    Fixture for the compilation of a C++ library.
    """
    compile_lib(request.param)
    yield CDLL(find_library(request.param))


@pytest.mark.skip(reason="WIP")
@pytest.mark.parametrize("cdll", ["option_1"], indirect=True)
def test_option_1(cdll, n_rows):
    """
    Test for option 1:
    1/ Input array is sent from Python to C++
    2/ Array is converted to QVector, processed and converted back to array
    3/ Output array is sent from C++ to Python

    :param cdll: compiled library
    :param n_rows: int, number of vector rows
    """
    input_array = create_dummy_vector(n_rows, 2)

    # Start timer
    start_time = time.time()

    # Call C++ function
    output_array = option_1.process_input(cdll, input_array)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("--- OPTION 1 ---")
    print(f"Number of rows: {n_rows}")
    print(f"Computation time: {elapsed_time:.6f} seconds")

    assert input_array == output_array


@pytest.mark.skip(reason="WIP")
@pytest.mark.parametrize("cdll", ["option_1"], indirect=True)
def test_option_1_without_return(cdll, n_rows):
    """
    Test for option 1, with a small change:
    Same as option 1, but the output QVector is not converted to array nor sent back to Python.
    This is a proxy just to see how much computation time this last step costs.

    :param cdll: compiled library
    :param n_rows: int, number of vector rows
    """
    input_array = create_dummy_vector(n_rows, 2)

    # Start timer
    start_time = time.time()

    # Call C++ function
    option_1.process_input_without_return(cdll, input_array)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("--- OPTION 1 (WITHOUT RETURN) ---")
    print(f"Number of rows: {n_rows}")
    print(f"Computation time: {elapsed_time:.6f} seconds")


@pytest.mark.skip(reason="Import of compiled library fails")
@pytest.mark.parametrize("cdll", ["option_2"], indirect=True)
def test_option_2(cdll):
    """
    Test for option 2:
    Use Pybind11 to create Python bindings of existing C++ code.

    :param cdll: compiled library
    """
    from src import option_2_wrapper

    input_array = [[1, 2], [3, 4], [5, 6]]

    # Start timer
    start_time = time.time()

    # Call C++ function
    output_vector = option_2_wrapper.process_input(input_array)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.6f} seconds")

    for input_point, output_point in zip(input_array, output_vector):
        assert input_point[0] == output_point.x
        assert input_point[1] == output_point.y


@pytest.mark.parametrize("cdll", ["option_3"], indirect=True)
def test_option_3(cdll, n_rows):
    """
    Test for option 3:
    1/ Input array is transformed to a C++ vector of Points row per row from Python
    2/ Vector is processed and converted back to array in C++
    3/ Output array is sent from C++ to Python

    :param cdll: compiled library
    :param n_rows: int, number of vector rows
    """
    input_array = create_dummy_vector(n_rows, 2)

    # Start timer
    start_time = time.time()

    # Call C++ function
    output_array = option_3.process_input(cdll, input_array)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("--- OPTION 3 ---")
    print(f"Number of rows: {n_rows}")
    print(f"Computation time: {elapsed_time:.6f} seconds")

    assert input_array == output_array
