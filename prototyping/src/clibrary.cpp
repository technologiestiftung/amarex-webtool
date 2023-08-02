#include <QVector>

#include <stdio.h>

/**
 *Define structure of Point objects.
 */
extern "C" struct Point {
    int x;
    int y;
};

/**
 *Allocate storage for the object, set its elements and
 *return the pointer, i.e. the memory address to the object.
 */
extern "C" Point* createPoint(int x, int y) {
    Point* point = new Point();

    point->x = x;
    point->y = y;

    return point;
}

/**
 *Given the pointer to a Point object,
 *free the storage that was allocated for it.
 */
extern "C" void deletePoint(Point* point) {
    if (point) {
        delete point;
    }
}

/**
 *Create an empty QVector object.
 */
extern "C" QVector<Point>* createPointVector() {
    QVector<Point>* pointVector = new QVector<Point>();

    return pointVector;
}

/**
 *Add a Point object to an existing QVector object.
 */
extern "C" QVector<Point>* addPointToVector(QVector<Point>* pointVector, Point* point) {
    pointVector->append(*point);

    return pointVector;
}

/**
 *Delete a QVector object, including all its elements.
 */
extern "C" void deletePointVector(QVector<Point>* pointVector) {
    if (pointVector) {
        delete pointVector;
    }
}

/**
 *Perform some calculations on an input QVector containing Points
 *and return the resulting points in an output QVector.
 */
extern "C" QVector<Point>* processPointVector(
    QVector<Point>* inputPointVector,
    QVector<Point>* outputPointVector
)
{
    for (int i = 0; i < inputPointVector->size(); i++) {
        Point inputPoint = inputPointVector->at(i);
        outputPointVector->append(inputPoint);
    }

    return outputPointVector;
}

int main() {
    return 0;
}
