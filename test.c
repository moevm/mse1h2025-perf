#include <math.h>
#include <stdlib.h>
void fastFunction() {
    double* result = malloc(sizeof(double) * 1000000);
    for (int i = 0; i < 1000000; ++i) {
        result[i] = sin(i) * cos(i);
    }
    result[1000000] = 1;
    //free(result);
}
void slowFunction() {
    double* result = malloc(sizeof(double) * 5000000);
    for (int i = 0; i < 5000000; ++i) {
        result[i] = sqrt(i) * log(i);
    }
    free(result);
}
int main() {
    for (int i = 0; i < 5; ++i) {
        fastFunction();
        slowFunction();
    }
    return 0;
}
