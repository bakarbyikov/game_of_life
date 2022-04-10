# from turtle import width
import numpy as np
import time
import functools


def timeit(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        ret = f(*args, **kwargs)
        elapsed = time.perf_counter() - start

        inner.__elapsed__ = elapsed
        # inner.__total_time__ += elapsed
        # inner.__n_calls__ += 1

        return ret


    inner.__elapsed__ = 0
    # inner.__total_time__ = 0
    # inner.__n_calls__ = 0
    return inner

class Field:

    def __init__(self, width: int, height: int) -> None:
        self.size = width, height
        self.array = np.zeros(self.size, dtype=np.bool_)
        self.to_update = {(x, y) for x in range(width) for y in range(height)}
    
    def add_life(self) -> None:
        life = np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 1],
            ]).transpose()
        o_w, o_h = [i//2 for i in self.size]
        self.array[o_w:o_w+3, o_h:o_h+3] = life
    
    @timeit
    def __str__(self):
        symbols = {0: '_', 1: '#'}
        rows = list()
        for row in self.array.transpose()[:,:]:
            row_s = ''.join(map(symbols.get, row))
            rows.append(row_s)
        return '\n'.join(rows)+'\n'
    
    @timeit
    def life_step(self) -> None:
        cells_to_change = list()
        width, height = self.size
        for x, y in self.to_update:
            alive = self.array[x, y]
            n = self.array[x-1:x+2, y-1:y+2].sum() - alive
            # alive = n == 3  or (n == 4 and self.array[x, y])
            if alive:
                changed = n > 3 or n < 2
            else:
                changed = n == 3
            if changed:
                cells_to_change.append((x, y))
        self.to_update.clear()
        
        for x, y in cells_to_change:
            self.array[x, y] = not self.array[x, y]
            for n_x in range(x-1, x+2):
                if n_x < 0 or n_x >= width:
                    continue
                for n_y in range(y-1, y+2):
                    if n_y < 0 or n_y >= height:
                        continue
                    self.to_update.add((n_x, n_y))
        return len(cells_to_change)




def main():
    size = width, height = 128, 16
    some_field = Field(*size)
    some_field.add_life()
    target_fps = 10

    while True:
        now = time.time()
        output = str(some_field)
        updated = some_field.life_step()
        d_time = some_field.__str__.__elapsed__
        u_time = some_field.life_step.__elapsed__
        output += f'drawing time: {d_time}\n'
        output += f'updating time: {u_time}\tper cel time: {u_time/updated}\n'

        output += f'fps: {1 / (time.time() - now)}'
        print(output)
        time.sleep(0.1)

if __name__ == "__main__":
    main()