import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"function {func.__name__} runtime: {end_time - start_time:.6f} seconds")
        return result
    return wrapper