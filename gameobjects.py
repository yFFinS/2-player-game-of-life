import pygame as pg


class Node(pg.sprite.Sprite):
    color = {1: pg.Color("red"), 2: pg.Color("blue"), 3: pg.Color("green")}

    def __init__(self, x, y, size, is_alive=False, player=1, group=None):
        super().__init__()
        if group:
            self.add(group)
        self.is_alive = is_alive
        self.player = player
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Grid:
    def __init__(self, x, y, width=0, height=0, node_size=(30, 30)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.node_size = node_size
        self.node_group = pg.sprite.Group()
        self.lines_group = self.create_grid_lines()
        self.grid = [[Node(x + i * node_size[0], y + j * node_size[1], node_size, self.node_group)
                      for j in range(height)] for i in range(width)]

    def render(self, screen):
        self.node_group.draw(screen)
        self.lines_group.draw(screen)

    def create_grid_lines(self) -> pg.sprite.Group:
        line_color = pg.Color("white")
        group = pg.sprite.Group()
        vertical_line_width = self.node_size[0] // 10
        vertical_line_length = self.node_size[1] * self.height
        horizontal_line_width = self.node_size[1] // 10
        horizontal_line_length = self.node_size[0] * self.width
        for x in range(self.width + 1):
            line = pg.sprite.Sprite(group)
            line.image = pg.Surface((vertical_line_width, vertical_line_length))
            line.image.fill(line_color)
            line.rect = line.image.get_rect()
            line.rect.topleft = (x * self.node_size[0] - vertical_line_width // 2, 0)

        for y in range(self.height + 1):
            line = pg.sprite.Sprite(group)
            line.image = pg.Surface((horizontal_line_length, horizontal_line_width))
            line.image.fill(line_color)
            line.rect = line.image.get_rect()
            line.rect.topleft = (0, y * self.node_size[1] - horizontal_line_width // 2)

        return group
