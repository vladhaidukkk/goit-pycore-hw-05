from typing import Callable

def caching_fibonacci() -> Callable[[int], int]:
    # Cache is enclosed within the inner function (fibonacci) -> GC does not clean it up
    cache: dict[int, int] = {}
    
    def fibonacci(n) -> int:
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]
        
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    
    print(f"{fib(10)=}")
    print(f"{fib(15)=}")
    