import pygame
from settings import *

class IdleState:
	def __init__(self, direction):
		self.direction = direction

	def state_logic(self, player):
		
		if ACTIONS['left_click']:
			return AttackState(player, self.direction)

		if ACTIONS['down']:
			player.moving_down = True
			self.direction = 'down'
			return MoveState(player.vel, self.direction)

		elif ACTIONS['up']:
			player.moving_up = True
			self.direction = 'up'
			return MoveState(player.vel, self.direction)

		if ACTIONS['right']:
			player.moving_right = True
			self.direction = 'right'
			return MoveState(player.vel, self.direction)

		elif ACTIONS['left']:
			player.moving_left = True
			self.direction = 'left'
			return MoveState(player.vel, self.direction)

		
	def update(self, player):
		player.decelerate(player.friction)
		player.move()
		player.animate(self.direction + '_idle')

class AttackState:
	def __init__(self, player, direction):
		self.direction = direction
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, pygame.mouse.get_pos())[1] * 5

	def state_logic(self, player):
		if player.vel.magnitude() < 0.5:
			return MoveState(player.vel, self.direction)
			
	def update(self, player):
		player.decelerate(0.1)
		player.move()
		player.animate('attacking')

class MoveState:
	def __init__(self, vel, direction):
		self.direction = direction

	def state_logic(self, player):

		if ACTIONS['left_click']:
			return AttackState(player, self.direction)

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
			return IdleState(self.direction)

	def update(self, player):
		player.accelerate()
		player.move()
		player.animate(self.direction)


		

		