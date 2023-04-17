import pygame

class Sword(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.image = pygame.Surface((40,40))
		
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		self.rect.center = self.zone.player.hitbox.center


class Gun(pygame.sprite.Sprite):
	def __init__(self):
		self.image = pygame.Surface((20,20))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()