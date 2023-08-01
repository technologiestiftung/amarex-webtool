#include <QVector>

#include <stdio.h>

extern "C" struct Point {
    int x;
    int y;
};

extern "C" struct Point *getPoint(QVector<struct Point> point_a) {

    struct Point *point_result = new struct Point; // Allocate memory for point_result on the heap

    point_result->x = point_a.at(0).x + 10;
    point_result->y = point_a.at(0).y + 10;
    return point_result;
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
