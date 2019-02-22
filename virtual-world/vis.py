#!/usr/bin/python
# -*- coding: utf-8 -*-

import logg
import pygame

def open_window():
	# initialize the pygame module
	pygame.init()
	pygame.display.set_caption('The CatTerroriser')
	 
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((640,480))
	return screen

def draw_room(screen, room, scalar=100):
	"""
	Room must be an object with attribute 'shape'.
	Shape is an array of arrays containing points
	"""
	l = logg.get('VIS')
	pygame.display.set_caption('The CatTerroriser: Room \'{}\''.format(room.name))
	
	pointlist = []
	for v in room.shape:
		pointlist += [[v[0]*scalar + 320, -v[1]*scalar + 240]]
	
	l.debug('Pointlist: %s', pointlist)
	
	pygame.draw.lines(screen, (255,0,0), True, pointlist, 1)
	pygame.display.flip()
	
	l.info('Opening window ...')
	l.warning('The program will be blocked until the window is closed')
	
	running = True
	# main loop
	while running:
		# event handling, gets all event from the event queue
		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
	
	l.info('Window closed!')
	l.debug('Continuing program ...')
	
if __name__ == '__main__':
	print("This module is not supposed to be executed.")
