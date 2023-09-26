from ctypes import CDLL, c_int, c_void_p, POINTER, pointer
from ctypes.util import find_library
import os
import time

import pytest

from compiler import compile_lib
from read_dbf import read_file, to_abimo_array, AbimoInputRecord, AbimoOutputRecord


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


    # Transform input DBF file to a vector of AbimoInputRecord objects
    df = read_file()
    records, records_n = to_abimo_array(df)

    cdll.array2AbimoInputVector.argtypes = [POINTER(AbimoInputRecord), c_int]
    cdll.array2AbimoInputVector.restype = c_void_p

    abimo_input_vector = cdll.array2AbimoInputVector(pointer(records[0]), records_n)

    # Create a vector of empty AbimoOutputRecord objects
    # with the same number of records as in the input
    cdll.createAbimoOutputRecordVector.argtypes = [c_int]
    cdll.createAbimoOutputRecordVector.restype = POINTER(AbimoOutputRecord)

    records = cdll.createAbimoOutputRecordVector(records_n)

    # Convert the records to a list
    record_list = [records[i] for i in range(records_n)]

    # TODO: Free memory for the vectors



    # Calculate computation time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Number of records: {records_n}")
    print(f"Computation time: {elapsed_time:.6f} seconds")

    # TODO: Add assertions
