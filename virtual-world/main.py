#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logg
import vis

def _sld(a, b, p):
	"""
	Returns the distance from line AB to point P.
	
	This distance is signed: if the point P is to the left
	of the arrow from A to B, the _sld will be positive.
	If it is to the right, it will be negative.
	
	== Example 1 ==
	
	         P           ╗
	         |           ║ _sld(a, b, p) = +1
	A--------*----->>>B  ╣
	         |           ║ _sld(a, b, q) = -1
	         Q           ╝
	         
	== Example 2 ==
	
	D<<─────────C        ┐
	│           ^        │	If ABCD is a square from 0,0 to 1,1,
	│     v     │        │  and a P is the middle,
	│    >P<    │        │  then the _sdl of each next vertex in
	│     ^     │        │	anti-clockwise manner will result in
	v           │        │	_sdl(v1, v2, p) == +0.5
	A─────────>>B        ┘
	         
	"""
	return (p[0] - b[0])*(a[1] - b[1]) - (p[1] - b[1])*(a[0] - b[0])

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
		Room.l.critical("No triangulation algorithm!")
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
