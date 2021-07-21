import math

from . import Abstracts
from . import BasicElements
from . import MapElements
from . import Functions

class MapInfo:
	'''
	MapInfo - class with generated information about specific map 2d space
	Containing parameters: 
	- 'outside_lines': list of outside lines List[MapElements.MapLine]
	- 'inside_lines': list of inside lines List[MapElements.MapLine]
	- 'central_lines': list of cenral lines List[MapElements.MapLine] connecing center and sides of the figure
	- 'connecting_lines': list of connecting lines List[MapElements.MapLine]
	- 'outside_circles': list of outside circles List[MapElements.MapCircle]
	- 'inside_circles': list of inside circles List[MapElements.MapCircle]
	- 'inside_rings': list of inside rings List[MapElements.MapCircle]
	- 'connecting_circles': list of connecting circles List[MapElements.MapCircle]
	'''
	def __init__(self,
			outside_lines: list[MapElements.MapLine],
			inside_lines: list[MapElements.MapLine],
			central_lines: list[MapElements.MapLine],
			connecting_lines: list[MapElements.MapLine],
			sector_lines: list[MapElements.MapLine],
			outside_circles: list[MapElements.MapCircle],
			inside_rings: list[MapElements.MapCircle],
			inside_circles: list[MapElements.MapCircle],
			connecting_circles: list[MapElements.MapCircle],
	):
		self.outside_lines = outside_lines
		self.inside_lines = inside_lines
		self.central_lines = central_lines
		self.connecting_lines = connecting_lines
		self.sector_lines = sector_lines
		self.outside_circles = outside_circles
		self.inside_rings = inside_rings
		self.inside_circles = inside_circles
		self.connecting_circles = connecting_circles

		self.lines = [
			self.outside_lines, 
			self.inside_lines, 
			self.central_lines,
			self.connecting_lines,
			self.sector_lines,
		]

		self.circles = [
			self.outside_circles, 
			self.inside_rings,
			self.inside_circles,
			self.connecting_circles,
		]

		self.objects_lists = self.lines+self.circles

	def move(self, offset: BasicElements.Point):
		'''Function to generate updated MapInfo with moving all elements to the specific offset'''
		
		objects_lists = []
		
		for objects in self.objects_lists:
			element_lists = []
		
			for element in objects:
				new_element = element+offset
				element_lists.append(new_element)

			objects_lists.append(element_lists)

		return MapInfo(*objects_lists)

	def scale(self, factor: float = 1):
		'''Function to generate updated MapInfo with scaling all elements to the specific factor'''
		
		objects_lists = []
		
		for objects in self.objects_lists:
			element_lists = []

			for element in objects:
				new_element = element*factor
				element_lists.append(new_element)

			objects_lists.append(element_lists)

		return MapInfo(*objects_lists)

	def get_lines(self):
		'''Function which returns iterator of all available lines'''
		for lines in self.lines:
			for line in lines:
				yield line

	def get_circles(self):
		'''Function which returns iterator of all available circles'''
		for circles in self.circles:
			for circle in circles:
				yield circle

	def get_boundaries(self):
		'''Function to get boundary points of the map'''
		points = []
		for circle in self.outside_circles:
			points.append(circle.center)

		return points

class Generator:
	'''
	Generator - class to generate specific map in 2d space
	Containing parameters: 
	- 'outside_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'inside_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'connecting_line' parameters [Abstracts.AbstractMapLineParameters]
	- 'outside_circle' parameters [Abstracts.AbstractMapCircleParameters]
	- 'inside_circle' parameters [Abstracts.AbstractMapCircleParameters]
	- 'inside_rings' parameters [Abstracts.AbstractMapCircleParameters]
	- 'connecting_circle' parameters [Abstracts.AbstractMapCircleParameters]
	- 'sides_count': count of the map sides
	- 'generation_count: count of generations of inside lines
	- 'noise_distance': function of one integer variable, which generates noise for distance between points
	- 'noise_scale_length': function of one integer variable, which generates noise for scaling factor of generations
	This class generates map with equilateral sides polygon
	'''

	def __init__(self,
			outside_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["outside"],
			inside_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["inside"],
			central_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["central"],
			connecting_line: Abstracts.AbstractMapLineParameters = Abstracts.AbstractMapLines.DEFAULTS["connecting"],
			outside_circle: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["outside"],
			inside_circle: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["inside"],
			inside_rings: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["rings"],
			connecting_circle: Abstracts.AbstractMapCircleParameters = Abstracts.AbstractMapCircles.DEFAULTS["connecting"],
			sides_count: int = 3,
			rings_count: int = 0,
			sector_subdivisions: int = 0,
			generation_count: int = 1,
			noise_distance=lambda n: n,
			noise_scale_length=lambda n: n,
	):
		self.outside_line = outside_line
		self.inside_line = inside_line
		self.central_line = central_line
		self.connecting_line = connecting_line

		self.outside_circle = outside_circle
		self.inside_circle = inside_circle
		self.inside_rings = inside_rings
		self.connecting_circle = connecting_circle

		self.sides_count = max(int(sides_count), 3)
		self.rings_count = max(int(rings_count), 0)
		self.sector_subdivisions = max(int(sector_subdivisions), 0)
		self.generation_count = max(int(generation_count), 1)

		self.noise_distance = noise_distance
		self.noise_scale_length = noise_scale_length

		#Generation
		self.g_outside_lines = self.generate_outside_lines()
		self.g_inside_lines = [self.generate_inside_lines(i+1) for i in range(self.generation_count)]
		self.g_central_lines = self.generate_central_lines()
		self.g_connecting_lines = [self.generate_connecting_lines(i) for i in range(self.generation_count+1)]
		self.g_sector_lines = [self.generate_sector_lines(i) for i in range(self.generation_count)]
		self.g_outside_circles = self.generate_outside_circles()
		self.g_inside_circle = self.generate_inside_circle()
		self.g_inside_rings = [self.generate_inside_ring(i+1) for i in range(self.rings_count)]
		self.g_connecting_circles = [self.generate_connecting_circles(i) for i in range(1, self.generation_count+1)]

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

	def generate_central_lines(self):
		'''Function to generate central connecting lines by pivot points'''
		lines = []
		points = self.generate_pivot_points()
		
		for i, point in enumerate(points):
			#Connect two points
			line = MapElements.MapLine(point, BasicElements.Point(0, 0), self.central_line)
			lines.append(line)

		return lines

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
		for list_index, outside_pair in enumerate(outside_points):
			
			if len(outside_pair) > 1:
				
				outside_line = BasicElements.Line(*outside_pair)
				inside_line = BasicElements.Line(*inside_points[list_index])
				
				if not outside_line.is_lines_in_one_direction(inside_line):
					inside_line.reverse_direction()

				for index, point in enumerate(outside_line.get_boundaries()):
					lines.append(MapElements.MapLine(point, inside_line.get_boundaries()[index], self.connecting_line))

			else:
				outside_point = outside_pair[0]
				inside_point = inside_points[list_index][0]
				lines.append(MapElements.MapLine(outside_point, inside_point, self.connecting_line))

		return lines

	def generate_sector_lines(self, generation: int = 0):
		'''Function to generate sector lines. Generation must be less than possible count of generations'''
		outside_points = self.generate_connecting_points(generation)
		inside_points = self.generate_inside_pivot_points(generation+1)

		outside_lines = []
		inside_lines = []

		for i in range(len(outside_points)):
			outside_lines.append(BasicElements.Line(*outside_points[i]))
			inside_lines.append(BasicElements.Line(*inside_points[i]))

		outside_sector_points = []
		inside_sector_points = []
	
		for line in outside_lines:
			outside_sector_points.append(line.get_subdivision_points(self.sector_subdivisions))

		for line in inside_lines:
			inside_sector_points.append(line.get_subdivision_points(self.sector_subdivisions))

		lines = []
		for points_list_index in range(len(outside_sector_points)):

			outside_points_list = outside_sector_points[points_list_index]
			inside_points_list = inside_sector_points[points_list_index]

			if len(outside_points_list) > 1:
				outside_line = BasicElements.Line(outside_points_list[0], outside_points_list[-1])
				inside_line = BasicElements.Line(inside_points_list[0], inside_points_list[-1])
				
				if not outside_line.is_lines_in_one_direction(inside_line):
					inside_points_list = inside_points_list[::-1]

			for index, point in enumerate(outside_points_list):
				lines.append(MapElements.MapLine(point, inside_points_list[index], self.connecting_line))

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

	def generate_inside_ring(self, generation: int = 1):
		'''Function to generate ring inside map with generation parameters'''
		circle = MapElements.MapCircle(BasicElements.Point(0, 0), self.inside_rings, True)
		circle.scale(self.noise_scale_length(generation))
		return circle

	def generate_connecting_circles(self, generation: int = 1):
		'''Function to generate connecting circles'''
		boundary_points = self.generate_inside_pivot_points(generation)

		circles = []
		for _, list_boundary_points in enumerate(boundary_points):
			for point in list_boundary_points:
				circle = MapElements.MapCircle(point, self.connecting_circle)
				circles.append(circle)

		return circles

	def generate(self):
		'''Function to combine all information in specific format to visualize'''

		outside_lines = self.g_outside_lines
		inside_lines = [line for lines in self.g_inside_lines for line in lines]
		central_lines = self.g_central_lines
		connecting_lines = [line for lines in self.g_connecting_lines for line in lines]
		sector_lines = [line for lines in self.g_sector_lines for line in lines]
		outside_circles = self.g_outside_circles
		inside_rings = self.g_inside_rings[::-1]
		inside_circles = [self.g_inside_circle]
		connecting_circles = [circle for circles in self.g_connecting_circles for circle in circles]

		return MapInfo(outside_lines, inside_lines, central_lines, connecting_lines, sector_lines, outside_circles, inside_rings, inside_circles, connecting_circles)
