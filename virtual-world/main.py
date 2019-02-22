#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
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
	│           │        │  and a P is the middle,
	│     P     │        │  then the _sdl of each next vertex in
	│           │        │	anti-clockwise manner will result in
	v           │        │	_sdl(v1, v2, p) == +0.5
	A─────────>>B        ┘
	         
	"""
	return (p[0] - b[0])*(a[1] - b[1]) - (p[1] - b[1])*(a[0] - b[0])

class Room:
	def from_json(path='room1.json'):
		with open(path) as f:
			data = json.load(f)
		
		r = Room(name=data["name"], wu_per_m=data["wu_per_m"], shape=data["shape"])
		print(r.shape)
		return r

	def __init__(self, name="null", wu_per_m=1, shape=[], obstacles=[]):
		# These are some basic user information
		self.name = name
		self.wu_per_m = wu_per_m
		
		# These arrays contain raw data (not used later)
		self.shape = shape
		self.obstacles = obstacles
		
		# These are what store all information!
		self.vertices = []
		self.triangles = []
		
		self._triangulate()
		
	def _triangulate(self):
		# TODO: some magic (sweep algorithm)
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

def main():
	room = Room.from_json('room3.json')
	screen = vis.open_window()
	vis.draw_room(screen, room, 50)
	
	
if __name__ == '__main__':
	main()
	
	print(_sld((-1.0,-1.0), (1.0,-1.0), (0.8,-.75)))
	print(_sld((-1.0,-1.0), (1.0,-1.0), (0.0,-1.25)))
