import pygame, math, random
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
		self.screenshake_timer = 0

	def screenshake(self):
		if self.game.screenshaking:
			self.screenshake_timer += 1
			if self.screenshake_timer < 120:
				random_number = random.randint(-1, 1)
				self.offset += [random_number, random_number]
			else:
				self.game.screenshaking = False

	def offset_draw(self, target):
		
		self.game.screen.fill(GREEN)

		self.offset.x += (target.rect.centerx - self.offset.x - HALF_WIDTH)
		self.offset.y += (target.rect.centery - self.offset.y - HALF_HEIGHT)
	
		#self.offset += [1, 1] + self.zone.get_distance_direction_and_angle(target.hitbox.center, pygame.mouse.get_pos())[1] * 10

		self.screenshake()

		for group in Z_LAYERS:
			for sprite in sorted(self.zone.rendered_sprites, key = lambda sprite: sprite.rect.centery):
				if sprite in group:
					offset = sprite.rect.topleft - self.offset
					self.game.screen.blit(sprite.image, offset)