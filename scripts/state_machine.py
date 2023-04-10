import pygame
from settings import *

class IdleState:

	def state_logic(self, player):
		if ACTIONS['right']:
			return MoveState(player.vel)
		# elif action['left']:
		# 	return AccState()

		# else:
		# 	player.vel.x = 0

	def update(self, player):
		pass
		# animate?

class MoveState:
	def __init__(self, vel):
		self.vel = vel



	def state_logic(self, player):
		player.vel.x = 2
		if ACTIONS['right'] == False:
			return IdleState()

	def update(self, player):
		pass
		