import pygame
from settings import *

class Idle:
	def __init__(self, player, direction):

		self.player = player
		self.direction = direction
		
		self.player.edge = ''
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

		player.zone.create_melee()
		
		ACTIONS['left_click'] = False
		
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
		if 45 < player.angle < 135: self.direction = 'right'
		elif 135 < player.angle < 225: self.direction = 'down'
		elif 225 < player.angle < 315: self.direction = 'left'
		else: self.direction = 'up'
			
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

		ACTIONS['right_click'] = False

		self.direction = direction
		self.lunge_speed = 15
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]

	def state_logic(self, player):
		# if player.edge_collided() and player.vel.magnitude() < player.max_speed:
		# 	player.vel = pygame.math.Vector2()
		# 	return Idle(player, self.direction) 

		if player.vel.magnitude() < 0.05:
			return Idle(player, self.direction)

	def get_angle(self, player):
		if 45 < player.angle < 135: self.direction = 'right'
		elif 135 < player.angle < 225: self.direction = 'down'
		elif 225 < player.angle < 315: self.direction = 'left'
		else: self.direction = 'up'
			
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

	def get_facing(self, player):
		# face the correct direction (if y held first, always face y regardless of x, if x held first, always face x regardless of y)
		if abs(player.vel.y) < player.max_speed/4:
			if player.vel.x > 0: self.direction = 'right'
			elif player.vel.x < 0: self.direction = 'left'
		if abs(player.vel.x) < player.max_speed/4:
			if player.vel.y > 0: self.direction = 'down'
			elif player.vel.y < 0: self.direction = 'up'

	def state_logic(self, player):

		self.get_facing(player)

		if ACTIONS['left_click']: return Attack(player, self.direction)

		if ACTIONS['right_click']: return Dash(player, self.direction)

	
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

		if player.edge == 'left_up' and not ((ACTIONS['left'] and ACTIONS['down']) or (ACTIONS['right'] and ACTIONS['up'])): return OnEdge(self.direction, player.edge)
		elif player.edge == 'right_up' and not ((ACTIONS['right'] and ACTIONS['down']) or (ACTIONS['left'] and ACTIONS['up'])): return OnEdge(self.direction, player.edge)
		if player.edge == 'left_down' and not ((ACTIONS['left'] and ACTIONS['up']) or (ACTIONS['right'] and ACTIONS['down'])): return OnEdge(self.direction, player.edge)
		elif player.edge == 'right_down' and not ((ACTIONS['right'] and ACTIONS['up']) or (ACTIONS['left'] and ACTIONS['down'])): return OnEdge(self.direction, player.edge)
		elif player.edge in ['left','right','up','down']: return OnEdge(self.direction, player.edge)

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

class OnEdge:
	def __init__(self, direction, edge):
		self.direction = direction
		self.edge = edge

	def state_logic(self, player):

		if ACTIONS['right_click']: return Dash(player, self.direction)

		if self.edge == 'left' and not ACTIONS['left']: return Idle(player, self.direction)
		elif self.edge == 'right' and not ACTIONS['right']: return Idle(player, self.direction)
		if self.edge == 'up' and not ACTIONS['up']: return Idle(player, self.direction)
		elif self.edge == 'down' and not ACTIONS['down']: return Idle(player, self.direction)

		if self.edge == 'left_up' and ((ACTIONS['up'] and ACTIONS['right']) or (ACTIONS['down'] and ACTIONS['left']) or not (ACTIONS['up'] or ACTIONS['left'])): return Idle(player, self.direction)
		elif self.edge == 'right_up' and ((ACTIONS['up'] and ACTIONS['left']) or (ACTIONS['down'] and ACTIONS['right']) or not (ACTIONS['up'] or ACTIONS['right'])): return Idle(player, self.direction)
		if self.edge == 'left_down' and ((ACTIONS['down'] and ACTIONS['right']) or (ACTIONS['up'] and ACTIONS['left']) or not (ACTIONS['down'] or ACTIONS['left'])): return Idle(player, self.direction)
		elif self.edge == 'right_down' and ((ACTIONS['down'] and ACTIONS['left']) or (ACTIONS['up'] and ACTIONS['right']) or not (ACTIONS['down'] or ACTIONS['right'])): return Idle(player, self.direction)

	def update(self, dt, player):
		player.vel = pygame.math.Vector2()
		player.animate(self.direction + '_idle', 0.2 * dt, 'loop')





		

		