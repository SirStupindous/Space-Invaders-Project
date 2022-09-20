import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer


class Alien(Sprite):
    alien_images = [pg.image.load(f'images/alien{n}.bmp') for n in range(2)]
    alien_explosion_images = [pg.image.load(f'images/explode{n}.png') for n in range(7)]
    
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pg.image.load('images/alien0.bmp')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        
        self.dying = self.dead = False
        self.timer_normal = Timer(image_list=self.alien_images)              
        self.timer_explosion = Timer(image_list=self.alien_explosion_images, is_loop=False)  
        self.timer = self.timer_normal                                    

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    def hit(self):
        self.dying = True 
        self.timer = self.timer_explosion
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect) 


class Aliens:
    def __init__(self, game, screen, settings, lasers: Lasers, ship): 
        self.model_alien = Alien(settings=settings, screen=screen)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.lasers = lasers.lasers    # a laser Group
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.create_fleet()
    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows        
    def reset(self):
        self.aliens.empty()
        self.create_fleet()
    def create_alien(self, alien_number, row_number):
        alien = Alien(settings=self.settings, screen=self.screen)
        alien_width = alien.rect.width

        alien.x = alien_width + 2 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
        self.aliens.add(alien)     
    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                   self.create_alien(alien_number, row_number)
    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break
    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die()
                break
    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.aliens, self.lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()
            self.sb.increment_score()
    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update() 
    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
