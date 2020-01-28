import pygame as pg


class ClickableObject(pg.sprite.Sprite):

    def __init__(self, x: int, y: int, size: tuple, color: pg.color.Color,
                 text='', text_color=(0, 0, 0), target=None, args=()) -> None:
        super().__init__()
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.target = target
        self.args = args
        self.hovered = False
        self.font = pg.font.Font(None, 20)
        self.update_text()

    def press(self) -> None:
        if self.target is not None:
            self.target(*self.args)

    def update(self, event: pg.event.EventType) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            if self.rect.collidepoint(*event.pos):
                self.press()
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(*event.pos):
                if not self.hovered:
                    self.hovered = True
                    self.image.set_alpha(168)
            else:
                if self.hovered:
                    self.hovered = False
                    self.image.set_alpha(255)

    def update_text(self, text=None) -> None:
        self.image.fill(self.color)
        if text is not None:
            self.text = str(text)
        text_renderer = self.font.render(self.text, True, self.text_color)
        rect = text_renderer.get_rect()
        rect.center = (self.rect.w // 2, self.rect.h // 2)
        self.image.blit(text_renderer, (0, 0))


class Button(ClickableObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)