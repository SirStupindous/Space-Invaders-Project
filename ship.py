import pygame as pg
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from sys import exit


class Ship(Sprite):
    def __init__(self, game, settings, screen, sound, lasers=None):
        super().__init__()
        self.game = game
        self.screen = screen
        self.settings = settings
        self.sound = sound
        self.ships_left = settings.ship_limit  
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()
        self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0
    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)
    def reset(self): 
        self.vel = Vector()
        self.posn = self.center_ship()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
    def die(self):
# # TODO: reduce the ships_left, 
# #       reset the game if ships > 0
# #       game_over if the ships == 0
        self.ships_left -= 1
        print(f'Ship is dead! Only {self.ships_left} ships left')
        self.game.reset() if self.ships_left > 0 else self.game.game_over()
    def update(self):
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(settings=self.settings, screen=self.screen,
                                ship=self, sound=self.sound)
        self.draw()
    def draw(self): 
        self.screen.blit(self.image, self.rect)
