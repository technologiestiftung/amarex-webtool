TEMPLATE = lib
TARGET = option_3

QMAKE_MACOSX_DEPLOYMENT_TARGET = 13.4

CONFIG += plugin
#QT += core
INCLUDEPATH += /Users/guadaluperomero/.pyenv/versions/3.11.4/envs/amarex/lib/python3.11/site-packages/pybind11/include

# Link against the Python shared library
LIBS += -L/Users/guadaluperomero/.pyenv/versions/3.11.4/lib -lpython3.11

# Include the Python header files
INCLUDEPATH += /Users/guadaluperomero/.pyenv/versions/3.11.4/include/python3.11

SOURCES += option_3.cpp
