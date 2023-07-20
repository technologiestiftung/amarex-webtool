#include <stdio.h>

struct Point {
    int x;
    int y;
};

struct Point *getPoint() {
    struct Point point;         // Initialize variable
    struct Point *ptr;          // Initialize pointer to variable
    ptr = &point;               // Store address of variable in pointer
    ptr->x = 50;                // Get x member of variable that ptr points to and assign a value to it
    ptr->y = 10;                // Get y member of variable that ptr points to and assign a value to it
    return ptr;
}

void printPoint(struct Point p) {
        printf("%d %d\n", p.x, p.y);
}
