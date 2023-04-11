import pygame
from settings import *

class Idle:
	def __init__(self, direction):
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['left_click']:
			return Attack(player, self.direction)

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

		if ACTIONS['down']:
			player.moving_down = True
			self.direction = 'down'
			return Move(player.vel, self.direction)

		elif ACTIONS['up']:
			player.moving_up = True
			self.direction = 'up'
			return Move(player.vel, self.direction)

		if ACTIONS['right']:
			player.moving_right = True
			self.direction = 'right'
			return Move(player.vel, self.direction)

		elif ACTIONS['left']:
			player.moving_left = True
			self.direction = 'left'
			return Move(player.vel, self.direction)

		
	def update(self, player):
		player.decelerate(player.friction)
		player.move(player.max_speed)
		player.animate(self.direction + '_idle', 0.2, 'end')

class Attack:
	def __init__(self, player, direction):
		self.direction = direction
		self.lunge_speed = 3
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, pygame.mouse.get_pos())[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, pygame.mouse.get_pos())[2]

	def state_logic(self, player):
		if player.vel.magnitude() < 0.5:
			return Move(player.vel, self.direction)

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

	def get_angle(self, player):
		if 45 < player.angle < 135:
			self.direction = 'right'
		elif 135 < player.angle < 225:
			self.direction = 'down'
		elif 225 < player.angle < 315:
			self.direction = 'left'
		else:
			self.direction = 'up'
			
	def update(self, player):
		player.decelerate(0.2)
		player.move(self.lunge_speed)
		self.get_angle(player)
		player.animate(self.direction + '_attack', 0.2, 'loop')

class Dash:
	def __init__(self, player, direction):
		self.direction = direction
		self.lunge_speed = 8
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, pygame.mouse.get_pos())[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, pygame.mouse.get_pos())[2]

	def state_logic(self, player):
		if player.vel.magnitude() < 0.5:
			return Move(player.vel, self.direction)

	def get_angle(self, player):
		if 45 < player.angle < 135:
			self.direction = 'right'
		elif 135 < player.angle < 225:
			self.direction = 'down'
		elif 225 < player.angle < 315:
			self.direction = 'left'
		else:
			self.direction = 'up'
			
	def update(self, player):
		player.decelerate(0.2)
		player.move(self.lunge_speed)
		self.get_angle(player)
		player.animate(self.direction + '_attack', 0.2, 'loop')

class Move:
	def __init__(self, vel, direction):
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['left_click']:
			return Attack(player, self.direction)

		if ACTIONS['right_click']:
			return Dash(player, self.direction)

		# face the correct direction (if y held first, always face y regardless of x, if x held first, always face x regardless of y)
		if ACTIONS['down'] and not (ACTIONS['right'] or ACTIONS['left']):
			self.direction = 'down'
		elif ACTIONS['up'] and not (ACTIONS['right'] or ACTIONS['left']):
			self.direction = 'up'
		if ACTIONS['right'] and not (ACTIONS['down'] or ACTIONS['up']):
			self.direction = 'right'
		elif ACTIONS['left'] and not (ACTIONS['down'] or ACTIONS['up']):
			self.direction = 'left'


		# y direction
		if ACTIONS['down']:
			player.moving_down = True
		else:
			player.moving_down = False		
		
		if ACTIONS['up']:
			player.moving_up = True	
		else:
			player.moving_up = False

		# x direction
		if ACTIONS['right']:
			player.moving_right = True
		else:
			player.moving_right = False
			
		if ACTIONS['left']:
			player.moving_left = True
		else:
			player.moving_left = False

		if not (ACTIONS['down'] or ACTIONS['up'] or ACTIONS['right'] or ACTIONS['left']):
			return Idle(self.direction)

	def update(self, player):
		player.accelerate()
		player.move(player.max_speed)
		player.animate(self.direction, 0.2, 'loop')


		

		