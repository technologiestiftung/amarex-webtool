from ctypes import c_int, POINTER


def process_input(cdll, input_array):
    """
    Process an input array.
    :param cdll: compiled C++ library
    :param input_array: array, 2D nested array containing the input values
    :return: array, 2D nested array containing the output values
    """
    # Define argument and return types for the C++ function processInput
    cdll.processInput.argtypes = [POINTER(c_int), c_int]
    cdll.processInput.restype = POINTER(POINTER(c_int))

    # Flatten the array, so it can be processed by the C++ function processInput
    n_rows = len(input_array)
    input_array_flat = [col for row in input_array
                            for col in row]

    # Process the input with C++
    output_array_pointer = cdll.processInput((c_int * len(input_array_flat))(*input_array_flat), n_rows)

    # Unflatten the output array so that it has 2D
    output_array = [[output_array_pointer[i][0], output_array_pointer[i][1]] for i in range(n_rows)]

    return output_array
