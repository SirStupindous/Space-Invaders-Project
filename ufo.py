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
        self.spawnTimer = randint(1000, 3000)


    # create a countdown function that counts down the timer and then sets self.active to True
    # the countdown timer should be a random number between 10 and 30 seconds
    def countdown(self):
        self.spawnTimer -= 1
        if self.spawnTimer <= 0:
            print("Spawn timer reached 0")
            self.active = True
            self.spawn()


    def spawn(self):
        self.x = 0
        self.rect.x = self.x
        # if self.active == True:
        print("UFO spawned")
        self.update()


    # create a function called check_edges that checks if the ufo has reached the right side of the screen
    # if the ufo has reached the right side of the screen, remove the ufo and reset the timer
    # if the ufo has not reached the right side of the screen, move the ufo
    def check_edges(self):
        if self.rect.right >= self.screen.get_rect().right:
            print("UFO reached right side of screen and will be reset")
            # self.active = False
            self.reset()
            

    # create a function called check_collisions that checks if the player's laser has hit the ufo
    # if the player's laser has hit the ufo, call the hit function
    def check_collisions(self, lasers):
        for laser in lasers:
            if laser.rect.colliderect(self.rect):
                self.hit()


    def hit(self):
        # if the udo is hit by the player's laser, set the ufo to dying
        # if the ufo is dying, update the explosion timer
        # if the explosion timer has finished, set the ufo to dead
        # if the ufo is dead, reset the ufo
        if self.active == True:
            self.dying = True
            self.timer = self.timer_explosion
            self.timer.reset()
            self.sb.score += randint(100, 300)
            print("UFO HIT!!! You received a bonus score of " + str(self.sb.score) + " points")
            self.reset()


    # create a reset function
    def reset(self):
        print("UFO reset")
        self.active = False
        self.rect.x = 0 # self.screen.get_rect().left
        self.spawnTimer = randint(1000, 3000)
        self.countdown()


    def update(self):
        # if the ufo is active, move the ufo from the left side of the screen to the right side of the screen
        # if the ufo is not active, countdown the timer and then spawn the ufo
        if self.active == True:
            self.x += self.settings.ufo_speed_factor
            self.rect.x = self.x
            self.draw()
            self.check_edges()
            # self.check_collisions(self.ship_lasers.lasers)
        else:
            self.countdown()

        # if the ufo is dying, update the explosion timer
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.dying = True
        if self.dying:
            self.timer_explosion.update()
            # if the explosion timer has finished, set the ufo to dead
            if self.timer_explosion.finished:
                self.dead = True
                # self.active = False
                self.dying = False
                self.reset()


    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

