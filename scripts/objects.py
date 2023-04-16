import pygame
from settings import *

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.4, -self.rect.height * 0.1)

class Tree(Object):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.5)

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
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.4, -self.rect.height * 0.4)



