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

class Triangulation:
	"""
	An instance of this class describes
	the outcome of the triangulation algorithm.
	
	The class has functions to create
	triangulation instances.
	"""

	def convex():
		pass

	def monotone():
		pass

	def npolygon():
		pass
	
	def shape(polygon=[], holes=[[]], order='-+'):
		"""
		Triangulates a shape.
		A shape is defined as a polygon border
		with any number of smaller polygon holes.
		
		The order (-+ by default) encodes the winding order
		of the given polygon and holes.
		+ :	Clockwise		winding order
		- : Anti-Clockwise	winding order
		The algorithm is at its fastest when the input
		is given in the order of '-+''
		
		If holes does not contain holes, the function
		triangulate_npolygon is called instead.
		"""
		if holes == None or len(holes) == 0 or len(holes[0]) == 0:
			return Triangulation.triangulate_npolygon()
		
		
	
	def __init__(self, vertices=[], indices=[]):
		self.vertices = vertices
		self.indices = indices
