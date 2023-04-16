import pygame
from settings import *

class Idle:
	def __init__(self, player, direction):

		
		self.player = player
		self.direction = direction

		self.player.frame_index = 0

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


	def update(self, dt, player):
		player.physics(dt)
		player.animate(self.direction + '_idle', 0.2 * dt, 'end')

class Attack:
	def __init__(self, player, direction):

		player.game.reset_keys()
		
		self.direction = direction
		self.lunge_speed = 5
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]

	def state_logic(self, player):
		if player.vel.magnitude() < 0.05:
			return Idle(player, self.direction)

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
			
	def update(self, dt, player):
		player.acc = pygame.math.Vector2()

		self.get_angle(player)

		self.lunge_speed -= 0.05
		self.lunge_speed *= 0.99

		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.vel = player.vel.normalize() * self.lunge_speed
		
		
		player.physics(dt)
		player.animate(self.direction + '_attack', 0.2 * dt, 'end')

class Dash:
	def __init__(self, player, direction):

		player.game.reset_keys()

		self.direction = direction
		self.lunge_speed = 15
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]

	def state_logic(self, player):
		if player.vel.magnitude() < 0.05:
			return Idle(player, self.direction)

	def get_angle(self, player):
		if 45 < player.angle < 135:
			self.direction = 'right'
		elif 135 < player.angle < 225:
			self.direction = 'down'
		elif 225 < player.angle < 315:
			self.direction = 'left'
		else:
			self.direction = 'up'
			
	def update(self, dt, player):
		player.acc = pygame.math.Vector2()

		self.get_angle(player)

		self.lunge_speed -= 0.05
		self.lunge_speed *= 0.99

		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.vel = player.vel.normalize() * self.lunge_speed

		
		player.physics(dt)
		player.animate(self.direction + '_attack', 0.2 * dt, 'end')

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

		if player.vel == pygame.math.Vector2():
			return Idle(player, self.direction)


	def update(self, dt, player):

		#player movement
		player.acc = pygame.math.Vector2()

		if player.moving_down and player.vel.y >= 0:
			player.acc.y += 1
		elif player.moving_up and player.vel.y <= 0:
			player.acc.y -= 1

		if player.moving_right and player.vel.x >= 0:
			player.acc.x += 1
		elif player.moving_left and player.vel.x <= 0:
			player.acc.x -= 1

		player.physics(dt)

		player.animate(self.direction, 0.2 * dt, 'loop')


		

		