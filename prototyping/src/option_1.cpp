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
 *Transform a 2D array of integers into a QVector of Points.
 */
extern "C" QVector<Point>* array2Vector(int array[][2], int numRows){
    QVector<Point>* pointVector = createPointVector();
    for (int i = 0; i < numRows; i++) {
        int* row = array[i];
        Point* point = createPoint(row[0], row[1]);
        addPointToVector(pointVector, point);
        deletePoint(point);
    }
    return pointVector;
}

/**
 *Transform a QVector of Points into a 2D array.
 */
extern "C" int** vector2Array(QVector<Point>* pointVector, int* numRows) {
    *numRows = pointVector->size();

    // Allocate an array of pointers for the rows
    int** array = new int*[*numRows];

    for (int i = 0; i < *numRows; i++) {
        // Allocate memory for each row
        array[i] = new int[2];

        Point point = pointVector->at(i);
        array[i][0] = point.x;
        array[i][1] = point.y;
    }

    return array;
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

/**
 *Perform some calculations on an input array containing Points
 *and return the resulting points in an output array.
 *Internally, this function processes the arrays as QVectors.
 */
extern "C" int** processInput(int array[][2], int numRows) {
    // Transform array to vector
    QVector<Point>* inputVector = array2Vector(array, numRows);

    // Perform calculations
    QVector<Point>* outputVector = createPointVector();
    outputVector = processPointVector(inputVector, outputVector);

    // Transform vector to array
    int** outputArray = vector2Array(outputVector, &numRows);

    // Clean memory for vectors that we no longer need
    deletePointVector(inputVector);
    deletePointVector(outputVector);

    return outputArray;
}

/**
 *Perform some calculations on an input array containing Points.
 *Do not return anything, this function is just for testing the performance
 *when there is no vector to array conversion.
 */
extern "C" void processInputWithoutReturn(int array[][2], int numRows) {
    // Transform array to vector
    QVector<Point>* inputVector = array2Vector(array, numRows);

    // Perform calculations
    QVector<Point>* outputVector = createPointVector();
    outputVector = processPointVector(inputVector, outputVector);

    // Clean memory for vectors that we no longer need
    deletePointVector(inputVector);
    deletePointVector(outputVector);
}
