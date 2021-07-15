from math import atan, pi, sin, cos

class Point:
	'''
	Point - class to work with point in 2d space
	Containing parameters: 
	- 'x' coordinate in space
	- 'y' coordinate in space
	'''

	#Initializer
	def __init__(self, x: float = 0, y: float = 0):
		self.x = x
		self.y = y

	#Getters

	def get_distance(self, point2: 'Point'):
		'''Distance between two points (by default - distance between point and coordinate system center)'''
		
		if not isinstance(point2, Point):
			point2 = Point(0, 0)

		dx = self.x - point2.x
		dy = self.y - point2.y
		return (dx**2 + dy**2)**(1/2)

	def get_horizontal_angle(self, point2: 'Point'):
		'''Angle (in radians modulo PI) between line by 2 points and horizontal axis (by default - angle between line connect coordinate system center and horizontal axis)'''
		
		if not isinstance(point2, Point):
			point2 = Point(0, 0)

		dx = self.x - point2.x
		dy = self.y - point2.y
		
		#To except division by zero, set default value for arctan(infty)
		if dx == 0:
			return pi/2

		return atan(dy/dx)%pi

	def get_second_point_from_angle_distance(self, angle: float, distance: float):
		'''
		Generate second point from first, distance and angle:
		- 'angle' - angle in radians of oriented line (between 0 and PI)
		- 'distance' - distance between points (can be negative to orientate it in negative direction)
		'''
		deltapoint = Point(
			round(distance*cos(angle%pi), 6), 
			round(distance*sin(angle%pi), 6)
		)
		return self+deltapoint

	#Other classic methods

	def __add__(self, point2: 'Point'):
		if not isinstance(point2, Point):
			point2 = Point(0, 0)

		return Point(self.x + point2.x, self.y + point2.y)

	def __mul__(self, number: float):
		return Point(self.x*number, self.y*number)

	def __radd__(self, point2: 'Point'):
		return self.__add__(point2)

	def __sub__(self, point2: 'Point'):
		return self.__add__(point2.__mul__(-1))

	def __rsub__(self, point2: 'Point'):
		return point2.__add__(self.__mul__(-1))

	def __div__(self, number: float):
		return self.__mul__(1/number)

	def __str__(self):
		return f"Point({self.x}, {self.y})"

	def __repr__(self):
		return self.__str__()

	def __iter__(self):
		'''Method for converting coordinates to tuples and lists'''
		for i in [self.x, self.y]:
			yield i


class Line:
	'''
	Line - class to work with lines and line sectors in 2d space
	Containing parameters: 
	- 'point1': first point in 2d space (order doesn't matter)
	- 'point2': second point in 2d space
	Also independent parameters:
	- 'angle': angle in radians between line and horizontal axis
	- 'distance': distance between two points
	'''

	#Initializer
	def __init__(self, 
			point1: Point = Point(0, 0), 
			point2: Point = Point(1, 1)
	):
		self.point1 = point1
		self.point2 = point2
		self.angle = Point.get_horizontal_angle(self.point1, self.point2)
		self.distance = round(Point.get_distance(self.point1, self.point2), 6)

	@staticmethod
	def from_angle_distance_point(
			angle: float, 
			distance: float, 
			point: Point = Point(0, 0)
	):
		'''
		Generate line from one point, angle and distance:
		- 'angle' - angle in radians of oriented line (between 0 and PI)
		- 'distance' - distance between points (can be negative to orientate it in negative direction)
		- 'point' - first point in 2d space
		'''
		if not isinstance(point, Point):
			point = Point(0, 0)

		point2 = point.get_second_point_from_angle_distance(angle, distance)
		return Line(point, point2)

	#Getters

	def get_line_equation(self):
		'''
		Function to get line equation coefficients from available points
		Looks like: Ax + By + C = 0
		Returns function f(x, y) = Ax + By + C
		'''
		deltas = self.point2 - self.point1
		A = deltas.y
		B = -deltas.x
		C = self.point1.y * deltas.x - self.point1.x * deltas.y

		#Generate function of the line
		def equation(point: Point = Point(0, 0)):
			if not isinstance(point, Point):
				point = Point(0, 0)

			return A*point.x + B*point.y + C

		return equation

	def is_point_on_line(self, point: Point = Point(0, 0)):
		'''
		Function to check is point (x, y) located on the line
		By default checks is line intersect center of coordinate system
		'''
		return self.get_line_equation(point) == 0

	def is_point_on_sector(self, point: Point = Point(0, 0)):
		'''
		Function to check is point (x, y) located on the sector of line, defined by two boundary points
		'''
		
		xmin, xmax = min(self.point1.x, self.point2.x), max(self.point1.x, self.point2.x)
		ymin, ymax = min(self.point1.y, self.point2.y), max(self.point1.y, self.point2.y)
		
		xcond = (xmin <= point.x <= xmax)
		ycond = (ymin <= point.y <= ymax)

		return xcond && ycond && self.is_point_on_line(point)

	#Other classic methods

	def __str__(self):
		return f"""Line:
		Point 1: \t{self.point1}, 
		Point 2: \t{self.point2},
		Distance: \t{self.distance},
		Angle:  \t{self.angle}"""

	def __repr__(self):
		return f"Line[{self.point1}, {self.point2}]"