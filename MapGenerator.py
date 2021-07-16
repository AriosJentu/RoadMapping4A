import math

import Abstracts
import BasicElements
import MapElements
import Functions

class MapInfo:
	'''
	MapInfo - class with generated information about specific map 2d space
	Containing parameters: 
	- 'outside_lines': list of outside lines List[MapElements.MapLine]
	- 'inside_lines': list of inside lines List[MapElements.MapLine]
	- 'connecting_lines': list of connecting lines List[MapElements.MapLine]
	- 'outside_circles': list of outside circles List[MapElements.MapCircle]
	- 'inside_circles': list of inside circles List[MapElements.MapCircle]
	'''
	def __init__(self,
			outside_lines: list,
			inside_lines: list,
			connecting_lines: list,
			outside_circles: list,
			inside_circles: list,
	):
		self.outside_lines = outside_lines
		self.inside_lines = inside_lines
		self.connecting_lines = connecting_lines
		self.outside_circles = outside_circles
		self.inside_circles = inside_circles


class Generator:
	'''
	Generator - class to generate specific map in 2d space
	Containing parameters: 
	- 'outside_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'inside_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'connecting_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'outside_circle' parameters [Abstracts.AbstractMapCircleParameters]
	- 'inside_circle' parameters [Abstracts.AbstractMapCircleParameters]
	- 'sides_count': count of the map sides
	- 'generation_count: count of generations of inside lines
	- 'noise_distance': function of one integer variable, which generates noise for distance between points
	- 'noise_scale_length': function of one integer variable, which generates noise for scaling factor of generations
	This class generates map with equilateral sides polygon
	'''

	def __init__(self,
			outside_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["outside"],
			inside_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["inside"],
			connecting_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["connecting"],
			outside_circle: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["outside"],
			inside_circle: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["inside"],
			sides_count: int = 3,
			generation_count: int = 1,
			noise_distance=lambda n: n,
			noise_scale_length=lambda n: n,
	):
		self.outside_line = outside_line
		self.inside_line = inside_line
		self.connecting_line = connecting_line

		self.outside_circle = outside_circle
		self.inside_circle = inside_circle

		self.sides_count = max(int(sides_count), 3)
		self.generation_count = max(int(generation_count), 1)

		self.noise_distance = noise_distance
		self.noise_scale_length = noise_scale_length

		#Generation
		self.g_outside_lines = self.generate_outside_lines()
		self.g_inside_lines = [self.generate_inside_lines(i+1) for i in range(self.generation_count)]
		self.g_connecting_lines = [self.generate_connecting_lines(i) for i in range(self.generation_count+1)]
		self.g_outside_circles = self.generate_outside_circles()
		self.g_inside_circle = self.generate_inside_circle()

	#Generators

	def generate_pivot_points(self):
		'''Function to generate pivot points, depends of outside line length and outside circle radius'''
		
		#Calculate real side length using line length and circle radius
		line_length = self.outside_line.length
		circle_radius = self.outside_circle.radius
		side_length = line_length + 2*circle_radius

		#Calculate angle from sides count
		angle = 2*math.pi/self.sides_count

		#Calculate distance from center to points
		central_radius = (side_length/2)/math.sin(angle/2)

		points = []
		for k in range(self.sides_count):
			#Reverse X and Y parameters, which made points counterclock-wise, but with point on the top of the map
			x = round(central_radius*math.sin(k*angle), 10)
			y = round(central_radius*math.cos(k*angle), 10)
			points.append(BasicElements.Point(x, y))

		return points

	def generate_outside_lines(self):
		'''Function to generate outside lines by pivot points'''
		lines = []
		points = self.generate_pivot_points()
		
		for i, point in enumerate(points):
			#Connect two points
			line = MapElements.MapLine(point, points[(i+1)%self.sides_count], self.outside_line)
			lines.append(line)

		return lines

	def generate_inside_pivot_points(self, generation: int = 1):
		'''
		Function to generate pivot points inside polygon by specific generation
		Returns like list of tuples of points for lines: [(point1, point2), ...]
		'''

		#If this generations doesn't exists, return only coordinate system centers
		if generation == self.generation_count+1:
			return [tuple([BasicElements.Point(0, 0)]) for i in range(self.sides_count)]

		points = []
		for line in self.g_inside_lines[generation-1]:
			points.append(line.get_boundaries())

		return points

	def generate_inside_lines(self, generation: int = 1):
		'''
		Function to generate lines inside polygon by specific generation
		Returns like list of lines: [line1, ...]
		'''
		gen_lines = []

		#For all lines
		for line in self.g_outside_lines:
			#Get it's centers, and distance between line center and axis center
			center = line.get_central_point()
			distance = center.get_distance(BasicElements.Point(0, 0))

			#Calculate new distance using real inside_line distance, add some noise, and then calculate point scaling factor
			new_distance = distance - self.noise_distance(generation)*self.inside_line.distance
			factor = new_distance/distance

			#Then calculate half-length for inside line by generation with noising this distance factor
			halflength = self.inside_line.length/(2*self.noise_scale_length(generation))

			#Generate lines
			gen_line = line.get_parallel_line(center*factor, halflength, self.inside_line)
			gen_lines.append(gen_line)

		return gen_lines

	def generate_connecting_points(self, generation: int = 0):
		'''
		Function to generate connecting points on specific generation
		Returns list of tuples of points [(point1, point2), ...]
		If generation is lats, generates list of tuples of one point: [(point1), ...]
		'''

		#If generation == 0, it means that subdivide outside line
		lines = self.g_inside_lines[generation-1] if generation != 0 else self.g_outside_lines
		distance = self.connecting_line.distance + int(not bool(generation))*self.outside_circle.radius

		if generation != self.generation_count:
			#If it isn't last generation, then generate two points
			return [line.get_points_by_distance_on_line(distance) for line in lines]
		else:
			#If it's last generation then generate only central points
			return [tuple([line.get_central_point()]) for line in lines]

	def generate_connecting_lines(self, generation: int = 0):
		'''Function to generate connecting lines'''
		
		#Generate list of points
		outside_points = self.generate_connecting_points(generation)
		inside_points = self.generate_inside_pivot_points(generation+1)
		
		lines = []
		for i, v in enumerate(outside_points):
			for j, _ in enumerate(v):
				nearest = outside_points[i][j].get_nearest_point(inside_points[i])
				lines.append(MapElements.MapLine(outside_points[i][j], nearest, self.connecting_line))

		return lines

	def generate_outside_circles(self):
		'''Function to generate outside circles by pivot points'''
		circles = []
		points = self.generate_pivot_points()
		for point in points:
			circle = MapElements.MapCircle(point, self.outside_circle)
			circles.append(circle)

		return circles

	def generate_inside_circle(self):
		'''Function to generate inside circle in center of the coordinate system'''
		return MapElements.MapCircle(BasicElements.Point(0, 0), self.inside_circle)

	def generate(self):
		'''Function to combine all information in specific format to visualize'''

		outside_lines = self.g_outside_lines
		inside_lines = [line for lines in self.g_inside_lines for line in lines]
		connecting_lines = [line for lines in self.g_connecting_lines for line in lines]
		outside_circles = self.g_outside_circles
		inside_circles = [self.g_inside_circle]

		return MapInfo(outside_lines, inside_lines, connecting_lines, outside_circles, inside_circles)
