from ctypes import CDLL, c_int, c_void_p, POINTER
from ctypes.util import find_library
import os
import time

import pytest

from compiler import compile_lib
from read_dbf import read_file, to_abimo_array


@pytest.fixture
def cdll():
    """
    Fixture for the compilation of a C++ library.
    """
    project_path = "/Users/guadaluperomero/ProjectsTSB/amarex/abimo"
    compile_lib(project_path)

    os.chdir(f"{project_path}/release")
    compiled_lib = CDLL(find_library("myAbimo"))

    yield compiled_lib


def test_read_dbf(cdll):
    """
    Test conversion of a DBF file to a vector of Abimo input records.

    :param cdll: compiled library
    """
    # Start timer
    start_time = time.time()

    df = read_file()
    abimo_array, shape = to_abimo_array(df)

    # TODO: Have to specify the right type here
    #cdll.array2AbimoInputVector.argtypes = []
    #cdll.array2AbimoInputVector.restype = POINTER(c_int)

    # TODO: Might have to do some additional conversions here, check option 1 in branch wrapper_prototyping
    #   where I pass the first argument input_array_flat like this: (c_int * len(input_array_flat))(*input_array_flat)
    abimo_input_vector = cdll.array2AbimoInputVector(abimo_array, shape[0])

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("--- OPTION 1 ---")
    print(f"Number of rows: {shape[0]}")
    print(f"Computation time: {elapsed_time:.6f} seconds")

    # TODO: Add assertions
