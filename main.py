import pygame as pg
from gameobjects import Grid


pg.init()
width, height = 500, 500
fps = 60

screen = pg.display.set_mode((width, height), pg.DOUBLEBUF, pg.RESIZABLE)
clock = pg.time.Clock()
running = True
grid_size = (20, 20)
grid = Grid(0, 0, grid_size, (width // grid_size[0], height // grid_size[1]))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            grid.update(event)
        if event.type == pg.KEYDOWN:
            grid.next_generation()
    grid.render(screen)

    pg.display.flip()
    clock.tick(fps)

    pg.display.set_caption(str(round(clock.get_fps())) + ' FPS')

pg.quit()