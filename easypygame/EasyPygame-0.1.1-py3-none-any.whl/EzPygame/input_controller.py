import pygame

class KeyboardController:
    
    def __init__(self,movement_speed=2):
        self.movement_speed = movement_speed
    
    def handle_keys(self, player, canvas):
      """ Handles Keys """
      key = pygame.key.get_pressed()
      if key[pygame.K_s] and player.rect.y < canvas.screen_size[1]-player.size: # down key
            player.rect.y += self.movement_speed # move down
      if key[pygame.K_w] and player.rect.y > 0: # up ke
            player.rect.y -= self.movement_speed # move up
      if key[pygame.K_d] and player.rect.x < canvas.screen_size[0]-player.size: #move right
            player.rect.x += self.movement_speed 
      if key[pygame.K_a] and player.rect.x > 0: # left key
            player.rect.x -= self.movement_speed # move left