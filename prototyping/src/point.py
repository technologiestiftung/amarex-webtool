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


def process_point_vector(cdll):
    # Define argument and return types for the C++ functions
    cdll.createPointVector.restype = ctypes.POINTER(ctypes.c_void_p)

    cdll.createPoint.argtypes = (ctypes.c_int, ctypes.c_int)
    cdll.createPoint.restype = ctypes.POINTER(Point)

    # TODO: Here it should be QVector type instead of c_void_p but this is not straightforward in Python
    cdll.addPointToVector.argtypes = (ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(Point))
    cdll.addPointToVector.restype = ctypes.POINTER(ctypes.c_void_p)

    # Create the (empty) QVector object in C++ and store the pointer to that object in c_vector
    c_vector = cdll.createPointVector()
    output_vector = cdll.createPointVector()

    # Create some objects of C++ class points and store the pointers to these objects in c_point_1, ..., c_point_3
    c_point_1 = cdll.createPoint(1, 2)
    c_point_2 = cdll.createPoint(3, 4)
    c_point_3 = cdll.createPoint(5, 6)

    # Add the point objects one by one to the QVector object
    c_vector = cdll.addPointToVector(c_vector, c_point_1)
    c_vector = cdll.addPointToVector(c_vector, c_point_2)
    c_vector = cdll.addPointToVector(c_vector, c_point_3)

    # Now that all points are in the QVector object we can delete the original point objects
    cdll.deletePoint(c_point_1)
    cdll.deletePoint(c_point_2)
    cdll.deletePoint(c_point_3)

    # c_vector should now point to a QVector object that has three point objects in it

    # Pass c_vector to a function (not yet available) that can handle the data in the QVector object...
    cdll.processPointVector(c_vector, output_vector)

    # Finally, delete the QVector object
    cdll.deletePointVector(c_vector)
