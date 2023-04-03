import math
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos):
		super().__init__()


		self.image = pygame.Surface((32, 32))
		self.image.fill(LIGHT_GREEN)
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()
		self.acc = pygame.math.Vector2()
		self.friction = -0.2

	def update(self, dt):
		pass

	def render(self, screen):
		pass

class Player(Entity):
	def __init__(self, game, groups, pos):
		super().__init__(game, groups, pos)
		

	def move(self, dt):
		
		self.acc = pygame.math.Vector2()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.acc.x += 0.4
		if keys[pygame.K_LEFT]:
			self.acc.x -= 0.4

		if keys[pygame.K_DOWN]:
			self.acc.y += 0.4
		if keys[pygame.K_UP]:
			self.acc.y -= 0.4

		if self.acc.magnitude() != 0:
			self.acc = self.acc.normalize()

		self.acc += self.vel * self.friction
		self.vel += self.acc * dt

		self.pos += self.vel * dt - (self.acc * 0.5) * dt
		self.rect.center = self.pos

		


		# if keys[pygame.K_DOWN]:
		# 	self.acc.y += 1
		# elif keys[pygame.K_UP]:
		# 	self.acc.y -= 1
		# else:
		# 	self.acc.y = 0

		# self.vel += self.acc * dt
		# self.vel *= self.friction
		# self.rect.x += self.vel.x
		# self.rect.y += self.vel.y

	def update(self, dt):
		self.move(dt)
		

	def render(self, screen):
		pass

