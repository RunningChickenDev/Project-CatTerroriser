# -*- coding: utf-8 -*-

from operator import itemgetter
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

class ConnEdge:
	"""
	A ConnEdge is a half-edge in a polygon
	with multiple inner faces.

	Fields:
		origin	-	A vertex from where this line comes (the source)
		face	-	An identifier for the face to its left
		twin	-	The half-edge moving in the opposite direction, but along the same vertices
		prev	-	The half-edge preceding this one: this == prev.next
		next	-	The half-edge successing this one: this == next.prev
	"""
	def __init__(self, origin, face, twin, prev, next, helper = None):
		self.origin = origin
		self.face = face
		self.twin = twin
		self.prev = prev
		self.next = next
		self.helper = helper

	def __str__(self):
		return "ConnEdge(from {}, face {})".format(self.origin, self.face)

	def __repr__(self):
		return str(self)

class DCEL:
	"""
	DCEL stands for Doubly Connected Edge List.
	Such a list contains a polygon with within
	chains of vertices.

	The list contains half-edges, represented as ConnEdges.
	See ConnEdge documentation for more.

	This object also remembers how many faces it handles.
	This object also remembers the edges.

	Multiple DCELs will have different objects of
	ConnEdge, as they are different polygons.
	"""
	def __init__(self, vertices, update_vertices = True):
		self.faces = 1
		self.edges = []
		for vertex in vertices:
			self.edges += [ConnEdge(vertex, 0, None, None, None)]
		for i in range(len(self.edges)):
			e = self.edges[i]
			e.next = self.edges[ (i+1) % len(self.edges) ]
			e.prev = self.edges[ (i-1) % len(self.edges) ]

		if update_vertices:
			for e in self.edges:
				e.origin.e = e	# Cool syntax bro

	def insert(self, src, tgt):
		starters = []			# All edges that start at the source
		enders = []				# All edges that start at the target
		for e in self.edges:
			if e.origin is src:
				starters += [e]
			elif e.origin is tgt:
				enders += [e]

		# If starter and ender dont have the same face,
		# it means the diagonal cuts through multiple
		# faces. This is not handled, and returns a ValueError
		se_pair = None
		face = None
		for starter in starters:
			for ender in enders:
				if starter.face == ender.face:
					se_pair = (starter, ender)
					face = starter.face
		if not se_pair:
			raise ValueError("Cannot find a starter/ender-pair on the same face")

		# Cool syntax bro
		new_face = self.new_face()
		left_edge = ConnEdge(src, face, None, se_pair[0].prev, se_pair[1])
		right_edge = ConnEdge(tgt, new_face, None, se_pair[1].prev, se_pair[0])
		left_edge.twin = right_edge
		right_edge.twin = left_edge

		left_edge.prev.next = left_edge
		left_edge.next.prev = left_edge
		right_edge.prev.next = right_edge
		right_edge.next.prev = right_edge

		# Update the new face
		e = right_edge.next
		while e is not right_edge:
			e.face = new_face
			e = e.next

		self.edges += [left_edge]
		self.edges += [right_edge]

	def new_face(self):
		self.faces += 1
		return self.faces - 1

	def _march_face_data(self, e0):
		self._Sf += [e0.face]
		e = e0.next
		while e is not e0:
			if e.twin != None:
				if not self.Sf.contains(e.twin.face):
					self._march_face_data(e)


	def gen_face_data(self, q=["faces","colours"]):
		l = logg.get("DCEL")
		data = {}

		if "faces" in q:
			data["network"] = {}
			polygons = {}
			roots = [self.edges[0]]
			Sf = [self.edges[0].face]
			#per polygon
			while roots:
				e0 = roots.pop()
				e = e0.next
				verts = [e0.origin]
				data["network"][e.face] = []
				#per edge
				while e != e0:
					if e.twin != None:
						data["network"][e.face] += [e.twin.face]
						if e.twin.face not in Sf:
							roots += [e.twin]
							Sf += [e.twin.face]
					verts += [e.origin]
					e = e.next
				if e.twin != None:
					data["network"][e.face] += [e.twin.face]
				polygons[e.face] = verts
				Sf.remove(e.face)
			data["polys"] = polygons

		if "colours" in q:
			if "faces" not in q:
				l.warning("Cannot generate data for DCEL colours if faces are not generated!")
			else:
				data["colours"] = {}
				c = 0
				for face in data["network"].keys():
					potentialis = [0,1,2,3]
					# check neighbors
					for n in data["network"][face]:
						if n in data["colours"]:
							potentialis.remove(data["colours"][n])
					data["colours"][face] = potentialis[c % len(potentialis)]
					c+=1
		return data

	def __str__(self):
		return "A DCEL containing: {}".format(self.edges)

class Vertex:
	def tuples_to_vertices(tuples):
		r = []
		for t in tuples:
			r += [Vertex(t[0], t[1])]
		return r

	def vertices_to_tuples(vertices, whole = False):
		r = []
		for v in vertices:
			if whole:
				vertices += [(int(v.x),int(v.y))]
			else:
				vertices += [(v.x,v.y)]
		return r

	def __init__(self, x, y, e = None):
		self.x = x
		self.y = y
		self.e = e

	def prev(self):
		try:
			return self.e.prev.origin
		except AttributeError:
			logg.get("VTX").error("Could not get previous!")

	def next(self):
		try:
			return self.e.next.origin
		except AttributeError:
			logg.get("VTX").error("Could not get next!")

	def help(self):
		try:
			return self.e.helper
		except AttributeError:
			logg.get("VTX").error("Could not get helper!")

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

class TriangleSweep:
	def triangulate(t):
		r = TriangleSweep(t)
		r.sweep()

	def __init__(self, t):
		self.t = t
		print(t)
		self.l = logg.get("TRI")
		self._l = logg.get("~TRI~")

	def _vxh(self, p, q):
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

		for vertex in vertices:
			if not q:
				q += [vertex]
			else:
				inserted = False
				for entry in q:
					if not inserted and not self._vxh(vertex, entry):
						q.insert(q.index(entry), vertex)
						inserted = True
				if not inserted:
					q += [vertex]
			_l.debug("partial q: %s" , q)

		return q

	def _vertex_type(self, vertex):
		above_prev = self._vxh(vertex, vertex.prev())
		above_next = self._vxh(vertex, vertex.next())
		if above_prev and above_next:
			if vertex.prev().x >= vertex.next().x:
				return "start"
			else:
				return "split"
		elif not above_prev and not above_next:
			if vertex.prev().x <= vertex.next().x:
				return "end"
			else:
				return "merge"
		else:
			return "regular"

	def _handle(self, vertex):
		t = self._vertex_type(vertex)

		self.l.debug("Handling\t%-10s%-10s", str(vertex), t)

		m = getattr(self, "_handle_"+t)
		m(vertex)

	def _handle_start(self, vertex):
		#1: 'Insert e_i in T and set helper(e_i) to v_i'
		self.T += [vertex]
		vertex.e.helper = vertex

	def _handle_end(self, vertex):
		#1: 'if helper(e_i-1) is a merge vertex'
		if self._vertex_type(vertex.prev()) == "merge":
			#2: 'then Insert the diagonal connecting v_i to helper(e_i-1) in D'
			self.queueD += [(vertex, vertex.prev().help())]
		#3: 'Delete e_i-1 from T'
		self.T.remove(vertex.prev())

	def _handle_split(self, vertex):
		#1: 'Search in T to find the edge e_j directly left of v_i'
		left_edge = None
		left_edge_xt = float('inf')
		for v in self.T: # TODO: T should contain only edges, not vertices
			edge = v.e
			if (edge.origin.y >= vertex.y and edge.next.origin.y <= vertex.y) \
					or (edge.origin.y <= vertex.y and edge.next.origin.y >= vertex.y):
				xt = ((vertex.y-edge.origin.y)/(edge.next.origin.y-edge.origin.y)) \
						*(edge.next.origin.x-edge.origin.x)+edge.origin.x
				if xt < vertex.x and xt < left_edge_xt:
					# Found it ~!
					left_edge_xt = xt
					left_edge = edge
		#2: 'Insert the diagonal connecting v_i to helper(e_j) in D'
		self.queueD += [(vertex, left_edge.helper)]
		#3: 'helper(e_j) = v_i'
		left_edge.elperh = vertex
		#4: 'Insert e_i in T and set helper(e_i) to v_i'
		self.T += [vertex]
		vertex.e.helper = vertex

	def _handle_merge(self, vertex):
		#1: 'if helper(e_i-1) is a merge vertex'
		if self._vertex_type(vertex.prev().help()) == "merge":
			#2: 'then Insert the diagonal connecting v_i to helper(e_i-1) in D'
			self.queueD += [(vertex, vertex.prev().help())]
		#3: 'Delete e_i-1 from T'
		self.T.remove(vertex.prev())
		#4: 'Search in T to find the edge e_j directly left of v_i'
		left_edge = None
		left_edge_xt = float('inf')
		for v in self.T: # TODO: T should contain only edges, not vertices
			edge = v.e
			if (edge.origin.y >= vertex.y and edge.next.origin.y <= vertex.y) \
					or (edge.origin.y <= vertex.y and edge.next.origin.y >= vertex.y):
				xt = ((vertex.y-edge.origin.y)/(edge.next.origin.y-edge.origin.y)) \
						*(edge.next.origin.x-edge.origin.x)+edge.origin.x
				if xt < vertex.x and xt < left_edge_xt:
					# Found it ~!
					left_edge_xt = xt
					left_edge = edge
		#5: 'if helper(e_j) is a merge vertex'
		if self._vertex_type(left_edge.helper) == "merge":
			#6: 'then Insert the diagonal connecting v_i to helper(e_j) in D'
			self.queueD += [(vertex, left_edge.helper)]
		#7: 'helper(e_j) = v_i'
		left_edge.helper = vertex

	def _handle_regular(self, vertex):
		#1: 'if the interior of P lies to the right of v_i'
		if vertex.prev().y > vertex.y:	# TODO: I don't think this works
			#2: 'then if helper(e_i-1) is a merge vertex'
			if self._vertex_type(vertex.prev().help()) == "merge":
				#3: 'then Insert the diagonal connecting v_i to helper(e_i-1) in D'
				self.queueD += [(vertex, vertex.prev().help())]
			#4: 'Delete e_i-1 from T'
			self.T.remove(vertex.prev())
			#5: 'Insert e_i in T and set helper(e_i) to v_i'
			self.T += [vertex]
			vertex.e.helper = vertex
		#6: 'else Search in T to find the edge e_j directly left of v_i'
		else:
			left_edge = None
			left_edge_xt = float('inf')
			for v in self.T: # TODO: T should contain only edges, not vertices
				edge = v.e
				if (edge.origin.y >= vertex.y and edge.next.origin.y <= vertex.y) \
						or (edge.origin.y <= vertex.y and edge.next.origin.y >= vertex.y):
					xt = ((vertex.y-edge.origin.y)/(edge.next.origin.y-edge.origin.y)) \
							*(edge.next.origin.x-edge.origin.x)+edge.origin.x
					if xt < vertex.x and xt < left_edge_xt:
						# Found it ~!
						left_edge_xt = xt
						left_edge = edge
			#7: 'if helper(e_j) is a merge vertex'
			if self._vertex_type(left_edge.origin) == "merge":
				#8: 'then Insert the diagonal connecting v_i to helper(e_j) in D'
				self.queueD += [(vertex, left_edge.helper)]
			#9: 'helper(e_j) = v_i'
			left_edge.helper = vertex

	def _recursive_untangle(self, diag = None):
		r = []
		first = 0						if diag == None else min(diag.s, diag.t)
		last = (len(self.vertices)-1)	if diag == None else max(diag.s, diag.t)

		just_returned = False
		i_vertex = first
		while i_vertex < last:
			just_returned = False
			for ddiag in self.D:
				if not just_returned:
					r += [i_vertex]
				else:
					continue
				if ddiag == diag:
					i_vertex += 1
					continue
				if i_vertex == min(ddiag.s, ddiag.t):
					self._recursive_untangle(ddiag)
					i_vertex = max(ddiag.s, ddiag.t)
					just_returned = True
					self._l.debug("returned to {}".format(i_vertex))
				else:
					i_vertex += 1
		r += [last]
		self.monotones += [r]
		self._l.debug("one recursion done: {}".format(r))

	def _chain(self, monotone, j):
		"""
		+1 for the Left chain;
		-1 for the Right chain;
		"""
		if self._vxh(self.vertices[j-1], self.vertices[j]):
			return +1
		else:
			return -1

	def monotone_triangulation(self, monotone):
		"""
		This function is a clusterfuck.
		It triangulates a monotone polygon
		"""
		# In case to monotone is incorrect
		if len(monotone) < 3:
			raise IndexError("A monotone piece must contain at least three vertices!")
		# In case the monotone is a triangle
		if len(monotone) == 3:
			if _sld(self.vertices[monotone[0]], self.vertices[monotone[1]], self.vertices[monotone[2]]) > 0:
				# An anti-clockwise winding triangle
				return [[monotone[0], monotone[1], monotone[2]]]
			else:
				# Clockwise triangle
				return [[monotone[0], monotone[2], monotone[1]]]

		# init status objects
		D = []
		indices = []

		# Up-To-Down Queue
		q = self._q(monotone)
		self.l.debug("Monotone priority queue: {}".format(q))

		S = [0,1]
		for j in range(2,len(monotone)-1):
			self._l.debug("j = %d", j)
			if self._chain(monotone, q[-j-1]) != self._chain(monotone, q[-S[-1]-1]):
				self._l.debug("Non-chain; Current stack: {}".format(S))
				while len(S) > 1:
					p = S.pop()
					D += [Edge(q[-j-1], q[-p-1], None)]
					if self._chain(monotone, q[-j-1]) > 0:
						indices += [[ q[-j-1], q[-p-1], q[-S[-1]-1] ]]
					else:
						indices += [[ q[-j-1], q[-S[-1]-1], q[-p-1] ]]
				S.pop()
				S += [j-1]
				S += [j]
			else:
				self._l.debug("Same chain; Current stack: {}".format(S))
				l = S.pop()
				k = S[-1]
				self._l.debug("j: %d; k: %d; l: %d", j,k,l)
				self._l.debug("q[j]: %d; q[k]: %d; q[l]: %d", q[-j-1],q[-k-1],q[-l-1])

				triwind = _sld(self.vertices[q[-j-1]],self.vertices[q[-k-1]],self.vertices[q[-l-1]]) > 0
				chain = self._chain(monotone, q[-j-1]) > 0

				self._l.debug("Triwind: %d; Chain: %d", triwind, chain)

				while S and triwind == chain:
					l = k
					k = S[-1]
					triwind = _sld(self.vertices[q[-j-1]],self.vertices[q[-k-1]],self.vertices[q[-l-1]]) > 0
					S.pop()
					D += [Edge(q[-j-1], q[-k-1], None)]
					if self._chain(monotone, q[-j-1]) > 0:
						indices += [[ q[-j-1], q[-l-1], q[-k-1] ]]
					else:
						indices += [[ q[-j-1], q[-k-1], q[-l-1] ]]
					self._l.debug(".D %s", D)
				S += [l]
				S += [j]
		self._l.debug("Remainder S: %s", S)
		for us in S[1:-1]:
			D += [Edge(q[-len(monotone)], q[-us-1], None)]
		self._l.debug("D: %s", D)

		self._l.debug("Indices: %s", indices)
		return indices

	def sweep(self):
		self.l.debug("Input (Polygon): %s", self.t.polygon)
		self.l.debug("Input (Holes): %s", self.t.holes)

		# These are iterative arrays
		self.vertices = self.t.polygon
		# These are status objects
		self.T = []
		self.D = DCEL(self.vertices)
		self.queueD = []
		# TODO: add handling for holes

		for e in self.D.edges:
			print("E: " + str(e.prev) + " -> " + str(e.origin) + " -> " + str(e.next))

		self.l.info("Vertices: %s", self.vertices)
		#self.l.info("Edges: %s", self.edges)

		self.q = self._q(vertices)
		self.l.info("Priority Queue (LIFO): %s", self.q)

		# Here starts step 3
		while self.q:
			vertex = self.q.pop()
			self._handle(vertex)

		self.l.info("Done partition shape in y-monotone subsets ...")
		self.l.info("T: {}".format(self.T))
		self.l.debug("Diagonals to add: {}".format(self.queueD))

		# update D
		for queuedItem in self.queueD:
			self.D.insert(queuedItem[0], queuedItem[1])
		self.l.debug("self.D has been updated")

		# now for the monotone handling ...
		self.monotones = []
		self._recursive_untangle()
		self.l.info("Monotones: {}".format(self.monotones))

		# per monotone ...
		self.indices = []
		for monotone in self.monotones:
			self.indices += self.monotone_triangulation(monotone)
			self.l.debug("All indices: {}".format(self.indices))
			indices = self.monotone_triangulation(monotone)
			self.l.debug("Monotone indices: {}".format(indices))


#TODO: Delet this
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
	tuples = [(-1,-2),(0,-1),(1,-2),(2,0),(1,2),(0,1),(-1,2),(-2,0)]
	vertices = Vertex.tuples_to_vertices(tuples)
	t = Triangulation(vertices)

#	D = DCEL(vertices)
#	D.insert(vertices[1], vertices[3])
#	D.insert(vertices[5], vertices[7])
#	screen = vis.open_window()
#	vis.draw_DCEL(screen, D, msg="__main__ test")

	TriangleSweep.triangulate(t)
