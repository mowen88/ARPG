import pygame
from os import walk
from settings import *
from state import State

from entity import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.player = Player(self.game, RES/2)

		self.all_sprites = pygame.sprite.Group()
		self.all_sprites.add(self.player)

	def update(self, dt):
		#update the sprite groups
		self.all_sprites.update(dt)
		if ACTIONS['return']:
			self.exit_state()
		self.game.reset_keys()

	def render(self, screen):
		screen.fill(PINK)

		self.game.render_text('Zone', LIGHT_GREEN, self.game.big_font, RES * 0.5)
		self.game.render_text('Zone', LIGHT_GREEN, self.game.medium_font, (HALF_WIDTH, HEIGHT * 0.6))
		self.game.render_text('Zone', LIGHT_GREEN, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.7))

		# draw the sprites
		for sprite in self.all_sprites:
			screen.blit(sprite.image, sprite.rect)