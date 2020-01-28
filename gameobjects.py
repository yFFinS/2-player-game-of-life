import pygame as pg
import random as rnd


class Node(pg.sprite.Sprite):
    color = {0: pg.Color("black"), 1: pg.Color("blue"), 2: pg.Color("red")}
    FIRSTPLAYER = 1
    SECONDPLAYER = 2
    DEAD = 0

    def __init__(self, x: int, y: int, size: tuple, group=None) -> None:
        super().__init__()
        if group is not None:
            self.add(group)
        self.is_alive = False
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.__change_to = None
        self.condition = Node.DEAD
        self.preloaded = False

    def change(self, change_to=None) -> None:
        if change_to is not None:
            next_condition = change_to
        else:
            next_condition = self.__change_to
        self.is_alive = next_condition != Node.DEAD
        self.image.fill(Node.color[next_condition])
        self.condition = next_condition
        self.__change_to = None
        self.preloaded = False

    def get_pos(self) -> tuple:
        return self.rect.topleft

    def preload_next_change(self, change_to: int) -> None:
        self.image.fill(Node.color[self.condition])
        rect = pg.rect.Rect(0, 0, self.rect.w // 2, self.rect.h // 2)
        rect.center = (self.rect.w // 2, self.rect.h // 2)
        pg.draw.rect(self.image, Node.color[change_to], rect)
        self.__change_to = change_to
        self.preloaded = True

    def reload(self):
        self.image.fill(Node.color[self.condition])
        self.__change_to = None
        self.preloaded = False


class Grid:
    NEIGHBOURS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    CYCLIC = 1
    NONCYCLIC = 2

    def __init__(self, x: int, y: int, grid_size=(1, 1), node_size=(30, 30)) -> None:
        self.current_player = 1
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.node_size = node_size
        self.game_mode = Grid.CYCLIC
        self.nodes = pg.sprite.Group()
        self.lines = self.__create_grid_lines()
        self.grid = [[Node(x + i * node_size[0], y + j * node_size[1], node_size, self.nodes)
                      for j in range(self.grid_size[1])] for i in range(self.grid_size[0])]

        self.__to_change = None

    def __change_node(self, node):
        node.change(Node.DEAD if node.is_alive else Node.FIRSTPLAYER)

    def __collide(self, x, y):
        return 0 <= x - self.x <= self.grid_size[0] * self.node_size[0] \
               and 0 <= y - self.y <= self.grid_size[1] * self.node_size[1]

    def __create_grid_lines(self):
        line_color = pg.Color("white")
        group = pg.sprite.Group()
        vertical_line_width = self.node_size[0] // 10
        vertical_line_length = self.node_size[1] * self.grid_size[1]
        horizontal_line_width = self.node_size[1] // 10
        horizontal_line_length = self.node_size[0] * self.grid_size[0]
        for x in range(self.grid_size[0] + 1):
            line = pg.sprite.Sprite(group)
            line.image = pg.Surface((vertical_line_width, vertical_line_length))
            line.image.fill(line_color)
            line.rect = line.image.get_rect()
            line.rect.topleft = (x * self.node_size[0] - vertical_line_width // 2, 0)

        for y in range(self.grid_size[1] + 1):
            line = pg.sprite.Sprite(group)
            line.image = pg.Surface((horizontal_line_length, horizontal_line_width))
            line.image.fill(line_color)
            line.rect = line.image.get_rect()
            line.rect.topleft = (0, y * self.node_size[1] - horizontal_line_width // 2)

        return group

    def __get_node_at(self, x, y):
        for node in self.nodes:
            if node.rect.collidepoint(x, y):
                return node

    def __get_neighbours(self, node):
        x, y = node.get_pos()
        x //= self.node_size[0]
        y //= self.node_size[1]
        nb = []
        for dx, dy in Grid.NEIGHBOURS:
            if self.game_mode == Grid.NONCYCLIC:
                x2, y2 = x + dx, y + dy
                if -1 < x2 < self.grid_size[0] and -1 < y2 < self.grid_size[1]:
                    nb.append(self.grid[x2][y2])
            if self.game_mode == Grid.CYCLIC:
                x2, y2 = (x + dx) % self.grid_size[0], (y + dy) % self.grid_size[1]
                nb.append(self.grid[x2][y2])
        return nb

    def __get_node_by_index(self, xi, yi):
        try:
            return self.grid[xi][yi]
        except IndexError:
            return

    def preload_next_generation(self) -> None:
        self.__to_change = []
        for node in self.nodes:
            nb = self.__get_neighbours(node)
            alive = len(list(filter(lambda x: x.is_alive, nb)))
            if node.is_alive and not 2 <= alive <= 3 or not node.is_alive and alive == 3:
                self.__to_change.append(node)
                node.preload_next_change(Node.DEAD if node.is_alive else Node.FIRSTPLAYER)
            elif node.preloaded:
                node.reload()

    def next_generation(self) -> None:
        if self.__to_change is None:
            self.preload_next_generation()
        for node in self.__to_change:
            self.__change_node(node)
        self.preload_next_generation()

    def random_generation(self):
        for node in self.nodes:
            if rnd.random() < 0.4:
                node.change(rnd.choice([Node.DEAD, Node.FIRSTPLAYER]))
        self.preload_next_generation()

    def render(self, screen: pg.Surface) -> None:
        self.nodes.draw(screen)
        self.lines.draw(screen)

    def update(self, event: pg.event.EventType) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                collision = self.__get_node_at(*event.pos)
                if collision:
                    self.__change_node(collision)
                    self.preload_next_generation()
