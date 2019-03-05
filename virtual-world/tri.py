from operator import itemgetter
import logg

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

	###########
	# LOGGERS #
	###########
	l = logg.get("TRI")			# For standard logging
	_l = logg.get("~TRI~")		# For logging helper methods

	###########
	# HELPERS #
	###########

	def _vxh(p,q):
		"""
		Stands for "VerteX Higher" function.
		Determines if vertex p is above vertex q.
		
		Vertex p is above q if p_y > q_y or,
		when p_y == q_y, if p_x < q_x
		"""
		return (p[1] > q[1]) or ((p[1] == q[1]) and (p[0] < q[0]))
		
	def _q(vertices):
		"""
		Priority Queue
		
		Args:
			vertices (list of lists of 2: [[a,b],[c,d]])
		Returns:
			Priority queue in LIFO-fashion, so it is
			compatible with list.pop() (First pop is highest priority).
		
		"""
		q = []
		
		for i_vertex in range(0, len(vertices)):
			Triangulation._l.debug("i_vertex: %d", i_vertex)
			vertex = vertices[i_vertex]
			if not q:
				q += [i_vertex]
			else:
				inserted = False
				for i_entry in range(0,len(q)):
					if not Triangulation._vxh(vertex, vertices[q[i_entry]]) and not inserted:
						q.insert(i_entry, i_vertex)
						inserted = True
				if not inserted:
					q += [i_vertex]
			Triangulation._l.debug("partial q: %s" , q)

		return q

	#############
	#  HANDLES  #
	#############

	def _vertex_type(i_vertex, vertices, edges):
		if i_vertex == None:
			return None
		vertex = vertices[i_vertex]
		prev_neighbor = vertices[(i_vertex-1) % len(vertices)]
		next_neighbor = vertices[(i_vertex+1) % len(vertices)]
		
		above_prev = Triangulation._vxh(vertex, prev_neighbor)
		above_next = Triangulation._vxh(vertex, next_neighbor)
		if above_prev and above_next:
			if prev_neighbor[1] > next_neighbor[1]:
				return "start"
			else:
				return "split"
		elif not above_prev and not above_next:
			if prev_neighbor[1] < next_neighbor[1]:
				return "end"
			else:
				return "merge"
		else:
			return "regular"

	def _handle(i_vertex, vertices, edges):
		t = Triangulation._vertex_type(i_vertex, vertices, edges)
		
		Triangulation.l.info("Handling %d:%s:%s", i_vertex, vertices[i_vertex], t)
		
		m = getattr(Triangulation, "_handle_"+t)
		m(i_vertex, vertices, edges)

	def _handle_start(i_vertex, vertices, edges):
		edges[i_vertex][2] = i_vertex

	def _handle_end(i_vertex, vertices, edges):
		if Triangulation._vertex_type(edges[i_vertex-1][2], vertices, edges) == "merge":
			# Insert diagonal
			pass

	def _handle_split(i_vertex, vertices, edges):
		pass

	def _handle_merge(i_vertex, vertices, edges):
		pass

	def _handle_regular(i_vertex, vertices, edges):
		pass

	###########
	# METHODS #
	###########
	
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
			#return Triangulation.triangulate_npolygon()
			pass
		
		Triangulation.l.debug("Input (Polygon): %s", polygon)
		Triangulation.l.debug("Input (Holes): %s", holes)
		
		vertices = []
		for v in polygon:
			vertices += [v]
		for hole in holes:
			for v in hole:
				vertices += [v]
		
		# This is the queue (pronounced: q)
		
		edges = []	# Currently incorrect
		for i_vertex in range(0, len(vertices)):
			if i_vertex is not len(vertices)-1:
				edges += [[i_vertex, i_vertex+1, None]]
			else:
				edges += [[i_vertex, 0, None]]
		
		Triangulation.l.info("Vertices: %s", vertices)
		Triangulation.l.info("Edges: %s", edges)
		
		q = Triangulation._q(vertices)
		Triangulation.l.info("Priority Queue (LIFO): %s", q)
		
		# Here starts step 3
		while q:
			i_vertex = q.pop()
			vertex = vertices[i_vertex]
			Triangulation._handle(i_vertex, vertices, edges)
			#print(v)
	
	def __init__(self, vertices=[], indices=[]):
		self.vertices = vertices
		self.indices = indices
		
if __name__ == '__main__':
	Triangulation.shape([(-1,-1),(1,-1),(1,1),(-1,1)])
