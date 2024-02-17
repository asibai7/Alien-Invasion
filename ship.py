import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        #initializes ship and starting position
        super().__init__()
        self.screen = ai_game.screen 
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()
        #starts each new ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom 
        self.x = float(self.rect.x)
        #movement flag, start with a ship thats not moving
        self.moving_right = False 
        self.moving_left = False

    def update(self): 
        #update ship position based on movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        #draws ship
        self.screen.blit(self.image, self.rect) 

    def center_ship(self):
        #center ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)