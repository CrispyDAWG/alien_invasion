import pygame as pg
import random 
from vector import Vector
from point import Point
from laser import Laser 
from settings import Settings
from pygame.sprite import Sprite
from timer import Timer
from random import randint
from alien_laser import AlienLaser

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images_other/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images_other/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images_other/alien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]

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

        self.image = self.timer.current_image()

        self.alien1_image = self.alien1.current_image()
        self.alien2_image = self.alien2.current_image()
        self.alien3_image = self.alien3.current_image()

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dying = False
        self.dead = False
        
        # New attributes for shooting
        self.alien_lasers = pg.sprite.Group()
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = random.randint(1000, 20000)  # Random delay between 1-3 seconds


    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return (self.x + self.rect.width >= sr.right or self.x <= 0)

    def alien_shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_delay = random.randint(1000, 3000)  # Reset the delay
            new_laser = AlienLaser(self.ai_game, self)
            self.alien_lasers.add(new_laser)
            
    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        self.image = self.timer.current_image()
        self.alien_shoot()
        self.alien_lasers.update()  # Changed from 'lasers' to 'alien_lasers'
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (self.rect.x, self.rect.y + 40))
        for alien_laser in self.alien_lasers:
            alien_laser.draw()  # Using AlienLaser's draw method directly

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
    
