import pygame as pg
from vector import Vector
from point import Point
from laser import Laser
from timer import Timer
from sound import Sound

from alien import Alien
from ufo import Ufo
from pygame.sprite import Sprite

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.ufo_group = pg.sprite.GroupSingle()
        self.fleet_lasers = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        self.vec = Vector(self.settings.alien_speed, 0)
        self.alien = Alien(ai_game=ai_game, v=self.v)
        self.lasers = Laser(ai_game=self)
        self.ufo = Ufo(ai_game=ai_game, v=self.v)
        self.sound = Sound()

        self.dead = False
        self.explosion = False
        self.center = 0

        # self.aliens.add(alien)
        self.spacing = 1.4
        self.create_fleet()
        self.create_ufo()
        # self.create_row()

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()
    
    def reset_ufo(self):
        self.ufo_group.empty()
        self.create_ufo()

    def create_fleet(self):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        current_y = alien_height
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            self.create_row(current_y)
            current_y += self.spacing * alien_height
        
    def create_row(self, y):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        current_x = alien_width 
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
             new_alien = Alien(self, v=self.v)
             new_alien.rect.y = y
             new_alien.y = y
             new_alien.x = current_x
             new_alien.rect.x = current_x
             self.aliens.add(new_alien)
             current_x += self.spacing * alien_width
    
    def create_ufo(self): 
        new_ufo = Ufo(ai_game=self.ai_game, v=self.vec)
        new_ufo.rect.y = new_ufo.rect.height
        new_ufo.y = new_ufo.rect.height
        new_ufo.x = new_ufo.rect.width
        new_ufo.rect.x = new_ufo.rect.width
        self.ufo_group.add(new_ufo)

    def create_explosions(self): 
        explode = Alien(ai_game=self.ai_game, v=self.vec)
        explode.explosion_rect.y = explode.rect.height
        explode.ex_y = explode.rect.height
        explode.ex_x = explode.rect.width
        explode.explosion_rect.x = explode.rect.width
        self.explosions.add(explode)
        

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True
        return False
    
    def check_ufo_edges(self):
        for ufo in self.ufo_group:
            if ufo.check_ufo_edges():
                return True
        return False
    
    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False
    def update(self):
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                for i in  aliens:
                    self.screen.blit(self.alien.explosion_image, aliens[0].rect.center)
                # self.center = aliens[0].rect.center
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            # self.screen.blit(self.alien.explosion_image, self.center)


        collisions = pg.sprite.groupcollide(self.ship.lasers, self.ufo_group, True, True)
        if collisions:
            for ufo in collisions.values():
                self.screen.blit(self.ufo.ufo_points, (ufo[0].rect.centerx, ufo[0].rect.centery))
                self.stats.score += round(self.settings.ufo_points)  * len(ufo)
            self.sb.prep_score()
            self.sb.check_high_score()

        
        if len(self.aliens) == 30:
            self.v.x = self.settings.fleet_increase_speed * 2
        elif len(self.aliens) == 15:
            self.v.x = self.settings.fleet_increase_speed * 2.5
        elif len(self.aliens) == 0:
            self.v.x = self.settings.alien_speed

        if not self.aliens and not self.ufo_group:
            self.v.x = self.settings.alien_speed          
            self.ship.lasers.empty()
            self.create_fleet()
            self.create_ufo()
            self.stats.level += 1
            if  self.stats.level == 2:
                pg.mixer.music.load('sounds/DS3_speedup.wav')
                pg.mixer.music.set_volume(1.5)
                self.sound.play_background()
            elif self.stats.level == 4:
                pg.mixer.music.load('sounds/DS3_speedup2.wav')
                pg.mixer.music.set_volume(1.5)
                self.sound.play_background()
            self.sb.prep_level()
            return
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self.screen.blit(self.alien.explosion_image, self.ship.rect.center)
            self.v.x = self.settings.alien_speed
            print("Ship hit!")
            self.ship.ship_hit()
            return
        
        if pg.sprite.spritecollideany(self.ship, self.ufo_group):
            self.screen.blit(self.alien.explosion_image, self.ship.rect.center)
            self.v.x = self.settings.alien_speed
            print("Ship hit!")
            self.ship.ship_hit()
            return
        
        if self.check_bottom():
            self.v.x = self.settings.alien_speed
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed
        if self.check_ufo_edges():
            self.settings.ufo_speed *= -1 
            for ufo in self.ufo_group:
                ufo.vec.x = self.settings.ufo_speed
            
        for alien in self.aliens:
            alien.update()
        for ufo_group in self.ufo_group:
            ufo_group.update()

    def draw(self): pass
        # for alien in self.aliens:
        #     alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
