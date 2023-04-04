import pygame
from os import walk
from settings import *
from state import State

from entity import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		# sprite groups
		self.all_sprites = pygame.sprite.Group()

		# sprites
		self.player = Player(self.game, self.all_sprites, RES/2)
		
		# add sprite to groups
		self.all_sprites.add(self.player)

	def update(self, dt):
		#update the sprite groups
		self.all_sprites.update(dt)
		if ACTIONS['return']:
			self.exit_state()
		self.game.reset_keys()

	def render(self, screen):
		screen.fill(PINK)

		# draw the sprites
		for sprite in self.all_sprites:
			screen.blit(sprite.image, sprite.rect)

		#self.game.render_text(f'{round(self.player.acc.x, 3)}, {round(self.player.acc.y, 3)}', PURPLE, self.game.small_font, RES/2)
		self.game.render_text(self.player.moving_right, PURPLE, self.game.small_font, RES/2)