import numpy as np
from typing import Tuple, NamedTuple
from loguru import logger
import time
from itertools import product

from tools import timeit

class Cell(NamedTuple):
    x: int
    y: int

class Field:

    def __init__(self, width: int, height: int) -> None:
        self.size = width, height
        self.array = np.zeros(self.size, dtype=np.ubyte)
        self.to_update = {Cell(x, y) for x, y  in product(range(width), range(height))}
        self.add_life()
    
    
    def add_life(self) -> None:
        life = np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 1],
            ]).transpose()
        o_w, o_h = (i//2 for i in self.size)
        self.array[o_w-3:o_w, o_h-3:o_h] = life


    def to_image(self, offset: Tuple[int, int], size: Tuple[int, int]) -> np.ndarray:
        o_x, o_y = offset
        s_x, s_y = size
        return self.array[o_x:o_x+s_x, o_y:o_y+s_y]
    

    def __str__(self) -> None:
        symbols = {0: '_', 1: '#'}
        rows = list()
        for row in self.array.transpose()[:,:]:
            row_s = ''.join(map(symbols.get, row))
            rows.append(row_s)
        return '\n'.join(rows)+'\n'
    

    def count_neighbor(self, cell: Cell):
        x, y = cell
        return self.array[x-1:x+2, y-1:y+2].sum() - self.array[cell]

    
    def is_cell_need_change(self, cell: Cell) -> bool:
        alive = self.array[cell]
        neighbor_count = self.count_neighbor(cell)
        if alive:
            #dead condition
            changed = neighbor_count > 3 or neighbor_count < 2
        else:
            #alive condition
            changed = neighbor_count == 3
        
        return changed
    

    def is_inbound(self, cell: Cell):
        w, h = self.size
        if 0 <= cell.x < w:
            if 0 <= cell.y < h:
                return True
        return False


    def add_to_update(self, cell: Cell):
        for o_x, o_y in product(range(-1, 2), repeat=2):
            neighbor = Cell(cell.x+o_x, cell.y+o_y)
            if self.is_inbound(neighbor):
                self.to_update.add(neighbor)


    def life_step(self) -> None:
        cells_to_change = tuple(filter(self.is_cell_need_change, self.to_update))
        self.to_update.clear()
        
        for cell in cells_to_change:
            self.array[cell] = not self.array[cell]
            self.add_to_update(cell)


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
            
if __name__ == '__main__':
    f = Field(100, 32)
    funcs = [f.life_step]
    for _ in range(100):
        print(f)
        f.life_step()