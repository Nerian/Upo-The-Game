import os
import pygame
from sys import exit


def load_png(name):
	fullname = os.path.join('Data', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
        	print 'Cannot load image:', fullname
        	raise SystemExit, message
	return image, image.get_rect()