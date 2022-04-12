import asyncio
import numpy as np
from typing import Tuple
from loguru import logger
import time

from tools import timeit

class Field:

    def __init__(self, width: int, height: int) -> None:
        self.size = width, height
        self.array = np.zeros(self.size, dtype=np.ubyte)
        self.to_update = {(x, y) for x in range(width) for y in range(height)}
        self.add_life()
    
    def add_life(self) -> None:
        life = np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 1],
            ]).transpose()
        o_w, o_h = [i//2 for i in self.size]
        self.array[o_w-3:o_w, o_h-3:o_h] = life
    
    @timeit
    def to_image(self, offset: Tuple[int, int], size: Tuple[int, int]) -> np.array:
        o_x, o_y = offset
        s_x, s_y = size
        image = self.array[o_x:o_x+s_x, o_y:o_y+s_y]
        return image
    
    @timeit
    def __str__(self) -> None:
        symbols = {0: '_', 1: '#'}
        rows = list()
        for row in self.array.transpose()[:,:]:
            row_s = ''.join(map(symbols.get, row))
            rows.append(row_s)
        return '\n'.join(rows)+'\n'
    
    @timeit
    def life_step(self) -> None:
        # logger.debug('life step')
        cells_to_change = list()
        width, height = self.size
        for x, y in self.to_update:
            alive = self.array[x, y]
            n = self.array[x-1:x+2, y-1:y+2].sum() - alive
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

    def main(self, tps: int) -> None:
        spt = 1/tps
        while True:
            start = time.time()
            self.life_step()
            time_to_sleep = spt - time.time() + start
            if time_to_sleep <= 0:
                logger.warning(f"low field tps")
            else:
                time.sleep(time_to_sleep)
            
