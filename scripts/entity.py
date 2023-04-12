import math
from settings import *
from state_machine import Idle
from timer import Timer

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.game = game
		self.zone = zone

		self.image = pygame.Surface((25, 25))
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(0, 0)
		self.vel = pygame.math.Vector2()
		self.acc = 0.25
		self.friction = 0.25
		self.max_speed = 2

	def switch_layer(self):
		for group in self.zone.layers:
			if self in group:
				new_group = self.zone.layers.index(group)-1
				group.remove(self)
				self.zone.layers[new_group].add(self)

	def animate(self, state, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.animations[state])
		self.image = self.animations[state][int(self.frame_index)]

	def collisions(self, direction):
		for sprite in self.zone.collidable_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'x':
						if self.vel.x >= 0:
							self.hitbox.right = sprite.hitbox.left
						if self.vel.x <= 0:
							self.hitbox.left = sprite.hitbox.right
					if direction == 'y':
						if self.vel.y >= 0:
							self.hitbox.bottom = sprite.hitbox.top
						if self.vel.y <= 0:
							self.hitbox.top = sprite.hitbox.bottom
						

	def accelerate(self):

		if self.moving_down:
			self.vel.y += self.acc
		elif self.moving_up:
			self.vel.y -= self.acc

		if self.moving_right:
			self.vel.x += self.acc
		elif self.moving_left:
			self.vel.x -= self.acc


	def decelerate(self, friction):
		
		if self.vel.y > 0:
			self.vel.y -= friction
		elif self.vel.y < 0:
			self.vel.y += friction
		else:
			self.vel.y = 0

		if self.vel.x > 0:
			self.vel.x -= friction
		elif self.vel.x < 0:
			self.vel.x += friction
		else:
			self.vel.x = 0

		# if the movement is less than 0.1 stay still, otherwise player moves up and left slightly?
		if self.vel.magnitude() < self.acc:
			self.vel = pygame.math.Vector2()

	def move(self, max_speed):
		pass
		# normalize speed for diagonal, max speed may be lower depending on acc and friction values (might resolve to a lower value than the max speed as friction builds up)
		if self.vel.magnitude() >= max_speed:
			self.vel = self.vel.normalize() * max_speed
	
		# move the entity
		self.hitbox.centerx += self.vel.x
		self.rect.centerx = self.hitbox.centerx
		self.collisions('x')
		self.hitbox.centery += self.vel.y
		self.rect.centery = self.hitbox.centery
		self.collisions('y')

	def update(self):
		pass

	def render(self, screen):
		pass

class Player(Entity):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.acc = 0.4
		self.friction = 0.4
		self.max_speed = 3

		self.import_imgs()

		self.state = Idle('up')
		self.animation_type = 'loop'
		self.frame_index = 0

		self.image = self.animations['down_idle'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.2)


		self.moving_right, self.moving_left = False, False
		self.moving_down, self.moving_up = False, False
		self.cardinal_directions = ['down', 'up', 'right', 'left']

	def state_logic(self):
		new_state = self.state.state_logic(self)
		self.state = new_state if new_state is not None else self.state
		
	def import_imgs(self):
		self.animations = {'down_attack':[], 'up_attack':[], 'right_attack':[], 'left_attack':[], 'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}

		for animation in self.animations.keys():
			full_path = '../assets/player/' + animation
			self.animations[animation] = self.game.import_folder(full_path)

	def input(self):
		keys = pygame.key.get_pressed()

		if ACTIONS['space']:
			print('yes')
			self.attacking.start()

		if keys[pygame.K_RIGHT]:
			self.moving_right = True
		else:
			self.moving_right = False
			
		if keys[pygame.K_LEFT]:
			self.moving_left = True	
		else:
			self.moving_left = False
			
		if keys[pygame.K_DOWN]:
			self.moving_down = True
		else:
			self.moving_down = False

		if keys[pygame.K_UP]:
			self.moving_up = True
		else:
			self.moving_up = False

	# def change_state(self, new_state, new_frame_rate, new_animation_type):
	# 	if self.state != new_state:
	# 		self.frame_index = 0
	# 		self.state = new_state
	# 		self.frame_rate = new_frame_rate
	# 		self.animation_type = new_animation_type

	# def set_state(self):
		# initialize states in order of priority...
		

		# # loop to control state switching from general moving and idling
		# elif self.state in self.cardinal_directions:
		# 	for state in self.cardinal_directions:	
		# 		if self.vel.magnitude() < 0.5 and self.state == state:
		# 			state = state.split('_')[0] + '_idle'
		# 			self.change_state(state, 0.2, 'loop')

		# 		elif self.state == state:
		# 			self.change_state(state, 0.2, 'loop')

	def update(self):
		
		self.state.update(self)
		self.state_logic()


	def render(self, screen):
		pass

