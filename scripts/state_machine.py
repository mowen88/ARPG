import pygame
from settings import *

class IdleState:
	def __init__(self, direction):
		self.direction = direction

	def state_logic(self, player):
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
		player.decelerate()
		player.move()
		player.animate(self.direction + '_idle')
		


class MoveState:
	def __init__(self, vel, direction):
		self.direction = direction

	def state_logic(self, player):
		
		# y direction
		if ACTIONS['down']:
			self.direction = 'down'
			player.moving_down = True		
		else:
			player.moving_down = False
			
		if ACTIONS['up']:
			self.direction = 'up'
			player.moving_up = True	
		else:
			player.moving_up = False

		# x direction
		if ACTIONS['right']:
			self.direction = 'right'
			player.moving_right = True
			
		else:
			player.moving_right = False
			
		if ACTIONS['left']:
			self.direction = 'left'
			player.moving_left = True
		else:
			player.moving_left = False


		if not (ACTIONS['down'] or ACTIONS['up'] or ACTIONS['right'] or ACTIONS['left']):
			return IdleState(self.direction)
			

	def update(self, player):
		player.accelerate()
		player.move()
		player.animate(self.direction)


		

		