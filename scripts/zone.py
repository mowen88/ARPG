import pygame
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from map import Map
from state import State
from camera import Camera
from player import Player
from objects import Object, Tree
from weapons import Sword, Gun

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.melee_sprite = pygame.sprite.GroupSingle()

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.collidable_sprites = pygame.sprite.Group()
		self.wall_sprites = pygame.sprite.Group()
		self.stair_sprites = pygame.sprite.Group()
		self.void_sprites = pygame.sprite.Group()

		

		Map(self.game, self).place_tileset()
		self.get_map()

	def get_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		# add a background
		Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())

		# for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
		# 	Object(self.game, self, [Z_LAYERS[2]], (x * TILESIZE, y * TILESIZE), surf)

		# add the player
		for obj in tmx_data.get_layer_by_name('player'):
			if obj.name == 'start':
				self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites, Z_LAYERS[3]], (obj.x * SCALE, obj.y * SCALE), pygame.Surface((16, 16)))
				self.target = self.player

		# add the flower pots!
		for obj in tmx_data.get_layer_by_name('objects'):
			if obj.name == 'tree':
				Tree(self.game, self, [self.collidable_sprites, self.rendered_sprites, Z_LAYERS[3]], (obj.x * SCALE, obj.y * SCALE), obj.image)

	def create_melee(self):
		self.melee_sprite = Sword(self.game, self, [self.updated_sprites, self.rendered_sprites, Z_LAYERS[3]], self.player.hitbox.center)
		
	def get_distance_direction_and_angle(self, point_1, point_2):
		pos_1 = pygame.math.Vector2(point_1 - self.rendered_sprites.offset)
		pos_2 = pygame.math.Vector2(point_2)
		distance = (pos_2 - pos_1).magnitude()
		if (pos_2 - pos_1).magnitude() != 0:
		    direction = (pos_2 - pos_1).normalize()
		else:
			direction = pygame.math.Vector2(1,1)
		
		dx = point_1[0] - (pos_2.x + self.rendered_sprites.offset.x)
		dy = point_1[1] - (pos_2.y + self.rendered_sprites.offset.y)

		radians = atan2(-dx, dy)
		radians %= 2*pi
		angle = int(degrees(radians))

		return(distance, direction, angle)

	def return_to_menu(self):
		if ACTIONS['space']:
			self.create_melee()
		if ACTIONS['return']:
			self.exit_state()
			self.game.reset_keys()

	def update(self, dt):
		self.return_to_menu()
		#update the sprite groups
		self.updated_sprites.update(dt)
	
	def render(self, screen):
		screen.fill(PINK)

		# draw the sprites
		self.rendered_sprites.offset_draw(self.target)

		#self.game.render_text(f'{round(self.player.acc.x, 3)}, {round(self.player.acc.y, 3)}', PURPLE, self.game.small_font, RES/2)
		self.game.render_text(self.player.state, PURPLE, self.game.small_font, RES/2)
		# self.game.render_text(self.player.moving_right, PURPLE, self.game.small_font, (WIDTH * 0.8, HALF_HEIGHT))
		# self.game.render_text(self.player.moving_left, PURPLE, self.game.small_font, (WIDTH * 0.2, HALF_HEIGHT))
		self.game.render_text(self.player.moving_down, PURPLE, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.8))
		self.game.render_text(self.player.moving_up, PURPLE, self.game.small_font, (HALF_WIDTH, HEIGHT * 0.2))



