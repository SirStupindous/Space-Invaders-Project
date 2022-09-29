import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from laser import Lasers
from timer import Timer


class Alien(Sprite):
    # alien_images = []
    # for n in range(2):
    #     alien_images.append(pg.image.load(f'images/alien{n}.bmp'))

    # alien_images = [pg.image.load(f"images/alien{n}.bmp") for n in range(2)]

    alien_images2 = [pg.image.load(f"images/alien-0{n}.png") for n in range(1, 4)]
    alien_images1 = [pg.image.load(f"images/alien-1{n}.png") for n in range(1, 7)]
    alien_images0 = [pg.image.load(f"images/alien-2{n}.png") for n in range(1, 4)]
    alien_images3 = [pg.image.load(f"images/UFO-Enemy-{n}.png") for n in range(1, 4)]

    # alien_types = {0: alien_images0, 1 : alien_images1, 2: alien_images2, 3: alien_images3}
    alien_timers = {
        0: Timer(image_list=alien_images0),
        1: Timer(image_list=alien_images1),
        2: Timer(image_list=alien_images2),
        3: Timer(image_list=alien_images3),
    }

    alien_explosion_images = [
        pg.image.load(f"images/Explosion-{n}.png") for n in range(1, 11)
    ]

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load("images/alien0.bmp")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type

        self.dying = self.dead = False
        self.sb = game.scoreboard

        # self.timer_normal = Timer(image_list=self.alien_images)
        # self.timer_normal = Timer(image_list=self.alien_types[type])

        self.timer_normal = Alien.alien_timers[self.type]
        self.timer_explosion = Timer(
            image_list=Alien.alien_explosion_images, is_loop=False
        )
        self.timer = self.timer_normal

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(
            ship.rect
        )

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            self.sb.increment_score(self.type)

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += settings.alien_speed_factor * settings.fleet_direction
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)


class Aliens:
    def __init__(self, game):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()

        # self.ship_lasers = game.ship.lasers.lasers    # a laser Group
        # self.aliens_lasers = Lasers(settings=game.settings)

        self.ship_lasers = game.ship_lasers.lasers  # a laser Group
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows

    def reset(self):
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()

    def create_alien(self, alien_number, row_number):
        # if row_number > 5: raise ValueError('row number must be less than 6')
        type = row_number // 2
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
        number_rows = self.get_number_rows(
            self.ship.rect.height, self.model_alien.rect.height
        )
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
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print("Aliens all gone!")
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(
                    game=self.game, x=alien.rect.centerx, y=alien.rect.bottom
                )
            i += 1

    def check_collisions(self):
        # ship_lasers hitting an alien
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()

        # ship_lasers hitting a barrier
        collisions = pg.sprite.groupcollide(
            self.game.barriers.barriers, self.ship_lasers, False, True
        )
        if collisions:
            for barrier in collisions:
                barrier.hit()

        # ship_lasers hitting an aliens_lasers
        # collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers, True, True)
        # if collisions:
        #     for alien_laser in collisions:
        #         alien_laser.hit()
        #     for ship_laser in collisions:
        #         ship_laser.hit()

        # alien_lasers hitting the ship
        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        # alien_lasers hitting a barrier
        collisions = pg.sprite.groupcollide(
            self.game.barriers.barriers, self.aliens_lasers.lasers, False, True
        )
        if collisions:
            for barrier in collisions:
                barrier.hit()

        # alien_lasers hitting a ship_lasers
        # collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers, True, True)
        # if collisions:
        #     for alien_laser in collisions:
        #         alien_laser.hit()
        #     for ship_laser in collisions:
        #         ship_laser.hit()

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:  # set True once the explosion animation has completed
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()
