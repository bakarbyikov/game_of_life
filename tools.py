from typing import NamedTuple, overload, Tuple
import functools
import time
import numpy as np

# class Coord(np.ndarray):
#     def __init__(self, x: int, y: int) -> None:
#         self.x = int(x)
#         self.y = int(y)
    
#     def __iter__(self):
        # return iter((self.x, self.y))

def timeit(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        ret = f(*args, **kwargs)
        elapsed = time.perf_counter() - start

        inner.__elapsed__ = elapsed

        return ret


    inner.__elapsed__ = 0
    return inner

def now():
    return time.time()

def not_so_fast(delay = 0.1):
    def decorate(f):
        # @functools.wraps
        def inner(*args, **kwargs):
            if now() - inner.__last_run__ >= delay:
                inner.__res__ = f(*args, **kwargs)
                inner.__last_run__ = now()
            return inner.__res__
    
        inner.__last_run__ = 0
        return inner
    return decorate

if __name__ == '__main__':
    pos = Coord(10, 20)
    for c in pos:
        print(c)