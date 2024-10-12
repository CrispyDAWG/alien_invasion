import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from settings import Settings
from pygame.sprite import Sprite
from timer import Timer
from random import randint

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
        self.ufo = Timer(images=Ufo.ufo_images[Ufo.n], delta=(type+1)*600, start_index=Ufo.n % 2)
        self.image_ufo = self.ufo.current_image()
        self.ufo_rect = self.image_ufo.get_rect() 

        self.ufo_rect.x = self.ufo_rect.width
        self.ufo_rect.y = self.ufo_rect.height

        self.ufo_x = float(self.ufo_rect.x)
        self.ufo_y = float(self.ufo_rect.y)

    def check_ufo_edges(self):
        sr = self.screen.get_rect()
        self.ufo_rect.x = self.ufo_x
        return (self.ufo_x + self.ufo_rect.width >= sr.right or self.ufo_x <= 0)
    
    def update(self):
        self.ufo_x += self.settings.ufo_speed
        self.image_ufo = self.ufo.current_image()
        self.draw()

    def draw(self):
        self.ufo_rect.x = self.ufo_x
        self.ufo_rect.y = self.ufo_y
        self.screen.blit(self.image_ufo, (self.ufo_rect.x, self.ufo_rect.y - 40))




def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()