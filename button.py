from pickle import TRUE
import pygame as pg
from alien import Alien

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (20, 20, 20)


class Button:
    def __init__(self, settings, screen, msg, x, y, color):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = GRAY
        self.text_color = color
        self.font = pg.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = x, y

        # The button message needs to be prepped only once.
        self.prep_msg(msg)
        self.settings = settings

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def update(self):
        self.draw_button()


class LaunchScreen:
    def __init__(self, game, screen, settings):
        self.game = game
        self.screen = screen
        self.settings = settings

        self.alien0 = Alien(game=self.game, type=2)
        self.alien1 = Alien(game=self.game, type=1)
        self.alien2 = Alien(game=self.game, type=0)
        self.alien3 = Alien(game=self.game, type=3)

        self.play_button = Button(
            settings=self.settings,
            screen=self.screen,
            msg="PLAY GAME",
            x=self.settings.screen_width / 2,
            y=600,
            color=(GREEN),
        )

        self.score_button = Button(
            settings=self.settings,
            screen=self.screen,
            msg="HIGH SCORES",
            x=self.settings.screen_width / 2,
            y=700,
            color=WHITE,
        )

        self.back_button = Button(
            settings=self.settings,
            screen=self.screen,
            msg="BACK",
            x=80,
            y=30,
            color=WHITE,
        )

    def update_aliens_coordinates(self):
        self.alien0.rect.x = self.settings.screen_width / 2 - 100
        self.alien0.rect.y = self.settings.screen_height / 2 - 100
        self.alien1.rect.x = self.settings.screen_width / 2 - 100
        self.alien1.rect.y = self.settings.screen_height / 2 - 50
        self.alien2.rect.x = self.settings.screen_width / 2 - 100
        self.alien2.rect.y = self.settings.screen_height / 2
        self.alien3.rect.x = self.settings.screen_width / 2 - 100
        self.alien3.rect.y = self.settings.screen_height / 2 + 40

    def check_button(self, mouse_x, mouse_y):
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self.settings.game_active = True
        elif self.score_button.rect.collidepoint(mouse_x, mouse_y):
            self.settings.score_screen = True
        elif self.back_button.rect.collidepoint(mouse_x, mouse_y):
            self.settings.score_screen = False

    def draw_words_on_screen(self):
        # Space
        title_font = pg.font.SysFont(None, 150)
        space_text = title_font.render("SPACE", True, WHITE, GRAY)
        space_text_rect = space_text.get_rect()
        space_text_rect.center = (self.settings.screen_width / 2, 100)
        self.screen.blit(space_text, space_text_rect)

        # Invaders
        invader_font = pg.font.SysFont(None, 80)
        invader_text = invader_font.render("INVADERS", True, GREEN, GRAY)
        invader_text_rect = invader_text.get_rect()
        invader_text_rect.center = (self.settings.screen_width / 2, 165)
        self.screen.blit(invader_text, invader_text_rect)

        # = 20 PTS
        points_font = pg.font.SysFont(None, 50)
        points_text_20 = points_font.render("= 20 PTS", True, WHITE, GRAY)
        points_text_20_rect = points_text_20.get_rect()
        points_text_20_rect.center = (
            self.settings.screen_width / 2 + 20,
            self.settings.screen_height / 2 - 35,
        )
        self.screen.blit(points_text_20, points_text_20_rect)

        # = 10 PTS
        points_text_10 = points_font.render("= 10 PTS", TRUE, WHITE, GRAY)
        points_text_10_rect = points_text_10.get_rect()
        points_text_10_rect.center = (
            self.settings.screen_width / 2 + 20,
            self.settings.screen_height / 2 - 85,
        )
        self.screen.blit(points_text_10, points_text_10_rect)

        # = 40 PTS
        points_text_40 = points_font.render("= 40 PTS", TRUE, WHITE, GRAY)
        points_text_40_rect = points_text_40.get_rect()
        points_text_40_rect.center = (
            self.settings.screen_width / 2 + 20,
            self.settings.screen_height / 2 + 10,
        )
        self.screen.blit(points_text_40, points_text_40_rect)

        # = ???
        points_text_unknown = points_font.render("= ???", TRUE, WHITE, GRAY)
        points_text_unknown_rect = points_text_unknown.get_rect()
        points_text_unknown_rect.center = (
            self.settings.screen_width / 2 + 20,
            self.settings.screen_height / 2 + 55,
        )
        self.screen.blit(points_text_unknown, points_text_unknown_rect)

    def draw(self):
        self.screen.fill(GRAY)
        self.update_aliens_coordinates()
        self.draw_words_on_screen()
        self.alien0.draw()
        self.alien1.draw()
        self.alien2.draw()
        self.alien3.draw()
        self.play_button.update()
        self.score_button.update()

    def update(self):
        self.draw()

    def read_scores_from_file(self):
        text = []
        file = open("high_scores.txt")
        for line in file:
            text.append(line)

        x, y = self.settings.screen_width / 2, self.settings.screen_height / 2 - 200
        font = pg.font.SysFont(None, 50)

        for item in text:
            item = item[:-1]
            score = font.render(item, TRUE, WHITE, GRAY)
            score_rect = score.get_rect()
            score_rect.center = (x, y)
            self.screen.blit(score, score_rect)
            y += 50

    def draw_score(self):
        self.screen.fill(GRAY)

        # Draws 'High score' onto screen
        high_score_font = pg.font.SysFont(None, 100)
        high_score = high_score_font.render("HIGH SCORES", TRUE, WHITE, GRAY)
        high_score_rect = high_score.get_rect()
        high_score_rect.center = (
            self.settings.screen_width / 2,
            100,
        )
        self.screen.blit(high_score, high_score_rect)

        self.read_scores_from_file()

        self.back_button.update()

    def update_score(self):
        self.draw_score()
