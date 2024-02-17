import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        #initialize alien and starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #load alien image and sets rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        #start new alien in top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #store aliens exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        #return true if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        return (self.rect.right > screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        #move the alien right or left
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        #checks the edges of the alien