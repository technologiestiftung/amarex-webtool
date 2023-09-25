from ctypes import CDLL, c_int, c_void_p, POINTER, pointer
from ctypes.util import find_library
import os
import time

import pytest

from compiler import compile_lib
from read_dbf import read_file, to_abimo_array, AbimoInputRecordStruct


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
    records, records_n = to_abimo_array(df)

    cdll.array2AbimoInputVector.argtypes = [POINTER(AbimoInputRecordStruct), c_int]
    cdll.array2AbimoInputVector.restype = c_void_p

    abimo_input_vector = cdll.array2AbimoInputVector(pointer(records[0]), records_n)

    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("--- OPTION 1 ---")
    print(f"Computation time: {elapsed_time:.6f} seconds")

    # TODO: Add assertions
