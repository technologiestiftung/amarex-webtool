//#include <QVector>

#include <stdio.h>

extern "C" struct Point {
    int x;
    int y;
};

extern "C" struct Point *getPoint(struct Point point_a) {
    struct Point point_result;          // Initialize variable
    struct Point *ptr;                  // Initialize pointer to variable
    ptr = &point_result;                // Store address of variable in pointer

    ptr->x = point_a.x + 10;            // Get x member of variable that ptr points to and assign a value to it
    ptr->y = point_a.y + 10;            // Get y member of variable that ptr points to and assign a value to it
    return ptr;
}

extern "C" void printPoint(struct Point p) {
        printf("%d %d\n", p.x, p.y);
}

int main() {
    return 0;
}
