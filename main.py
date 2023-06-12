import functools
import pygame as pg
from loguru import logger
from typing import Tuple
import time
pg.init()

from field import Field
from tools import *

class Widget:
    def __init__(
            self, 
            pos: Tuple[int, int], 
            size: Tuple[int, int],
        ) -> None:
        raise NotImplementedError
    def to_draw(self):
        raise NotImplementedError


class Field_windget:

    def __init__(
            self, 
            pos: Tuple[int, int], 
            size: Tuple[int, int], 
            field: Field,
        ) -> None:
        self.pos = pos
        self.size = size
        self.field = field
    
    def to_draw(self):
        array_img = self.field.to_image((0, 0), (-1, -1))
        surf = pg.surfarray.make_surface(array_img)
        surf.set_palette_at(1, pg.Color('white'))
        scale = min([i/j for i, j in zip(self.size, array_img.shape)])
        new_size = [i * scale for i in array_img.shape]
        resized = pg.transform.scale(surf, new_size)
        return surf


class Camera:

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        self.pos = pos
        self.size = size


class Display():

    def __init__(
        self,
        size: Tuple[int, int] = (0, 0),
        flags: int = 0,
    ) -> None:
        self.size = w, h = size
        self.flags = pg.SCALED#pg.RESIZABLE
        self.surface = pg.display.set_mode(self.size, self.flags)
        self.last_update = now()
        self.widgets = list()
    

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)
    

    def update(self):
        # if self.size != pg.display.get_window_size():
        #     self.resize()
        #     self.update_surface()
        self.draw()
        try:
            fps = 1 / (now() - self.last_update)
        except ZeroDivisionError:
            fps = float('inf')
        if fps < 30:
            logger.warning(f"low fps~{fps:0.2f}")
        self.set_caption(f'fps:{fps:0.2f}')
        self.last_update = now()
    

    # def resize():
    #     pass
    

    # def update_surface(self):
    #     self.size = pg.display.get_window_size()
    #     self.surface = pg.display.get_surface()

    
    def draw(self):
        color = int(now()) % (256**3)
        self.surface.fill(color)
        for w in self.widgets:
            s = w.to_draw()
            self.surface.blit(s, (0, 0))
        pg.display.flip()


    @not_so_fast()
    def set_caption(self, caption: str) -> None:
        pg.display.set_caption(caption)
    


    

class Game:
    field_size = 100, 100

    def __init__(self, display: Display) -> None:
        self.field = Field(*self.field_size)
        self.display = display
        self.field_widget = Field_windget((0, 0), self.display.size, self.field)
        self.display.add_widget(self.field_widget)
    
    @not_so_fast()
    def update(self):
        self.field.life_step()
    

        



class App:
    # window_size = 1920//2, 1080//2
    window_size = 100, 100

    class Exit(BaseException):
        pass

    def __init__(self) -> None:
        self.screen = Display(self.window_size)
        self.game = Game(self.screen)
        self.clock = pg.time.Clock()
        try:
            self.mainloop()
        except self.Exit:
            pass

    
    def mainloop(self) -> None:
        while True:
            self.handle_events()
            self.screen.update()
            self.game.update()
            self.clock.tick(60)

    
    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    self.toggle_fullscreen()
    

    def toggle_fullscreen(self) -> None:
        #TODO
        pass
    
    def quit(self) -> None:
        raise self.Exit

@logger.catch
def main():
    app = App()
    

if __name__ == '__main__':
    main()