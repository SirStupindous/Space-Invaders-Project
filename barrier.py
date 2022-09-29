import pygame as pg
from pygame.sprite import Sprite, Group


class Barrier(Sprite):
    color = 255, 0, 0
    black = 0, 0, 0

    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.settings = game.settings

        # self.settings = game.settings
        # self.image = pg.image.load('images/alien0.bmp')
        # self.rect = self.image.get_rect()
        # self.rect.y = self.rect.height
        # self.x = float(self.rect.x)

    def hit(self):
        pass

    def update(self):
        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(
            self.screen,
            self.settings.bg_color,
            (self.rect.centerx, self.rect.bottom),
            self.rect.width / 6,
        )


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.create_barriers()

    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        rects = [
            pg.Rect(x * 2 * width + 1.5 * width, top, width, height) for x in range(4)
        ]  # SP w  3w  5w  7w  SP
        self.barriers = [Barrier(game=self.game, rect=rects[i]) for i in range(4)]

    def hit(self):
        pass

    def reset(self):
        self.create_barriers()

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    # def draw(self):
    #     for barrier in self.barriers: barrier.draw()
