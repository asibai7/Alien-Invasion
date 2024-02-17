import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        #create bullet and set position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        #store bullet position  as float
        self.y = float(self.rect.y)

    def update(self):
        # update exact position of bullet
        self.y -= self.settings.bullet_speed
        #update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        #draw bullet to screen
        pygame.draw.rect(self.screen, self.color, self.rect)
