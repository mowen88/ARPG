import pygame
from settings import *

class Sword(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.image = pygame.image.load('../assets/weapons/up_attack/0.png').convert_alpha()
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(center = pos)
		self.frame_index = 0
		self.import_imgs()

		self.get_current_direction = pygame.mouse.get_pos()
		self.angle = self.zone.get_distance_direction_and_angle(self.zone.player.hitbox.center, self.get_current_direction)[2]
		

	def get_angle(self, player):
		if 45 < player.angle < 135: self.direction = 'right'
		elif 135 < player.angle < 225: self.direction = 'down'
		elif 225 < player.angle < 315: self.direction = 'left'
		else: self.direction = 'up'

	def import_imgs(self):
		self.animations = {'right_attack':[], 'left_attack':[], 'up_attack':[], 'down_attack':[]}

		for animation in self.animations.keys():
			full_path = '../assets/weapons/' + animation
			self.animations[animation] = self.game.import_folder(full_path)

	def animate(self, state, animation_speed):
		self.frame_index += animation_speed
		if self.frame_index >= len(self.animations[state])-1:
			self.kill()
		self.image = self.animations[state][int(self.frame_index)]
	
	def update(self, dt):
		self.get_angle(self.zone.player)
		self.animate(self.direction + '_attack', 0.2 * dt)
		self.rect = self.image.get_rect(center = self.zone.player.rect.center)


class Gun(pygame.sprite.Sprite):
	def __init__(self):
		self.image = pygame.Surface((20,20))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()