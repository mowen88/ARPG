import pygame, math
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, zone):
		super().__init__()

		self.game = game
		self.zone = zone
		self.offset = pygame.math.Vector2()
		self.acc = pygame.math.Vector2()

		self.bg = pygame.image.load('../assets/bg.png').convert_alpha()
		self.bg = pygame.transform.scale_by(self.bg, SCALE)
		self.pos = pygame.math.Vector2()

	def offset_draw(self, target):
		self.game.screen.fill(GREEN)

		self.offset.x += (target.rect.centerx - self.offset.x - HALF_WIDTH)/50
		self.offset.y += (target.rect.centery - self.offset.y - HALF_HEIGHT)/50
	
		#self.offset += [1, 1] + self.zone.get_distance_direction_and_angle(target.hitbox.center, pygame.mouse.get_pos())[1] * 10


		for group in Z_LAYERS:
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite in group:
					offset = sprite.rect.topleft - self.offset
					self.game.screen.blit(sprite.image, offset)