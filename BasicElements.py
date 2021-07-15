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

	def get_equation(self):
		'''
		Function to get line equation coefficients from available points
		Looks like: Ax + By + C = 0
		Returns LineEquation class
		'''
		return LineEquation(self)

	def get_boundaries(self):
		'''Function to get boundary points of line'''
		return self.point1, self.point2

	def get_distance(self):
		'''Function to get distance between boundary points'''
		return self.distance

	def get_angle(self):
		'''Function to get angle between line and horizontal axis'''
		return self.angle

	def is_point_on_line(self, point: Point = Point(0, 0)):
		'''
		Function to check is point (x, y) located on the line
		By default checks is line intersect center of coordinate system
		'''
		return self.get_equation(point) == 0

	def is_point_on_object(self, point: Point = Point(0, 0)):
		'''
		Function to check is point (x, y) located on the sector of line, defined by two boundary points
		'''
		xmin, xmax = min(self.point1.x, self.point2.x), max(self.point1.x, self.point2.x)
		ymin, ymax = min(self.point1.y, self.point2.y), max(self.point1.y, self.point2.y)
		
		xcond = (xmin <= point.x <= xmax)
		ycond = (ymin <= point.y <= ymax)

		return xcond and ycond and self.is_point_on_line(point)

	#Other classic methods

	def __str__(self):
		return f"""Line:
		Point 1: \t{self.point1}, 
		Point 2: \t{self.point2},
		Distance: \t{self.distance},
		Angle:  \t{self.angle}"""

	def __repr__(self):
		return f"Line[{self.point1}, {self.point2}]"

class Circle:
	'''
	Circle - class to work with circles in 2d space
	Containing parameters: 
	- 'center': central point of circle in 2d space
	- 'radius': radius of the circle
	'''

	#Initializer
	def __init__(self, 
			center: Point = Point(0, 0), 
			radius: float = 1
	):
		self.center = center
		self.radius = radius

	#Getters

	def get_equation(self):
		'''
		Function to get circle equation from available parameters
		Looks like: (x-x0)^2 + (y-y0)^2 - r^2 = 0
		Returns function f(Point(x, y)) = (x-x0)^2 + (y-y0)^2 - r^2
		'''
		return CircleEquation(self)

	def get_center(self):
		'''Function to get center point of the circle'''
		return self.center

	def get_radius(self):
		'''Function to get radius of the circle'''
		return self.radius

	def is_point_inside(self, point: Point = Point(0, 0)):
		'''
		Function to get information - is point located inside circle
		'''
		return self.get_equation()(point) < 0

	def is_point_on_object(self, point: Point = Point(0, 0)):
		'''
		Function to get information - is point located on circle boundaries
		'''
		return self.get_equation()(point) == 0

	#Other classic methods

	def __str__(self):
		return f"""Circle:
		Center: \t{self.center}, 
		Radius: \t{self.radius}"""

	def __repr__(self):
		return f"Circle[{self.center}, {self.radius}]"


class LineEquation:
	'''
	LineEquation - class to work with line equations in 2d space
	Containing parameters: 
	- 'line': line in 2d space
	'''
	def __init__(self, 
			line: Line = Line(Point(0, 0), Point(1, 1))
	):
		self.line = line
		self.coefficients = self.generate_equation_coeffitients()
		self.equation = self.generate_equation()

	#Generators

	def generate_equation_coeffitients(self):
		'''
		Function to get line equation coefficients from available points
		Looks like: Ax + By + C = 0
		Returns list of coefficients - [A, B, C]
		'''
		deltas = self.line.point2 - self.line.point1
		A = deltas.y
		B = -deltas.x
		C = self.line.point1.y * deltas.x - self.line.point1.x * deltas.y
		return [A, B, C]

	def generate_equation(self):
		'''
		Function to generate line equation from available points
		Looks like: Ax + By + C = 0
		Returns function f(Point(x, y)) = Ax + By + C
		'''
		A, B, C = self.generate_equation_coeffitients()

		def function(point: Point = Point(0, 0)):
			'''Function of the line f(Point(x, y)) = Ax + By + C'''
			if not isinstance(point, Point):
				point = Point(0, 0)

			return A*point.x + B*point.y + C

		return function

	#Getters

	def get_equation(self):
		return self.equation

	def get_equation_coefficients(self):
		return self.coefficients

	#Other classic methods:

	def __str__(self):
		return f"Line equation: {self.coefficients[0]} x + {self.coefficients[1]} y + {self.coefficients[2]} = 0"

	def __repr__(self):
		return self.__str__()

	def __call__(self, point: Point = Point(0, 0)):
		return self.equation(point)

class CircleEquation:
	'''
	CircleEquation - class to work with circle equations in 2d space
	Containing parameters: 
	- 'circle': circle in 2d space
	'''
	def __init__(self, circle: Circle = Circle(Point(0, 0), 1)):
		self.circle = circle
		self.equation = self.generate_equation()

	#Generator

	def generate_equation(self):
		'''
		Function to generate circle equation from available center and radius
		Looks like: (x-x0)^2 + (y-y0)^2 - r^2 = 0
		Returns function f(Point(x, y)) = (x-x0)^2 + (y-y0)^2 - r^2
		'''
		def function(point: Point = Point(0, 0)):
			'''Function of the circle f(Point(x, y)) = (x-x0)^2 + (y-y0)^2 - r^2'''
			if not isinstance(point, Point):
				point = Point(0, 0)

			deltas = self.point-self.circle.center
			return deltas.x**2 + deltas.y**2 - self.circle.radius**2

		return function

	#Getters

	def get_equation(self):
		return self.equation

	#Other classic methods:

	def __str__(self):
		return f"Circle equation: (x - {self.circle.center.x})^2 + (y - {self.circle.center.y})^2 - {self.circle.radius}^2 = 0"

	def __repr__(self):
		return self.__str__()

	def __call__(self, point: Point = Point(0, 0)):
		return self.equation(point)