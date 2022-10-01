import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from alien import Alien
from laser import Lasers
from timer import Timer


class UFO:
    ufo_images = Alien.alien_images3
    ufo_explosion_images = Alien.alien_explosion_images

    ufo_timer = Timer(image_list=ufo_images)

    def __init__(self, game, type, color):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load("images/UFO-Enemy-1.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.active = False
        self.text_color = color
        self.font = pg.font.SysFont(None, 48)

        self.dying = self.dead = False
        self.sb = game.scoreboard

        self.ship_lasers = game.ship_lasers.lasers  # a laser Group

        self.timer_normal = Alien.alien_timers[self.type]
        self.timer_explosion = Timer(
            image_list=Alien.alien_explosion_images, is_loop=False
        )
        self.timer = self.timer_normal
        self.spawnTimer = randint(1000, 5000)
        self.pointTimer = 0
        self.countdown()
        self.prep_msg(str(self.settings.ufo_points))


    # create a countdown function that counts down the timer and then sets self.active to True
    def countdown(self):
        self.spawnTimer -= 1
        if self.spawnTimer <= 0:
            self.active = True
            self.spawn()


    def spawn(self):
        self.x = 0
        self.rect.x = self.x
        self.update()


    # if the ufo has reached the right side of the screen, remove the ufo and reset the timer
    # if the ufo has not reached the right side of the screen, move the ufo
    def check_edges(self):
        if self.rect.right >= self.screen.get_rect().right:
            self.reset()
            

    # if the player's laser has hit the ufo, call the hit function
    def check_collisions(self):
        for laser in self.ship_lasers:
            if laser.rect.colliderect(self.rect):
                self.hit()


    def hit(self):
        # if the ufo is hit by the player's laser, set the ufo to dying
        # if the ufo is dead, reset the ufo
        self.pointTimer = 1000
        if self.active == True:
            self.timer.reset()
            self.sb.score += self.settings.ufo_points
            self.prep_msg(str(self.settings.ufo_points))
            self.reset()


    # create a reset function
    def reset(self):
        self.active = False
        self.rect.x = 0
        self.settings.ufo_points = randint(100, 500)
        self.spawnTimer = randint(1000, 5000)
        self.countdown()


    def update(self):
        # if the ufo is active, move the ufo from the left side of the screen to the right side of the screen
        # if the ufo is not active, countdown the timer and then spawn the ufo
        if self.active == True:
            self.x += self.settings.ufo_speed_factor
            self.rect.x = self.x
            self.draw()
            self.check_edges()
            self.check_collisions()
        else:
            self.countdown()
        
        if self.pointTimer >= 0:
            self.draw_score()
            

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

    
    def prep_msg(self, msg):
        # Turn msg into a rendered image and center text on the button.
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.rect.right, self.rect.top


    def draw_score(self):
        # Draw blank button and then draw message.
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.pointTimer -= 1


