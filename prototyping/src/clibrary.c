#include <stdio.h>

struct Point {
    int x;
    int y;
};

struct Point *getPoint(int x_value, int y_value) {
    struct Point point;         // Initialize variable
    struct Point *ptr;          // Initialize pointer to variable
    ptr = &point;               // Store address of variable in pointer
    ptr->x = x_value;           // Get x member of variable that ptr points to and assign a value to it
    ptr->y = y_value;           // Get y member of variable that ptr points to and assign a value to it
    return ptr;
}

void printPoint(struct Point p) {
        printf("%d %d\n", p.x, p.y);
}
