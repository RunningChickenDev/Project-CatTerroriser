#!/usr/bin/python
# -*- coding: utf-8 -*-

import logg
from math import sqrt # I don't trust 'import' to load only one thing
import pygame

def open_window():
	# initialize the pygame module
	pygame.init()
	pygame.display.set_caption('The CatTerroriser')
	 
	# create a surface on screen that has the size of 640 x 480
	screen = pygame.display.set_mode((640,480))
	screen.fill([255,255,255])
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

def _vec_getnorm(vec):
	return sqrt(vec[0]**2 + vec[1]**2)

def _vec_setnorm(vec, newnorm):
	l = _vec_getnorm(vec)
	vec[0] *= newnorm/l
	vec[1] *= newnorm/l

def _to_screen(vertices, screen, scalar = 100, shrink = 3.72):
	w, h = screen.get_size()
	vr = []
	if shrink:
		sumx = 0
		sumy = 0
		for v in vertices:
			vr += [[int(v[0])*scalar+w/2,-int(v[1])*scalar+h/2]]
			sumx += vr[-1][0]
			sumy += vr[-1][1]
		mx = sumx/len(vr)
		my = sumy/len(vr)
		for v in vr:
			dir_to_m = [mx-v[0], my-v[1]]
			_vec_setnorm(dir_to_m, shrink)
			v[0] += int(dir_to_m[0])
			v[1] += int(dir_to_m[1])
	else:
		for v in vertices:
			vr += [[int(v[0])*scalar+w/2,-int(v[1])*scalar+h/2]]
	return vr

def draw_DCEL(screen, dcel, scalar=100, msg=""):
	l = logg.get('VIS')
	if msg:
		pygame.display.set_caption('The CatTerroriser: a DCEL (\'{}\')'.format(msg))
	else:
		pygame.display.set_caption('The CatTerroriser: a DCEL')
	
	# cycles through HSV with H = [0,90,180,270], S = 100%, V = 80%
	#color_wheel = [(128,0,0), (64,128,0), (0,128,128), (64,0,128)]
	color_wheel = [(204,0,0), (102,204,0), (0,204,204), (102,0,204)]
	
	data = dcel.gen_face_data()
	for f in data["polys"].keys():
		polygon = data["polys"][f]
		l.debug("Drawing polygon: %s", polygon)
		pl = _to_screen(polygon, screen)
		l.debug("Point list: %s", pl)
		pygame.draw.polygon(screen, color_wheel[data["colours"][f]], pl, 3)
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
