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
    c_point_a = Point(input_point["x"], input_point["y"])
    c_point_result = cdll.getPoint(c_point_a)
    result_point = {"x": c_point_result.contents.x, "y": c_point_result.contents.y}

    # Deallocate memory in C++
    cdll.deletePoint(c_point_result)

    return result_point
