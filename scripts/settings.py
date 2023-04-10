import pygame, math

FPS = 60
SCALE = 2
TILESIZE = 16 * SCALE
RES = WIDTH, HEIGHT = pygame.math.Vector2(640, 360)#(960, 540)
HALF_WIDTH, HALF_HEIGHT = RES/2

FONT = '../font/Pokemon Classic.ttf'

Z_LAYERS = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]

MX, MY = pygame.math.Vector2(0,0)

# game colours
BLACK = ((9, 9, 14))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((255, 255, 255)) 
BLUE = ((20, 68, 145))
LIGHT_BLUE = ((113, 181, 219))
RED = ((112, 21, 31))
ORANGE = ((227, 133, 36))
PINK = ((195, 67, 92))
GREEN = ((88, 179, 150))
LIGHT_GREEN = ((106, 226, 145))
PURPLE = ((66, 0, 78))
CYAN = ((0, 255, 255))
MAGENTA = ((153, 60, 139))
YELLOW = ((224, 225, 146))

# key events
ACTIONS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False, 'right': False, 'return': False, 'backspace': False, 'left_click': False, 'right_click': False, 'scroll_up': False, 'scroll_down': False}
