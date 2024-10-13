import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from settings import Settings
from pygame.sprite import Sprite
from timer import Timer
from random import randint
import pygame.font

class Explosions(Sprite):
    alien_explosion_images = [pg.image.load(f"images_other/exp0{n}.png") for n in range(2)]
    alien_explosion = [alien_explosion_images]
    n = 0
    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.timer = Timer(images=Explosions.alien_explosion[Explosions.n], delta=500, start_index=Explosions.n, loop_continuously=False)
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.start_time = pg.time.get_ticks()

    def update(self):
        current_time = pg.time.get_ticks()
        timespan = 1000
        if current_time > self.start_time + timespan:
             self.kill()
        self.image = self.timer.current_image()
        self.draw()
    
    def draw(self): 
        self.screen.blit(self.image, self.rect)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()