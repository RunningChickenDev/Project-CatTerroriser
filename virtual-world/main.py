#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logg
import tri
import vis

class Room:
	l = logg.get("ROOM")

	def from_json(path='room1.json'):
		with open(path) as f:
			data = json.load(f)
		
		r = Room(**data)	# ** is called a splat operator
		Room.l.debug("Room interpeted as %s", repr(r))
		return r

	def __init__(self, **kwargs):
		# Data variables (user information + winding vertices)
		self.name = kwargs['name']				if 'name' in kwargs			else 'null'
		self.wu_per_m = kwargs['wu_per_m']		if 'wu_per_m' in kwargs		else 1
		self.shape = kwargs['shape']			if 'shape' in kwargs		else []
		self.obstacles = kwargs['obstacles']	if 'obstacles' in kwargs	else [[]]
		
		# These are what store all information!
		self.vertices = []
		self.triangles = []
		
		self._triangulate()
		
	def _triangulate(self):
		# TODO: some magic (sweep algorithm)
		Room.l.critical("Triangulation algorithm not finished yet!")
		pass
	
	def _union(self, other):
		"""
		This will return the union of two rooms,
		defined as another room
		"""
		pass
	
	def vision(self, a, d):
		"""
		The distance to the first wall from
		point A in direction D (2D vector)
		"""
		pass
	
	def path_find(self, a, b, rad):
		"""
		Finds the shortest path between A and B,
		assuming the pathwalker is has a certain radius
		
		This is not implemented
		"""
		pass
		
	def __repr__(self):
		return 'Room(**{})'.format(self.__dict__)

def main():
	room = Room.from_json('room3.json')
	screen = vis.open_window()
	vis.draw_room(screen, room, 50)
	
if __name__ == '__main__':
	main()
