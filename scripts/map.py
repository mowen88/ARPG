import pygame, os
from csv import reader
from pytmx.util_pygame import load_pygame

from settings import *
from objects import Object, Wall, Stairs
from player import Player

class Map:
	def __init__(self, game, zone):

		self.game = game
		self.zone = zone

	def import_csv_tileset(self):
		zone_grid = []
		with open(f'../zones/{self.game.current_zone}.csv') as grid:
			zone = reader(grid, delimiter = ',')
			for row in zone:
				zone_grid.append(list(row))

		return zone_grid

	def place_tileset(self):

		# csv to get id of tiles in tileset
		csv_data = self.import_csv_tileset()

		for row_index, row in enumerate(csv_data):
			for col_index, col in enumerate(row):

				if col != '-1':
					# get surface using the index
					surf = pygame.image.load(f'../assets/tiles/{col}.png').convert_alpha()
					x = col_index * TILESIZE
					y = row_index * TILESIZE

					if col in '56789': # index values from the tiles folder
						Wall(self.game, self.zone, [self.zone.wall_sprites, self.zone.rendered_sprites, Z_LAYERS[3]], (x, y), surf, col)
					if col in '012': # index values from the tiles folder
						Stairs(self.game, self.zone, [self.zone.stair_sprites, self.zone.rendered_sprites, Z_LAYERS[2]], (x, y), surf, col)







