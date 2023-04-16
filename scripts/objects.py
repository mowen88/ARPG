import pygame
from settings import *

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.image.get_width() * 0.4, -self.image.get_height() * 0.75)

class Wall(Object):
	def __init__(self, game, zone, groups, pos, surf, col):
		super().__init__(game, zone, groups, pos, surf)

		self.image = surf
		self.col = col
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0, 0)

class Stairs(Object):
	def __init__(self, game, zone, groups, pos, surf, col):
		super().__init__(game, zone, groups, pos, surf)

		self.image = surf
		self.col = col
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.image.get_width() * 0.5, -self.image.get_height() * 0.5)



