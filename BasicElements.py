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
		x2 = round(self.x + distance*cos(angle%pi), 6)
		y2 = round(self.y + distance*sin(angle%pi), 6)
		return Point(x2, y2)

	#Other classic methods

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

	def get_line_function(self):
		'''
		Function to get line equation from available points
		If there is parallel line to vertical axis, there is no one-to-one representative function
		'''
		dx = self.point1.x - self.point2.x
		dy = self.point1.y - self.point2.y

		if dx == 0:
			return None

		k = dy/dx
		b = self.point1.y - k*self.point1.x
		return lambda x: k*x + b

	#Other classic methods

	def __str__(self):
		return f"""Line:
		Point 1: \t{self.point1}, 
		Point 2: \t{self.point2},
		Distance: \t{self.distance},
		Angle:  \t{self.angle}"""

	def __repr__(self):
		return f"Line[{self.point1}, {self.point2}]"