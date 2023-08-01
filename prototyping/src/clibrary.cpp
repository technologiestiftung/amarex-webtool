#include <QVector>

#include <stdio.h>

extern "C" struct Point {
    int x;
    int y;
};

extern "C" struct Point *getPoint(QVector<struct Point>& input_point) {

    struct Point *result_point = new struct Point; // Allocate memory for point_result on the heap

    result_point->x = input_point.at(0).x + 10;
    result_point->y = input_point.at(0).y + 10;
    return result_point;
}

extern "C" void deletePoint(struct Point *point) {
    delete point; // Free the allocated memory for the Point struct
}

extern "C" void printPoint(struct Point p) {
        printf("%d %d\n", p.x, p.y);
}

int main() {
    return 0;
}
