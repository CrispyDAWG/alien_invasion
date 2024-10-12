from settings import Settings
from game_stats import GameStats
import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(ai_game=self)

        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.invaders_color = (0, 135, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 100)
        self.invaders_font = pygame.font.SysFont(None, 80)
        self.high_score_font = pygame.font.SysFont(None, 100)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect2 = pygame.Rect(0, 0, self.width, self.height + 100)
        self.back_rect = pygame.Rect(0, 0, self.width, self.height * 2 - 50)

        self.rect.center = self.screen_rect.center
        self.rect2.center = self.screen_rect.center
        self.back_rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def reset_message(self, msg="Play"):
        self.msg = msg
        self._prep_msg(msg)
    
    def high_score(self, msg="High Score"):
        self.msg = msg
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.title = self.title_font.render("Space", True, self.text_color)
        self.invaders = self.invaders_font.render("Invaders", True, self.invaders_color)

        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        msg = "Highscore"
        self.msg_image2 = self.font.render(msg, True, self.text_color,
                self.button_color)
        msg = "Back"
        self.back_image = self.font.render(msg, True, self.text_color, self.button_color)
        
        self.score = self.high_score_font.render(f"High Score: {str(self.stats.high_score)}", True, self.text_color)

        self.title_rect = self.title.get_rect(center=(self.settings.scr_width / 2, self.settings.scr_height / 4))
        self.invaders_rect = self.invaders.get_rect(center=(self.settings.scr_width /2, self.settings.scr_height / 4 + self.height))

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image2_rect = self.msg_image2.get_rect()
        self.back_img_rect = self.back_image.get_rect()

        self.score_rect = (self.rect.x - 110, self.rect.y)

        self.msg_image_rect.center = self.rect.center
        self.msg_image2_rect.center = self.rect2.center
        self.back_img_rect.center = self.back_rect.center

    def draw_button(self):
        self.screen.fill(self.bg_color, self.screen_rect)
        self.screen.fill(self.button_color, self.rect)

        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.invaders, self.invaders_rect)

        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.msg_image2, (self.msg_image2_rect.x, self.msg_image2_rect.y + self.height))