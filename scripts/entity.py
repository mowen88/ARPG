import math
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos):
		super().__init__()


		self.image = pygame.Surface((32, 32))
		self.image.fill(LIGHT_GREEN)
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.vel = pygame.math.Vector2()
		self.acc = pygame.math.Vector2()
		self.friction = 0.99

	def update(self, dt):
		pass

	def render(self, screen):
		pass

class Player(Entity):
	def __init__(self, game, groups, pos):
		super().__init__(game, groups, pos)
		self.speed = 5

	def move(self, dt):
		keys = pygame.key.get_pressed()

		self.acc = pygame.math.Vector2()

		if keys[pygame.K_RIGHT]:
			self.acc.x += 0.3
		elif keys[pygame.K_LEFT]:
			self.acc.x -= 0.3
		else:
			self.acc.x = 0

		if keys[pygame.K_DOWN]:
			self.acc.y += 0.3
		elif keys[pygame.K_UP]:
			self.acc.y -= 0.3
		else:
			self.acc.y = 0

		self.vel += self.acc
		self.vel *= self.friction * dt
		self.rect.x += self.vel.x
		self.rect.y += self.vel.y

	def update(self, dt):
		self.move(dt)
		

	def render(self, screen):
		pass

