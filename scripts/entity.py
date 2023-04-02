from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, pos):
		super().__init__()

		self.image = pygame.Surface((32, 32))
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		pass

	def render(self, screen):
		pass

class Player(Entity):
	def __init__(self, game, pos):
		super().__init__(game, pos)

	def update(self, dt):
		pass

	def render(self, screen):
		pass

