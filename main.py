import pygame as pg
from gameobjects import Grid
from interface import Button


pg.init()
width, height = 500, 500
fps = 60

screen = pg.display.set_mode((width, height), pg.DOUBLEBUF | pg.HWSURFACE)
screen2 = pg.Surface((width, height))
clock = pg.time.Clock()
running = True
grid_size = (20, 20)
node_size = (20, 20)
grid = Grid(0, 0, grid_size, node_size)
interface_components = pg.sprite.Group()


def add_button(*args, **kwargs):
    b = Button(*args, **kwargs)
    interface_components.add(b)


def load_interface():
    add_button(5, height - 25, (100, 20), pg.Color("grey"), text='Next gen', target=next_generation)


def next_generation():
    grid.next_generation()


load_interface()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            grid.update(event)
            interface_components.update(event)
        if event.type == pg.MOUSEMOTION:
            interface_components.update(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                grid.random_generation()
    grid.render(screen2)
    interface_components.draw(screen2)
    screen.blit(screen2, (0, 0))
    pg.display.flip()
    clock.tick(fps)

    pg.display.set_caption(str(round(clock.get_fps())) + ' FPS')

pg.quit()
