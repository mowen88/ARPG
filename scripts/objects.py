import pygame
from settings import *

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.75)
