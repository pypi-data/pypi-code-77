import pygame
import EzPygame
from EzPygame.input_controller import KeyboardController

class Character(object):
    
    def __init__(self, spawn_coordinates=(0,0), size=20, sprite=None):
        self.size = size
        if sprite is None:
            self.image = pygame.Surface((self.size,self.size))
            self.image.fill((128,70,128))
        else:
            self.image = pygame.image.load(sprite)
            self.image= pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.spawn_coordinates = spawn_coordinates
        self.rect.x, self.rect.y = spawn_coordinates[0], spawn_coordinates[1]
       
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def check_collision(self, other_sprites):
        for enemy_sprite in other_sprites:
            if self.rect.colliderect(enemy_sprite):
                print("crash!")


class Player(Character):

    def __init__(self, spawn_coordinates=(0,0), size=20, sprite=None):
        super().__init__(spawn_coordinates, size, sprite)
        self.controller = KeyboardController(movement_speed=10)


    def handle_keys(self,canvas):
        return self.controller.handle_keys(self, canvas)
