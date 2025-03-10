import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from settings import Settings
from pygame.sprite import Sprite
from timer import Timer
from random import randint
import pygame.font

class Ufo(Sprite):
    ufo_images0  = [pg.image.load(f"images_other/alien3{n}.png") for n in range(2)]
    ufo_images = [ufo_images0]
    n = 0
    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.vec = v


        type = randint(0, 2)
        self.timer = Timer(images=Ufo.ufo_images[Ufo.n], delta=(type+1)*600, start_index=type % 2)
        self.ufo_image = Timer(images=Ufo.ufo_images[0], start_index=0)
        self.image = self.timer.current_image()
        self.ufo = self.ufo_image.current_image()

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.ufo_font = pygame.font.SysFont(None, 80)
        self.ufo_text = (255, 0, 0)
        self.ufo_points = self.ufo_font.render(f"{round(self.settings.ufo_points)}", True,  self.ufo_text)
        self.points_rect = self.ufo_points.get_rect()

    def check_ufo_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return (self.x + self.rect.width >= sr.right or self.x <= 0)
    
    def update(self):
        self.x += self.settings.ufo_speed
        self.image = self.timer.current_image()
        self.draw()

    def draw(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (self.rect.x, self.rect.y - 40))

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()