import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from alien import Alien
from laser import Lasers
from timer import Timer

# create a ufo class that has an alien that has a random time frame of appearing
# and moving across the screen. If it reaches the end of the screen it disappears
# and the player does not get a bonus score. If the player shoots it, they get a bonus score
# and it disappears. If the player collides with it, they lose a life and it disappears.
# The ufo moves independently of the aliens and gives a random bonus score of 100, 200, or 300.
# The random bonus score is diplayed for four seconds where the ufo was shot and then disappears.

class UFO:
    ufo_images = Alien.alien_images3
    ufo_explosion_images = Alien.alien_explosion_images

    ufo_timer = Timer(image_list=ufo_images)

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load("images/UFO-Enemy-1.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.active = False
        

        self.dying = self.dead = False
        self.sb = game.scoreboard


        self.timer_normal = Alien.alien_timers[self.type]
        self.timer_explosion = Timer(
            image_list=Alien.alien_explosion_images, is_loop=False
        )
        self.timer = self.timer_normal

    # create a countdown timer that counts down the timer and then spawns the ufo
    # the countdown timer should be a random number between 10 and 30 seconds
    # if the timer reaches zero, the ufo is spawned and the timer is reset
    # if the ufo is shot, the timer is reset
    # if the ufo reaches the right side of the screen, the timer is reset
    # if the ufo is alive, set self.active to True
    # if the ufo is dead, set self.active to False

    # def countdown(self):
    #     self.timer -= 1
    #     if self.timer == 0:
    #         self.spawn()
    #         self.timer = randint(10, 30)

    # create a countdown function that counts down the timer and then sets self.active to True
    # the countdown timer should be a random number between 10 and 30 seconds

    def countdown(self):
        new_timer = randint(10, 30)
        new_timer -= 1
        if new_timer == 0:
            self.spawn()


    def spawn(self):
        self.active = True
        self.x = randint(0, self.screen.right)
        self.rect.x = self.x
        print("UFO spawned")
        self.update()

    # create a function called check_edges that checks if the ufo has reached the right side of the screen
    # if the ufo has reached the right side of the screen, remove the ufo and reset the timer
    # if the ufo has not reached the right side of the screen, move the ufo
    def check_edges(self):
        if self.rect.right >= self.screen.get_rect().right:
            return True
        else:
            return False
    
    # def check_edges(self):
    #     if self.rect.right >= self.screen.right or self.rect.left <= 0:
    #         return True
    #     return False

    def hit(self):
        self.score_displayed = True
        self.sb.score += self.score
        print("UFO hit")
        self.reset()

    def move(self):
        self.x += self.settings.ufo_speed_factor
        self.rect.x = self.x


    # create a reset function
    def reset(self):
        print("UFO reset")
        self.active = False
        self.score = randint(100, 300)
        self.score_displayed = False
        self.score_display_time = 0
        self.score_display_time_limit = 4
        self.countdown()
        
        

    def update(self):
        self.draw()
        self.move()
        
        if self.check_edges():
            self.reset()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

