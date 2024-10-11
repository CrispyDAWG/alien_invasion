import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from settings import Settings
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images_other/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images_other/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images_other/alien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]

    alien_explosion_images = [pg.image.load(f"images_other/exp{n}.png") for n in range(5)]  # fill in explosion images here
    alien_explosion = [alien_explosion_images]

    ufo_images0  = [pg.image.load(f"images_other/alien3{n}.png") for n in range(2)]
    ufo_images = [ufo_images0]
    n = 0

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.v = v

        type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[type], delta=(type+1)*600, start_index=type % 2)
        self.ufo = Timer(images=Alien.ufo_images[Alien.n], delta=(type+1)*600, start_index=Alien.n % 2)
        self.explosion_timer = Timer(images=Alien.alien_explosion[Alien.n], delta = 1, start_index=Alien.n, loop_continuously=False)

        self.image = self.timer.current_image()
        self.explosion_image = self.explosion_timer.current_image()
        self.image_ufo = self.ufo.current_image()

        print(self.image)

        self.rect = self.image.get_rect()
        self.explosion_rect = self.explosion_image.get_rect()
        self.ufo_rect = self.image_ufo.get_rect(topleft = (0, 40))

        self.index = 0
        self.counter = 0

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.ufo_rect.x = self.ufo_rect.width
        self.ufo_rect.y = self.ufo_rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.ufo_x = float(self.ufo_rect.x)
        self.ufo_y = float(self.ufo_rect.y)

        self.dying = False
        self.dead = False

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return (self.x + self.rect.width >= sr.right or self.x <= 0)
    
    def check_ufo_edges(self):
        self.ufo_rect.x += self.settings.ufo_speed
        if self.ufo_rect.right > self.settings.scr_width:
            self.kill()
        elif self.ufo_rect.left < 0:
            self.kill()

    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        self.ufo_x += self.settings.ufo_speed
        self.image = self.timer.current_image()
        self.explosion_image = self.explosion_timer.current_image()
        self.image_ufo = self.ufo.current_image()
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.ufo_rect.x = self.ufo_x
        self.ufo_rect.y = self.ufo_y
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.image_ufo, self.ufo_rect)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()




