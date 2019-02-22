#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

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
	def __init__(self, shape=[], wu_per_m=1, name="null"):
		self.shape = shape
		self.wu_per_m = wu_per_m
		self.name = name

def main():
	with open('room1.json') as f:
		data = json.load(f)
	
	print(data)
	
if __name__ == '__main__':
	main()
	
	print(_sld((-1.0,-1.0), (1.0,-1.0), (0.8,-.75)))
	print(_sld((-1.0,-1.0), (1.0,-1.0), (0.0,-1.25)))
