import pygame
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from state import State
from camera import Camera

from entity import Player

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game


		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
	
		self.layers = self.get_layer_groups()
			
		self.get_map()


	def get_layer_groups(self):
		layers = []
		for num in range(4):
			layers.append(pygame.sprite.Group())
		return layers

	def get_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		for obj in tmx_data.get_layer_by_name('player'):
			if obj.name == 'start':
				self.player = Player(self.game, [self.updated_sprites, self.layers[0]], (obj.x * SCALE, obj.y * SCALE))
				self.target = self.player
		

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Object((x * TILESIZE, y * TILESIZE), surf, [self.updated_sprites, self.layers[0]])


	def switch_layer(self):
		pass


	def update(self, dt):
		#update the sprite groups
		self.updated_sprites.update(dt)
		if ACTIONS['return']:
			self.exit_state()
		self.game.reset_keys()

	def render(self, screen):
		screen.fill(PINK)

		# draw the sprites
		self.rendered_sprites.offset_draw(self.target)

		#self.game.render_text(f'{round(self.player.acc.x, 3)}, {round(self.player.acc.y, 3)}', PURPLE, self.game.small_font, RES/2)
		self.game.render_text(self.player.moving_right, PURPLE, self.game.small_font, (WIDTH * 0.8, HALF_HEIGHT))
		self.game.render_text(self.player.moving_left, PURPLE, self.game.small_font, (WIDTH * 0.2, HALF_HEIGHT))
		self.game.render_text(self.player.moving_down, PURPLE, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.8))
		self.game.render_text(self.player.moving_up, PURPLE, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.2))


class Object(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)
