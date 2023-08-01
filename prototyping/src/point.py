import ctypes


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


def get_point(cdll, input_point):
    """
    Perform some calculations on an input point.

    :param: compiled C++ library
    :param input_point: dict, containing the x and y values of the input point
    :return result_point: dict, containing the x and y values of the resulting point
    """
    # Define types of arguments and return of getPoint function
    cdll.getPoint.restype = ctypes.POINTER(Point)
    cdll.getPoint.argtypes = (Point,)

    # Calculate with getPoint and save results
    input_point = Point(input_point["x"], input_point["y"])
    c_result_point = cdll.getPoint(input_point)
    result_point = {"x": c_result_point.contents.x, "y": c_result_point.contents.y}

    # Deallocate memory in C++
    cdll.deletePoint(c_result_point)

    return result_point
