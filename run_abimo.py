import argparse
import ctypes
from ctypes.util import find_library
import os
from datetime import datetime


def calculate():
    """
    Calculate with Abimo.
    """
    # Define working directory
    os.chdir(args.lib_dir)

    # Load compiled C++ library
    lib_filename = find_library("myAbimo")
    lib = ctypes.CDLL(lib_filename)

    # Set argument and result types
    lib.dllmain.argtypes = ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
    lib.dllmain.restype = ctypes.c_int

    # Prepare files
    config_file = bytes(args.config_file, encoding="utf-8")
    input_file = bytes(args.input_file, encoding="utf-8")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filepath = os.path.join(args.output_dir, f"output_{timestamp}.dbf")
    open(output_filepath, "a")
    output_file = bytes(output_filepath, encoding="utf-8")

    # Calculate
    lib.dllmain(input_file, config_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python wrapper for Abimo"
    )

    parser.add_argument("lib_dir", help="Path to the directory storing the compiled Abimo library")
    parser.add_argument("output_dir", help="Path to the dir where to save the output DBF file")
    parser.add_argument("input_file", help="Path to the input DBF file")
    parser.add_argument("--config-file", default="", help="Path to the config XML file")

    args = parser.parse_args()

    calculate()
