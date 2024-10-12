import sys
import pygame as pg
from colors import OFF_WHITE, DARK_GREY
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from event import Event
from barrier import Barriers
from sound import Sound


class AlienInvasion:
    def __init__(self):
        pg.init()   
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()

        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(ai_game=self)

        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.first = True
        self.score_button = False

        self.play_button = Button(self, "Play")
        self.high_score = Button(self, "High Score")
        self.back = Button(self,"Back")
        self.event = Event(self)

    def game_over(self):
        self.restart_game()
        print("Game over!") 
        self.sound.play_gameover()
        self.game_active = False
        pg.mouse.set_visible(True)

    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.sound.play_background()

        self.ship.reset_ship()
        self.fleet.reset_fleet()
        self.fleet.reset_ufo()
        pg.mouse.set_visible(False)
    
    def game_high_score(self):
        self.game_active = False
        self.score_button = True
        self.screen.fill(self.bg_color)
        self.screen.blit(self.high_score.score, self.high_score.score_rect)
        self.screen.blit(self.back.back_image, (self.back.back_img_rect.x, 
                                                      (self.back.back_img_rect.y * 2) - 10))

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.play_button.reset_message("Play again? (q for quit)")
        self.reset_game()

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        while not self.finished:
            self.finished = self.event.check_events()
            if self.first or self.game_active:
                self.first = False
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()

            if not self.game_active and not self.score_button:
                self.play_button.draw_button()
            pg.display.flip()
            self.clock.tick(60)
        sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
