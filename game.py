from this import s
import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers, LaserType
from alien import Aliens
from ufo import UFO
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from button import LaunchScreen
from barrier import Barriers
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")

        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)

        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.ufo = UFO(game=self, type=3, color=(255, 0, 255))
        self.settings.initialize_speed_settings()

        self.launch_screen = LaunchScreen(
            game=self, screen=self.screen, settings=self.settings
        )

    def reset(self):
        print("Resetting game...")
        # self.lasers.reset()
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.ufo.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print("All ships gone: game over!")
        self.sound.gameover()
        self.reset()
        self.scoreboard.reset()
        self.ship.ships_left = 3
        self.settings.game_active = False
        self.sound.play_bg()

    def play(self):
        self.sound.play_bg()
        switch_one, switch_two, switch_three = False, False, False

        while (
            True
        ):  # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            gf.check_events(
                settings=self.settings,
                ship=self.ship,
                launch_screen=self.launch_screen,
            )


            if self.settings.game_active and not self.settings.score_screen:
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.ufo.update()
                self.barriers.update()
                # self.lasers.update()
                self.scoreboard.update()
            elif not self.settings.game_active and not self.settings.score_screen:
                self.launch_screen.update()
            elif self.settings.score_screen and not self.settings.game_active:
                self.launch_screen.update_score()

            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
