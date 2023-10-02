// sum_without_parallel.cpp

#include <iostream>

int main() {
    const long long limit = 10000000000; // 1 billion
    long long sum = 0;

    for (long long i = 1; i <= limit; i++) {
        sum += i;
    }

    std::cout << "Sum = " << sum << std::endl;

    return 0;
}