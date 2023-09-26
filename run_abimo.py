import argparse
import ctypes
from ctypes.util import find_library
from datetime import datetime
import os
import random


class AbimoInputRecord(ctypes.Structure):
    """
    Struct for C++ class AbimoInputRecord.
    """
    _fields_ = [
        ("usage", ctypes.c_int),
        ("code", ctypes.c_char_p),  # TODO: This may not be the correct type (equivalent to QString)
        ("precipitationYear", ctypes.c_int),
        ("precipitationSummer", ctypes.c_int),
        ("depthToWaterTable", ctypes.c_float),
        ("type", ctypes.c_int),
        ("fieldCapacity_30", ctypes.c_int),
        ("fieldCapacity_150", ctypes.c_int),
        ("district", ctypes.c_int),
        ("mainFractionBuiltSealed", ctypes.c_float),
        ("mainFractionUnbuiltSealed", ctypes.c_float),
        ("roadFractionSealed", ctypes.c_float),
        ("builtSealedFractionConnected", ctypes.c_float),
        ("unbuiltSealedFractionConnected", ctypes.c_float),
        ("roadSealedFractionConnected", ctypes.c_float),
        ("unbuiltSealedFractionSurface", ctypes.c_float),
        ("roadSealedFractionSurface", ctypes.c_float),
        ("mainArea", ctypes.c_float),
        ("roadArea", ctypes.c_float)
    ]


class AbimoOutputRecord(ctypes.Structure):
    """
    Struct for C++ class AbimoOutputRecord.
    """
    _fields_ = [
        ("code_CODE", ctypes.c_char_p),  # TODO: This may not be the correct type (equivalent to QString)
        ("totalRunoff_R", ctypes.c_float),
        ("surfaceRunoff_ROW", ctypes.c_float),
        ("infiltration_RI", ctypes.c_float),
        ("totalRunoffFlow_RVOL", ctypes.c_float),
        ("surfaceRunoffFlow_ROWVOL", ctypes.c_float),
        ("infiltrationFlow_RIVOL", ctypes.c_float),
        ("totalArea_FLAECHE", ctypes.c_float),
        ("evaporation_VERDUNSTUN", ctypes.c_float)
    ]


def preprocess_input(input_file):
    """
    Convert DBF input file to AbimoInputRecord object.
    """
    # TODO: For now, we just initialize a dummy input.
    input_dummy = AbimoInputRecord(
        random.randint(0, 100),
        ctypes.c_char_p(b"1000536281000000"),  # TODO: May not be the correct type (QString)
        random.randint(0, 100),
        random.randint(0, 100),
        random.uniform(0.0, 100.0),
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(0, 100),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(1.0, 4.0),
        random.uniform(1.0, 4.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0),
        random.uniform(0.0, 100.0)
    )

    return input_dummy


def preprocess_output():
    """
    Convert DBF output file to AbimoOutputRecord object.
    """
    # TODO: For now, we just initialize a dummy output.
    output_dummy = AbimoOutputRecord(
        ctypes.c_char_p(b""),  # TODO: May not be the correct type (QString)
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    )

    return output_dummy


def calculate_in_memory(input_obj, output_obj):
    """
    Calculate with Abimo, using Python data structures.
    """
    # TODO: Take library loading outside of this function and refactor everything neatly in a class

    # Define working directory
    os.chdir(args.lib_dir)

    # Load compiled C++ library
    lib_filename = find_library("myAbimo")
    lib = ctypes.CDLL(lib_filename)

    # Set argument and result types
    lib.calculateData.argtypes = ctypes.POINTER(AbimoInputRecord), ctypes.POINTER(AbimoOutputRecord)
    lib.calculateData.restype = ctypes.c_int

    # Calculate
    lib.calculateData(input_obj, output_obj)

    # TODO: The current C++ implementation of this method makes changes directly to the
    #   AbimoOutputRecord and doesn't return anything. I am not sure that we can access
    #   the updated output from Python like this.
    #   Our Python calculate_in_memory() method should return an AbimoOutputRecord object.


def write_to_file(output_obj):
    """
    Write Abimo output to a DBF file.
    """
    # TODO: To be implemented
    pass


# def calculate():
#     """
#     Calculate with Abimo.
#     """
#     # Define working directory
#     os.chdir(args.lib_dir)
#
#     # Load compiled C++ library
#     lib_filename = find_library("myAbimo")
#     lib = ctypes.CDLL(lib_filename)
#
#     # Set argument and result types
#     lib.dllmain.argtypes = ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
#     lib.dllmain.restype = ctypes.c_int
#
#     # Prepare files
#     config_file = bytes(args.config_file, encoding="utf-8")
#     input_file = bytes(args.input_file, encoding="utf-8")
#
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_filepath = os.path.join(args.output_dir, f"output_{timestamp}.dbf")
#     open(output_filepath, "a")
#     output_file = bytes(output_filepath, encoding="utf-8")
#
#     # Calculate
#     lib.dllmain(input_file, config_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python wrapper for Abimo"
    )

    parser.add_argument("lib_dir", help="Path to the directory storing the compiled Abimo library")
    parser.add_argument("output_dir", help="Path to the dir where to save the output DBF file")
    parser.add_argument("input_file", help="Path to the input DBF file")
    parser.add_argument("--config-file", default="", help="Path to the config XML file")

    args = parser.parse_args()

    # Preprocess the input and output files
    input_obj = preprocess_input(args.input_file)

    # TODO: Is it possible to get non-empty output files?
    #  In this case, do they work like "intermediate results" that are part of the calculation?
    output_obj = preprocess_output()

    # Perform calculations
    calculate_in_memory(input_obj, output_obj)
    # TODO: Currently, we get the following error when executing this line:
    #   [1]    8241 segmentation fault  python run_abimo.py "/abimo/release"
