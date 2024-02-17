import sys #module that has tools to exit a game when the player quits
from time import sleep
import pygame #module which contains functionality to make a game
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
        def __init__(self):
                #initializes the background settings that pygame needs to work
                pygame.init() 
                #defines clock
                self.clock = pygame.time.Clock() 
                #makes an instance of Ship
                self.settings = Settings() 
                self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
                pygame.display.set_caption("Alien Invasion")
                #create an instance to store game stats and create a scoreboard
                self.stats = GameStats(self)
                self.sb = Scoreboard(self)
                #gives Ship access to the game's resources such as the screen object since the argument Ship takes is an instance of AlienInvasion
                self.ship = Ship(self) 
                #group to hold bullets
                self.bullets = pygame.sprite.Group() 
                self.aliens = pygame.sprite.Group()
                self._create_fleet()
                #start alien invasion in an active state
                self.game_active = False
                #make the play button
                self.play_button = Button(self, "Play")

        def run_game(self):
                while True:
                    self._check_events()
                    if self.game_active:
                        self.ship.update()
                        self._update_bullets()
                        self._update_aliens()
                    self._update_screen()
                    #creates an instance of class Clock, which makes the clock tick at the end of the while loop, takes frame rate which is 60 so pygame will make the loop run 60 times per second
                    self.clock.tick(60) 

        def _check_events(self):
                #accesses the events that pygame detects
                for event in pygame.event.get():
                    #when player clicks the game windows close button, the quit event is detected 
                    if event.type == pygame.QUIT: 
                        #once the quit event is detected, sys.exit() is called to exit the game
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self._check_keydown_events(event)
                    #when player releases right arrow key
                    elif event.type == pygame.KEYUP: 
                        self._check_keyup_events(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        self._check_play_button(mouse_pos)

        def _check_keydown_events(self, event):
            #Move ship to the right
            if event.key == pygame.K_RIGHT: 
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()

        def _check_keyup_events(self, event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

        def _fire_bullet(self):
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)

        def _update_screen(self): #updates images on screen and flips to new screen
            #redraws screen uring each pass through loop
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():   
                bullet.draw_bullet()
            #draws the ship on the screen so it appears on top of background
            self.ship.blitme() 
            self.aliens.draw(self.screen)
            #draw the score information
            self.sb.show_score()
            #draw the play button if the game is inactive
            if not self.game_active:
                self.play_button.draw_button()
             #continually updates the display to show new window look and hide old window look making the game movement smooth
            pygame.display.flip()

        def _update_bullets(self):
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()

        def _check_bullet_alien_collisions(self):
            #check for any bullets that have hit aliens, if so then get rid of the bullet and the alien
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
            if not self.aliens:
                #destroy existing bullets and create new fleet
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()
                #increase level
                self.stats.level += 1
                self.sb.prep_level()

        def _create_fleet(self):
            #create fleet of aliens              
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            #horizontal position of the next alien we intend to place on the screen
            current_x, current_y = alien_width, alien_height
            #loop to check that their is enough space for an alien which is determined by checking that on the right side their is at least two alien width's worth 
            while current_y < (self.settings.screen_height - 3 * alien_height):
                while current_x < (self.settings.screen_width - 2* alien_width):
                    self._create_alien(current_x, current_y)
                    current_x += 2 * alien_width
                #Finished a row, reset x value, and increment y value
                current_x = alien_width
                current_y += 2 * alien_height

        def _create_alien(self, x_position, y_position):
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

        def _update_aliens(self):
            #check if fleet is at an edge, then update the positions of all aliens in the fleet
            self._check_fleet_edges()
            self.aliens.update()
            #look for alien-ship collisions
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()
            #look for aliens hitting the bottom of the screen
            self._check_aliens_bottom()

        def _check_fleet_edges(self):
            #respond properly if an alien reaches an edge
            for alien in self.aliens.sprites():
                if alien.check_edges():
                    self._change_fleet_direction()
                    break

        def _change_fleet_direction(self):
            #drop the entire fleet and change the fleets direction
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

        def _ship_hit(self):
            #respond to the ship being hit by an alien
            if self.stats.ship_left > 0:
                #decrement ships left
                self.stats.ship_left -= 1
                self.sb.prep_ships()
                #get rid of any remaining bullets and aliens
                self.bullets.empty()
                self.aliens.empty()
                #create a new fleet and center the ship
                self._create_fleeet()
                self.ship.center_ship()
                #Pause
                sleep(0.5)
            else:
                self.game_active = False
                pygame.mouse.set_visible(True)

        def _check_aliens_bottom(self):
            #check if any aliens have reached the bottom of the screen
            for alien in self.aliens.sprites():
                if alien.rect.bottom >= self.settings.screen_height:
                    #treat this the same as if ship got hit
                    self._ship_hit()
                    break

        def _check_play_button(self, mouse_pos):
            #start a new game when the player clicks play
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.game_active:
                #reset the game stats
                self.settings.initialize_dynamic_settings()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                self.game_active = True
                #get rid of any remaining bullets and aliens
                self.bullets.empty()
                self.aliens.empty()
                #create a new fleet and center the ship
                self._create_fleet()
                self.ship.center_ship()
                #hide the mouse cursor
                pygame.mouse.set_visible(False)

if __name__ == '__main__': #runs only if the file is called directly
      #creates an instance of AlienInvasion class
      ai = AlienInvasion() 
      #calls run_game() method to start reading events
      ai.run_game() 