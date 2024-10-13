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

    n = 0

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.v = v

        type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[type], delta=(type+1)*600, start_index=type % 2)
        self.alien1 = Timer(images=Alien.alien_images[0], start_index=0)
        self.alien2 = Timer(images=Alien.alien_images[1], start_index=0)
        self.alien3 = Timer(images=Alien.alien_images[2], start_index=0)
        self.explosion_timer = Timer(images=Alien.alien_explosion[Alien.n], delta=(type+1)*600, start_index=Alien.n)

        self.image = self.timer.current_image()
        self.explosion_image = self.explosion_timer.current_image()
        self.alien1_image = self.alien1.current_image()
        self.alien2_image = self.alien2.current_image()
        self.alien3_image = self.alien3.current_image()

        print(self.image)

        self.rect = self.image.get_rect()
        self.explosion_rect = self.explosion_image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.explosion_rect.x = self.explosion_rect.width
        self.explosion_rect.y = self.explosion_rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.ex_x = float(self.explosion_rect.x)
        self.ex_y = float(self.explosion_rect.y)

        self.dying = False
        self.dead = False

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return (self.x + self.rect.width >= sr.right or self.x <= 0)


    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        self.image = self.timer.current_image()
        self.explosion_image = self.explosion_timer.current_image()
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (self.rect.x, self.rect.y + 40))
        self.screen.blit(self.explosion_image, (self.ex_x, self.ex_y))



def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()




