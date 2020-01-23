import pygame as pg
from gameobjects import Grid


pg.init()
width, height = 500, 500
fps = 60

screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
running = True
grid = Grid(0, 0, 10, 10)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    grid.render(screen)
    pg.display.flip()
    clock.tick(fps)
    pg.display.set_caption(str(round(clock.get_fps())) + ' FPS')

pg.quit()