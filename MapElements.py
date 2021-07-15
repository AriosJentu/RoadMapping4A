import Abstracts
import BasicElements

class MapLine(BasicElements.Line):
	'''
	MapLine - class to work with lines and line sectors in 2d space with parameters of the map
	Containing parameters: 
	- 'point1': first point in 2d space (order doesn't matter)
	- 'point2': second point in 2d space 
	- 'lineclass': abstract class of the map line [AbstractMapLineParameters]
	Also independent parameters:
	- 'angle': angle in radians between line and horizontal axis
	- 'distance': distance between two points
	'''
	
	DEFAULTS = {
		"point1": BasicElements.Point(0, 0),
		"point2": BasicElements.Point(1, 1),
		"lineclass": Abstracts.AbstractMapLineParameters(),
	}

	#Initializer
	def __init__(self, 
			point1: BasicElements.Point = DEFAULTS["point1"], 
			point2: BasicElements.Point = DEFAULTS["point2"],
			lineclass: Abstracts.AbstractMapLineParameters = DEFAULTS["lineclass"]
	):

		super().__init__(point1, point2)
		self.lineclass = lineclass

	@staticmethod
	def from_angle_distance_point(
			angle: float, 
			distance: float, 
			point: BasicElements.Point = BasicElements.Point(0, 0),
			lineclass: Abstracts.AbstractMapLineParameters = DEFAULTS["lineclass"]
	):
		'''
		Generate line from one point, angle and distance:
		- 'angle' - angle in radians of oriented line (between 0 and PI)
		- 'distance' - distance between points (can be negative to orientate it in negative direction)
		- 'point' - first point in 2d space
		- 'lineclass': class of the line [AbstractMapLineParameters]
		'''

		if not isinstance(point, BasicElements.Point):
			point = BasicElements.Point(0, 0)

		point2 = point.get_second_point_from_angle_distance(angle, distance)
		return MapLine(point, point2, lineclass)

	#Getters

	def get_thickness(self):
		return self.lineclass.thickness

	def get_length(self):
		return self.lineclass.length

	#Other classic methods

	def __str__(self):
		return f"""MapLine:
		Point 1: \t{self.point1}, 
		Point 2: \t{self.point2},
		Distance: \t{self.distance},
		Angle:  \t{self.angle},
		Class:  \t{self.lineclass}"""

	def __repr__(self):
		return f"MapLine[p1: {self.point1}, p2: {self.point2}, cls: {self.lineclass}]"


class MapCircle(BasicElements.Circle):
	'''
	MapCircle - class to work with circles in 2d space with parameters of the map
	Containing parameters: 
	- 'center': central point of circle in 2d space
	- 'circleclass': abstract class of the map circle [AbstractMapCircleParameters]
	'''
	
	DEFAULTS = {
		"center": BasicElements.Point(0, 0),
		"circleclass": Abstracts.AbstractMapCircleParameters(),
	}

	#Initializer
	def __init__(self, 
		center: BasicElements.Point = DEFAULTS["center"],
		circleclass: Abstracts.AbstractMapCircleParameters = DEFAULTS["circleclass"]
	):

		super().__init__(center, circleclass.radius)
		self.circleclass = circleclass

	#Other classic methods

	def __str__(self):
		return f"""MapCircle:
		Center: \t{self.center}, 
		Radius: \t{self.radius}, 
		Class:  \t{self.circleclass}"""

	def __repr__(self):
		return f"MapCircle[c: {self.point}, r: {self.radius}, cls: {self.circleclass}]"

