import pygame, math
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()

		self.bg = pygame.image.load('../assets/bg.png').convert_alpha()
		self.bg = pygame.transform.scale_by(self.bg, SCALE)

	def offset_draw(self, target):
		self.game.screen.fill(GREEN)
		#self.game.screen.blit(self.bg, (0 - self.offset.x, 0 - self.offset.y))

		self.offset += (target.hitbox.center - self.offset - RES * 0.5)/10

		
		for group in self.zone.layers:
			for sprite in sorted(group, key = lambda sprite: sprite.rect.centery):
				offset = sprite.rect.topleft - self.offset
				self.game.screen.blit(sprite.image, offset)