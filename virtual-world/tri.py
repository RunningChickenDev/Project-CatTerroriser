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

class Vertex:
	def __init__(self, x, y, p=None,n=None):
		self.x = x
		self.y = y
		self.p = p
		self.n = n
	
	def __getitem__(self, idx):
		if idx == 0:
			return self.x
		elif idx == 1:
			return self.y
		else:
			raise IndexError()
	
	def __str__(self):
		return "[{}, {}]".format(self.x, self.y)
	
	def __repr__(self):
		return "Vertex({}, {})".format(self.x, self.y)

class Edge:
	def __init__(self, source, target, helper, idx = -1):
		self.s = source
		self.t = target
		self.h = helper
		self.idx = idx
	
	def __getitem__(self, idx):
		if idx == 0:
			return self.s
		elif idx == 1:
			return self.t
		elif idx == 2:
			return self.h
		else:
			raise IndexError()
	
	def __str__(self):
		return "({} -> {}; help: {})".format(self.s, self.t, self.h)
	
	def __repr__(self):
		return "Edge({}, {}, {})".format(self.s, self.t, self.h)

class TriangleSweep:
	def triangulate(t):
		r = TriangleSweep(t)
		r.sweep()

	def __init__(self, t):
		self.t = t
		print(t)
		self.l = logg.get("TRI")
	
	def _helper(self, edge):
		if edge[2]:
			return edge[2]
		else:
			self.l.error("Edge did not have helper! %s", edge)
			return None
			
	
	def _vxh(self, p,q):
		"""
		Stands for "VerteX Higher" function.
		Determines if vertex p is above vertex q.
		
		Vertex p is above q if p_y > q_y or,
		when p_y == q_y, if p_x < q_x
		"""
		return (p.y > q.y) or ((p.y == q.y) and (p.x < q.x))
	
	def _q(self, vertices):
		"""
		Priority Queue
		
		Args:
			vertices (list of lists of 2: [[a,b],[c,d]])
		Returns:
			Priority queue in LIFO-fashion, so it is
			compatible with list.pop() (First pop is highest priority).
		
		"""
		q = []
		_l = logg.get("~TRI~")
		
		for i_vertex in range(0,len(self.vertices)):
			if not q:
				q += [i_vertex]
			else:
				inserted = False
				for i_entry in range(0,len(q)):
					if not self._vxh(self.vertices[i_vertex], self.vertices[q[i_entry]]) and not inserted:
						q.insert(i_entry, i_vertex)
						inserted = True
				if not inserted:
					q += [i_vertex]
			_l.debug("partial q: %s" , q)

		return q
	
	def _vertex_type(self, o):
		if hasattr(o, 's'):
			vertex = o.s
		elif hasattr(o, 'x'):
			vertex = o
		elif o == None:
			return None
		else:
			vertex = self.vertices[o]
		
		above_prev = self._vxh(vertex, vertex.p)
		above_next = self._vxh(vertex, vertex.n)
		if above_prev and above_next:
			if vertex.p.x >= vertex.n.x:
				return "start"
			else:
				return "split"
		elif not above_prev and not above_next:
			if vertex.p.x <= vertex.n.x:
				return "end"
			else:
				return "merge"
		else:
			return "regular"

	def _handle(self, i_vertex):
		t = self._vertex_type(i_vertex)
		
		self.l.debug("Handling  %-5d%-10s%-10s", i_vertex, self.vertices[i_vertex], t)
		
		m = getattr(self, "_handle_"+t)
		m(i_vertex)

	def _handle_start(self, i_vertex):
		#1
		self.T += [i_vertex]
		self.edges[i_vertex].h = i_vertex

	def _handle_end(self, i_vertex):
		#1
		if self._vertex_type(self.edges[i_vertex-1].h) == "merge":
			#2
			self.D += [Edge(self.vertices[i_vertex], self.edges[i_vertex-1].h, None)]
		#3
		self.T.remove((i_vertex-1) % len(self.vertices))

	def _handle_split(self, i_vertex):
		vertex = self.vertices[i_vertex]
		#1
		left_edge = []
		left_edge_xt = float('inf')
		for e_i in self.T:
			edge = self.edges[e_i]
			if (edge.s.y >= vertex.y and edge.t.y <= vertex.y) or (edge.s.y <= vertex.y and edge.t.y >= vertex.y):
				xt = ((vertex.y-edge.s.y)/(edge.t.y-edge.s.y))*(edge.t.x-edge.s.x)+edge.s.x
				if xt < vertex.x and xt < left_edge_xt:
					# Found it ~!
					left_edge_xt = xt
					left_edge = edge
		#2
		self.D += [Edge(i_vertex, self._helper(left_edge), None)]
		#3
		left_edge.h = i_vertex
		#4
		self.T += [i_vertex]
		self.edges[i_vertex].h = i_vertex
		

	def _handle_merge(self, i_vertex):
		vertex = self.vertices[i_vertex]
		#1
		if self._vertex_type(self.edges[i_vertex-1].h) == "merge":
			#2
			self.D += [Edge(i_vertex, self.edges[i_vertex-1].h, None)]
		#3
		self.T.remove((i_vertex-1) % len(self.vertices))
		#4
		left_edge = None
		left_edge_xt = float('inf')
		for e_i in self.T:
			edge = self.edges[e_i]
			if (edge.s.y >= vertex.y and edge.t.y <= vertex.y) or (edge.s.y <= vertex.y and edge.t.y >= vertex.y):
				xt = ((vertex.y-edge.s.y)/(edge.t.y-edge.s.y))*(edge.t.x-edge.s.x)+edge.s.x
				if xt < vertex.x and xt < left_edge_xt:
					# Found it ~!
					left_edge_xt = xt
					left_edge = edge
		#5
		if self._vertex_type(left_edge) == "merge":
			#6
			self.D += [Edge(i_vertex, self._helper(left_edge), None)]
		#7
		left_edge.h = i_vertex

	def _handle_regular(self, i_vertex):
		vertex = self.vertices[i_vertex]
		#1
		if self.vertices[i_vertex-1].y > self.vertices[i_vertex].y:
			#2
			if self._vertex_type(self.edges[i_vertex-1].h) == "merge":
				#3
				self.D += [Edge(i_vertex, self._helper(self.edges[i_vertex-1]), None)]
			#4
			self.T.remove((i_vertex-1) % len(self.vertices))
			#5
			self.T += [i_vertex]
			self.edges[i_vertex].h = i_vertex
		#6
		else:
			left_edge = None
			left_edge_xt = float('inf')
			for e_i in self.T:
				edge = self.edges[e_i]
			if (edge.s.y >= vertex.y and edge.t.y <= vertex.y) or (edge.s.y <= vertex.y and edge.t.y >= vertex.y):
				xt = ((vertex.y-edge.s.y)/(edge.t.y-edge.s.y))*(edge.t.x-edge.s.x)+edge.s.x
				if xt < vertex.x and xt < left_edge_xt:
					# Found it ~!
					left_edge_xt = xt
					left_edge = edge
			#7
			if self._vertex_type(left_edge) == "merge":
				#8
				self.D += [Edge(i_vertex, self._helper(left_edge), None)]
			#9
			left_edge.h = i_vertex

	def sweep(self):
		self.l.debug("Input (Polygon): %s", self.t.polygon)
		self.l.debug("Input (Holes): %s", self.t.holes)
		
		self.vertices = []
		for v in self.t.polygon:
			self.vertices += [Vertex(v[0],v[1])]
		#for hole in self.t.holes:
		#	for v in hole:
		#		self.vertices += [TriangleSweep.Vertex(v[0],v[1])]
		
		self.edges = []	# Currently incorrect
		for i_vertex in range(0, len(self.vertices)):
			if i_vertex is not len(self.vertices)-1:
				e = Edge(self.vertices[i_vertex], self.vertices[i_vertex+1], None)
				e.s.n = e.t
				e.t.p = e.s
				self.edges += [e]
			else:
				e = Edge(self.vertices[i_vertex], self.vertices[0], None)
				e.s.n = e.t
				e.t.p = e.s
				self.edges += [e]
		
		self.l.info("Vertices: %s", self.vertices)
		self.l.info("Edges: %s", self.edges)
		
		self.q = self._q(self.vertices)
		self.l.info("Priority Queue (LIFO): %s", self.q)
		
		# These are status objects
		# They lack the correct data structures,
		# because they are in Python
		self.T = []
		self.D = []
		
		# Here starts step 3
		while self.q:
			i_vertex = self.q.pop()
			self._handle(i_vertex)
		
		self.l.info("Done!")
		self.l.info("T: {}".format(self.T))
		self.l.info("D: {}".format(self.D))
		

class Triangulation:
	"""
	An instance of this class describes
	the outcome of the triangulation algorithm.
	
	The class has functions to create
	triangulation instances.
	"""

	###########
	# HELPERS #
	###########

	#############
	#  HANDLES  #
	#############

	###########
	# METHODS #
	###########
	
	def __init__(self, polygon=[], holes=[[]], vertices=[], indices=[]):
		self.polygon = polygon
		self.holes = holes
		self.vertices = vertices
		self.indices = indices
		
if __name__ == '__main__':
#	s = Triangulation([(-1,-1),(1,-1),(1,1),(-1,1)])
	s = Triangulation([(-1,-2),(0,-1),(1,-2),(2,0),(1,2),(0,1),(-1,2),(-2,0)])
	TriangleSweep.triangulate(s)
