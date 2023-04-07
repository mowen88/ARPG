import math
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos):
		super().__init__(groups)

		self.image = pygame.Surface((25, 25))
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(self.image.get_width() * 0.2, self.image.get_height() * 0.2)
		self.pos = pygame.math.Vector2(self.hitbox.center)
		
		self.vel = pygame.math.Vector2()
		self.acc = pygame.math.Vector2()
		self.friction = -0.2

		self.moving_right, self.moving_left = False, False
		self.moving_down, self.moving_up = False, False

	def move_logic(self, dt):
		
		self.acc = pygame.math.Vector2()

		if self.moving_right:
			self.acc.x += 0.4
		if self.moving_left:
			self.acc.x -= 0.4
		if self.moving_down:
			self.acc.y += 0.4
		if self.moving_up:
			self.acc.y -= 0.4

		if self.acc.magnitude() != 0:
			self.acc = self.acc.normalize()

		self.acc += self.vel * self.friction
		self.vel += self.acc * dt

		self.pos += self.vel * dt - (self.acc * 0.5) * dt
		self.hitbox.center = round(self.pos)
		self.rect.center = self.hitbox.center


	def update(self, dt):
		pass

	def render(self, screen):
		pass


class Platform(Entity):
	def __init__(self, game, groups, pos):
		super().__init__(game, groups, pos)

	def update(self, dt):
		pass

	def render(self, display):
		pass

class Player(Entity):
	def __init__(self, game, groups, pos):
		super().__init__(game, groups, pos)

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.moving_right = True
		else:
			self.moving_right = False
			
		if keys[pygame.K_LEFT]:
			self.moving_left = True
		else:
			self.moving_left = False
			
		if keys[pygame.K_DOWN]:
			self.moving_down = True
		else:
			self.moving_down = False

		if keys[pygame.K_UP]:
			self.moving_up = True
		else:
			self.moving_up = False

	def update(self, dt):
		self.input()
		self.move_logic(dt)

	def render(self, screen):
		pass

