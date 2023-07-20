import ctypes
import os


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


path = os.getcwd()
clibrary = ctypes.CDLL(os.path.join(path, 'clibrary.so'))

clibrary.getPoint.restype = ctypes.POINTER(Point)
#p = ctypes.POINTER(Point)
p = clibrary.getPoint()
print(p.contents.x, p.contents.y)
