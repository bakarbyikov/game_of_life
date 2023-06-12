import functools
import time

def timeit(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        ret = f(*args, **kwargs)
        elapsed = time.perf_counter() - start

        inner.__elapsed__ = elapsed
        inner.__total_time__ += elapsed
        inner.__n_runs__ += 1

        return ret
    
    inner.__total_time__ = 0
    inner.__n_runs__ = 0
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