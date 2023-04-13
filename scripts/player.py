import math
from settings import *
from state_machine import Idle
from timer import Timer
from objects import Object

class Player(Object):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.game = game
		self.zone = zone

		self.acc = 0.4
		self.friction = 0.4
		self.max_speed = 3
		self.vel = pygame.math.Vector2()

		self.import_imgs()

		self.state = Idle('up')
		self.animation_type = 'loop'
		self.frame_index = 0

		self.image = self.animations['down_idle'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.2)

		self.moving_right, self.moving_left = False, False
		self.moving_down, self.moving_up = False, False

	def animate(self, state, animation_speed, anmimation_type):
		self.frame_index += animation_speed
		if anmimation_type == 'end' and self.frame_index >= len(self.animations[state])-1:
			self.frame_index = len(self.animations[state])-1
		else:
			self.frame_index = self.frame_index % len(self.animations[state])
		self.image = self.animations[state][int(self.frame_index)]

	def collisions(self, direction):

		# all stairs
		for sprite in self.zone.stair_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.rect.colliderect(self.hitbox):

					if sprite.col == '1':
						self.vel.y = self.vel.x
						if self.moving_up:
							self.vel.y -= self.vel.x * (self.vel.y * 0.3)
						elif self.moving_down:
							self.vel.y += self.vel.x * (self.vel.y * 0.3)

					elif sprite.col == '2':
						self.vel.y = -self.vel.x
						if self.moving_up:
							self.vel.y += self.vel.x * (self.vel.y * 0.3)
						elif self.moving_down:
							self.vel.y -= self.vel.x * (self.vel.y * 0.3)

		# all walls
		for sprite in self.zone.wall_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.rect.colliderect(self.hitbox):
					rel_x = sprite.hitbox.x - self.hitbox.x
					rel_y = sprite.hitbox.y - self.hitbox.y

					if sprite.col == '5':
						# normal swuare block collisions....

						if direction == 'x':
							if self.vel.x > 0:
								self.hitbox.right = sprite.hitbox.left

							if self.vel.x < 0:
								self.hitbox.left = sprite.hitbox.right

						if direction == 'y':	
							if self.vel.y > 0:
								self.hitbox.bottom = sprite.hitbox.top
							if self.vel.y < 0:
								self.hitbox.top = sprite.hitbox.bottom

					elif sprite.col == '6':
						# moving right and diagonal up
						
						target_y = sprite.hitbox.top + rel_x
						target_x = sprite.hitbox.left + rel_y

						if self.hitbox.top >= target_y:
							self.hitbox.top = target_y
							self.hitbox.left = target_x

					elif sprite.col == '7':
						# moving left and diagonal up
						
						target_y = sprite.hitbox.top - rel_x
						target_x = sprite.hitbox.left - rel_y

						if self.hitbox.top >= target_y:
							self.hitbox.top = target_y
							self.hitbox.left = target_x

					elif sprite.col == '8':
						# moving right and diagonal down
						
						target_y = sprite.hitbox.top - rel_x
						target_x = sprite.hitbox.left - rel_y

						if self.hitbox.top <= target_y:
							self.hitbox.top = target_y
							self.hitbox.left = target_x

					elif sprite.col == '9':
						# moving left and diagonal down
						
						target_y = sprite.hitbox.top + rel_x
						target_x = sprite.hitbox.left + rel_y

						if self.hitbox.top <= target_y:
							self.hitbox.top = target_y
							self.hitbox.left = target_x
			
						
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
		self.collisions('x')
		self.rect.centerx = self.hitbox.centerx
		
		self.hitbox.centery += self.vel.y
		self.collisions('y')
		self.rect.centery = self.hitbox.centery
		

	def state_logic(self):
		new_state = self.state.state_logic(self)
		self.state = new_state if new_state is not None else self.state
		
	def import_imgs(self):
		self.animations = {'down_attack':[], 'up_attack':[], 'right_attack':[], 'left_attack':[], 'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}

		for animation in self.animations.keys():
			full_path = '../assets/player/' + animation
			self.animations[animation] = self.game.import_folder(full_path)

	def update(self):
		
		self.state.update(self)
		self.state_logic()


	def render(self, screen):
		pass

