#include <iostream>
#include <omp.h>

int main() {
    const long long limit = 10000000000; // 1 billion
    long long sum = 0;

    #pragma omp parallel for reduction(+:sum)
    for (long long i = 1; i <= limit; i++) {
        sum += i;
    }

    std::cout << "Sum = " << sum << std::endl;

    return 0;
}