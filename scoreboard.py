import pygame as pg

# import pygame.font


class Scoreboard:
    def __init__(self, game):
        self.score = 0
        self.level = 0
        self.high_score = 0

        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None
        self.score_rect = None
        self.prep_score()

    def increment_score(self, type):
        if type == 2:
            self.score += self.settings.alien0_points
        if type == 1:
            self.score += self.settings.alien1_points
        if type == 0:
            self.score += self.settings.alien2_points
        if type == 3:
            self.score += self.settings.alien3_points
        self.prep_score()

    def prep_score(self):
        score_str = str(self.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def check_for_high_score(self):
        text = []
        file = open("high_scores.txt", "r")

        for line in file:
            text.append(int(line[3:]))

        file.close()
        file = open("high_scores.txt", "w")

        for num in text:
            # new high score
            if self.score >= num:
                text.insert(text.index(num), self.score)
                del text[-1]
                break

        n = 1

        for num in text:
            file.write(str(n) + ". " + str(num) + "\n")
            n += 1

    def reset(self):
        self.check_for_high_score()
        self.score = 0
        self.prep_score()
        self.update()

    def update(self):
        # TODO: other stuff
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
