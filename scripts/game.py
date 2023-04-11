import sys, pygame, csv
from pygame import mixer
from os import walk
from settings import *

from intro import Intro

class Game():
	def __init__(self):

		pygame.init()

		self.clock = pygame.time.Clock()

		self.screen = pygame.display.set_mode(RES)
		self.screen = pygame.display.set_mode((RES), pygame.FULLSCREEN|pygame.SCALED)

		self.running = True

		#font
		self.big_font = pygame.font.Font(FONT, int(HEIGHT * 0.15))
		self.medium_font = pygame.font.Font(FONT, int(HEIGHT * 0.1))
		self.small_font = pygame.font.Font(FONT, int(HEIGHT * 0.05))

		# states
		self.stack = []

		self.current_zone = 0

		self.load_states()

	def get_events(self):
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					ACTIONS['escape'] = True
					self.running = False
				elif event.key == pygame.K_UP:
					ACTIONS['up'] = True
				elif event.key == pygame.K_DOWN:
					ACTIONS['down'] = True
				elif event.key == pygame.K_RIGHT:
					ACTIONS['right'] = True
				elif event.key == pygame.K_LEFT:
					ACTIONS['left'] = True
				elif event.key == pygame.K_SPACE:
					ACTIONS['space'] = True
				elif event.key == pygame.K_RETURN:
					ACTIONS['return'] = True
				elif event.key == pygame.K_BACKSPACE:
					ACTIONS['backspace'] = True

			if event.type == pygame.KEYUP:

				if event.key == pygame.K_UP:
					ACTIONS['up'] = False
				elif event.key == pygame.K_DOWN:
					ACTIONS['down'] = False
				elif event.key == pygame.K_RIGHT:
					ACTIONS['right'] = False
				elif event.key == pygame.K_LEFT:
					ACTIONS['left'] = False
				elif event.key == pygame.K_SPACE:
					ACTIONS['space'] = False
				elif event.key == pygame.K_RETURN:
					ACTIONS['return'] = False
				elif event.key == pygame.K_BACKSPACE:
					ACTIONS['backspace'] = False

			if event.type == pygame.MOUSEWHEEL:

				if event.y == 1:
					ACTIONS['scroll_up'] = True
				elif event.y == -1:
					ACTIONS['scroll_down'] = True

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					ACTIONS['left_click'] = True
				elif event.button == 3:
					ACTIONS['right_click'] = True
				elif event.button == 4:
					ACTIONS['scroll_down'] = True
				elif event.button == 2:
					ACTIONS['scroll_up'] = True

				print(event.button)

			if event.type == pygame.MOUSEBUTTONUP:

				if event.button == 1:
					ACTIONS['left_click'] = False
				elif event.button == 3:
					ACTIONS['right_click'] = False
				elif event.button == 4:
					ACTIONS['scroll_down'] = False
				elif event.button == 2:
					ACTIONS['scroll_up'] = False


	def reset_keys(self):
		for action in ACTIONS:
			ACTIONS[action] = False

	def update(self):
		pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
		self.stack[-1].update()

	def render(self, screen):
		self.stack[-1].render(screen)
		self.custom_cursor()
		pygame.display.flip()

	def custom_cursor(self):
		mx, my = pygame.mouse.get_pos()
		pygame.mouse.set_visible(False)
		cursor_img = pygame.image.load('../assets/cursor.png').convert_alpha()
		cursor_img = pygame.transform.scale_by(cursor_img, SCALE)
		cursor_img.set_alpha(150)
		cursor_rect = cursor_img.get_rect()
		self.screen.blit(cursor_img, (mx, my))

	def load_states(self):
		self.intro = Intro(self)
		self.stack.append(self.intro)

	def import_folder(self, path):
		surf_list = []

		for _, __, img_files in walk(path):
			for img in img_files:
				full_path = path + '/' + img
				img_surf = pygame.image.load(full_path).convert_alpha()
				img_surf = pygame.transform.scale_by(img_surf, SCALE)
				surf_list.append(img_surf)

		return surf_list

		print(surf_list)

	def get_image(self, path, pos):
		surf = pygame.image.load(path).convert_alpha()
		surf = pygame.transform.scale_by(surf, SCALE)
		rect = surf.get_rect(center = pos)
		return(surf, rect)

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), False, colour)
		rect = surf.get_rect(center = pos)
		self.screen.blit(surf, rect)

	def run(self):
		dt = self.clock.tick(FPS)/1000
		self.get_events()
		self.update()
		self.render(self.screen)

if __name__ == "__main__":
	game = Game()
	while game.running:
		game.run()