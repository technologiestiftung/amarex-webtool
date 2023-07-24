import ctypes


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
