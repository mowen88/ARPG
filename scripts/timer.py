import pygame

class Timer:
	def __init__(self, duration):
		self.duration = duration
		#self.func = func
		self.start_time = 0
		self.active = False

	def start(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def stop(self):
		self.active = False
		self.start_time = 0

	def update(self):
		time = pygame.time.get_ticks()
		if time - self.start_time >= self.duration:
			self.stop()
			# if self.func:
			# 	self.func()