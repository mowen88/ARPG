import pygame
from settings import *

class Idle:
	def __init__(self, player, direction):

		self.direction = direction
		
		if player.zone.melee_sprite: player.zone.melee_sprite.kill()
		player.edge = ''
		player.frame_index = 0

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
		player.acc = pygame.math.Vector2()
		player.vel = pygame.math.Vector2()
		player.animate(self.direction + '_idle', 0.2 * dt, 'end')

class Attack:
	def __init__(self, player, direction):

		player.frame_index = 0
		player.zone.create_melee()
		
		ACTIONS['left_click'] = False
		
		self.timer = 0
		self.direction = direction
		self.lunge_speed = 2
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.get_angle(player)

	def state_logic(self, player):
		if self.timer > 10:
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

		if player.vel.magnitude() > 0.01:
			self.lunge_speed -= 0.1 * dt
			self.lunge_speed *= 0.99

			player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
			player.vel = player.vel.normalize() * self.lunge_speed
		else:
			self.timer += dt
		
		player.physics(dt)
		player.animate(self.direction + '_attack', 0.3 * dt, 'end')

class Dash:
	def __init__(self, player, direction):

		ACTIONS['right_click'] = False

		self.direction = direction
		self.lunge_speed = player.dash_lunge_speed
		self.get_current_direction = pygame.mouse.get_pos()
		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.angle = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[2]
		self.get_angle(player)

	def state_logic(self, player):
		# if player.edge_collided() and player.vel.magnitude() < player.max_speed:
		# 	player.vel = pygame.math.Vector2()
		# 	return Idle(player, self.direction) 
		if player.vel.magnitude() < 0.1:
			if not player.grounded: return Jump(player, self.direction)
			else: return Idle(player, self.direction)


	def get_angle(self, player):
		if 45 < player.angle < 135: self.direction = 'right'
		elif 135 < player.angle < 225: self.direction = 'down'
		elif 225 < player.angle < 315: self.direction = 'left'
		else: self.direction = 'up'

			
	def update(self, dt, player):
		player.acc = pygame.math.Vector2()

		self.lunge_speed -= 0.4 * dt
		#self.lunge_speed *= 0.99

		player.vel = player.zone.get_distance_direction_and_angle(player.hitbox.center, self.get_current_direction)[1] * self.lunge_speed
		player.vel = player.vel.normalize() * self.lunge_speed

		player.physics(dt)
		player.animate(self.direction + '_dash', 0.2 * dt, 'end')

class Move:
	def __init__(self, vel, direction):
		self.direction = direction

	def state_logic(self, player):

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

		if player.edge == 'left_up' and not ((ACTIONS['left'] and ACTIONS['down']) or (ACTIONS['right'] and ACTIONS['up'])): return OnEdge(player, self.direction, player.edge)
		elif player.edge == 'right_up' and not ((ACTIONS['right'] and ACTIONS['down']) or (ACTIONS['left'] and ACTIONS['up'])): return OnEdge(player, self.direction, player.edge)
		if player.edge == 'left_down' and not ((ACTIONS['left'] and ACTIONS['up']) or (ACTIONS['right'] and ACTIONS['down'])): return OnEdge(player, self.direction, player.edge)
		elif player.edge == 'right_down' and not ((ACTIONS['right'] and ACTIONS['up']) or (ACTIONS['left'] and ACTIONS['down'])): return OnEdge(player, self.direction, player.edge)
		elif player.edge in ['left','right','up','down']: return OnEdge(player, self.direction, player.edge)

		if player.vel.magnitude() < 0.1:
			return Idle(player, self.direction)

	def update(self, dt, player):

		#player movement
		player.acc = pygame.math.Vector2()

		if player.moving_down and player.vel.y >= 0:
			player.acc.y += 1
			self.direction = 'down'
		elif player.moving_up and player.vel.y <= 0:
			player.acc.y -= 1
			self.direction = 'up'

		if player.moving_right and player.vel.x >= 0:
			player.acc.x += 1
			self.direction = 'right'
		elif player.moving_left and player.vel.x <= 0:
			player.acc.x -= 1
			self.direction = 'left'

		player.physics(dt)
		player.animate(self.direction, 0.2 * dt, 'loop')

class OnEdge:
	def __init__(self, player, direction, edge):
		self.direction = direction
		self.edge = edge
		self.timer = 50 # time spent pushing against edge before falling (60 = 1 sec)
		player.frame_index = 0

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

		if self.timer <= 0: return Jump(player, self.direction)

	def update(self, dt, player):
		self.timer -= dt
		
		player.vel = pygame.math.Vector2()
		player.animate(self.direction + '_edge', 0.3 * dt, 'end')

class Jump:
	def __init__(self, player, direction):

		self.direction = direction
		player.frame_index = 0
		player.grounded = False
		self.get_initial_speed(player)
		print(self.get_z_group(player))

		player.respawner.rect.center = player.rect.center
		player.zone.target = player.respawner

	def get_initial_speed(self, player):
		if self.direction == 'down': player.vel = pygame.math.Vector2(0, 0)
		elif self.direction == 'up': player.vel = pygame.math.Vector2(0, -1)
		elif self.direction == 'left': player.vel = pygame.math.Vector2(-1.25, -0.5)
		elif self.direction == 'right': player.vel = pygame.math.Vector2(1.25, -0.5)

	def fall_physics(self, player, dt):
		player.acc = pygame.math.Vector2()
		if player.vel.x > 0.5: 
			player.vel.x -= 0.1 * dt
			if player.vel.x <= 0.5: 
				player.vel.x = 0
		elif player.vel.x < -0.5: 
			player.vel.x += 0.1 * dt
			if player.vel.x >= -0.5: 
				player.vel.x = 0

		player.vel.y += 0.1 * dt
		player.pos += player.vel
		player.hitbox.center = round(player.pos)
		player.rect.center = player.hitbox.center

		if self.direction == 'up' and player.vel.y > 0:
			pass

	def get_z_group(self, player):
		for index, group in enumerate(Z_LAYERS):
			if player in group: 
				if player.vel.y > 2 and 'down' in player.edge:
					group.remove(player)
					Z_LAYERS[1].add(player)
				elif player.vel.y > 0  and not 'down' in player.edge:
					group.remove(player)
					Z_LAYERS[1].add(player)

	def state_logic(self, player):
		pass

	def update(self, dt, player):
		self.get_z_group(player)
		self.fall_physics(player, dt)

		player.animate(self.direction + '_edge', 0.2 * dt, 'end')

		if player.vel.y > 4:
			player.game.screenshaking = True






		

		