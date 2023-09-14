from ctypes import c_int, c_void_p, POINTER, Structure


# Define the Point struct
class Point(Structure):
    _fields_ = [("x", c_int),
                ("y", c_int)]


def process_input(cdll, input_array):
    """
    Process an input array.

    :param cdll: compiled C++ library
    :param input_array: array, 2D nested array containing the input values
    :return: array, 2D nested array containing the output values
    """
    # Define the function prototypes with restype and argtypes
    cdll.createPoint.restype = POINTER(Point)
    cdll.createPoint.argtypes = [c_int, c_int]

    cdll.deletePoint.argtypes = [POINTER(Point)]

    cdll.createPointVector.restype = POINTER(c_void_p)  # QVector is a template, so we use void pointer
    cdll.createPointVector.argtypes = []

    cdll.addPointToVector.argtypes = [POINTER(c_void_p), POINTER(Point)]

    cdll.deletePointVector.argtypes = [POINTER(c_void_p)]

    cdll.vector2Array.restype = POINTER(POINTER(c_int))
    cdll.vector2Array.argtypes = [POINTER(c_void_p), POINTER(c_int)]

    cdll.processPointVector.argtypes = [
        POINTER(c_void_p),
        POINTER(c_void_p)
    ]

    # Process the input with C++
    input_vector = cdll.createPointVector()
    output_vector = cdll.createPointVector()
    for point in input_array:
        point_c = cdll.createPoint(point[0], point[1])
        cdll.addPointToVector(input_vector, point_c)
        cdll.deletePoint(point_c)

    cdll.processPointVector(input_vector, output_vector)
    output_array = cdll.vector2Array(output_vector, c_int(len(input_array)))

    cdll.deletePointVector(input_vector)
    cdll.deletePointVector(output_vector)

    # Unflatten the output array so that it has 2D
    output_array = [[output_array[i][0], output_array[i][1]] for i in range(len(input_array))]

    return output_array
