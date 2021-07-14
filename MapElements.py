import Abstracts
import BasicElements

class MapLine(BasicElements.Line):
	'''
	MapLine - class to work with lines and line sectors in 2d space with parameters of the map
	Containing parameters: 
	- 'point1': first point in 2d space (order doesn't matter)
	- 'point2': second point in 2d space 
	- 'source': source abstract class of line types [AbstractMapLines]
	- 'linetype': type of the line
	Also independent parameters:
	- 'angle': angle in radians between line and horizontal axis
	- 'distance': distance between two points
	'''
	
	DEFAULTS = {
		"point1": BasicElements.Point(0, 0),
		"point2": BasicElements.Point(1, 1),
		"source": Abstracts.AbstractMapLines(),
		"linetype": "default",
	}
	POSSIBLE_LINETYPES = ["outside", "inside", "connecting", "default"]

	#Initializer
	def __init__(self, 
			point1: BasicElements.Point = DEFAULTS["point1"], 
			point2: BasicElements.Point = DEFAULTS["point2"],
			source: Abstracts.AbstractMapLines = DEFAULTS["source"],
			linetype: str = DEFAULTS["linetype"]
	):
		if linetype not in self.POSSIBLE_LINETYPES:
			linetype = self.DEFAULTS["linetype"]

		super().__init__(point1, point2)
		self.sourcetypes = source
		self.thickness = source.get_parameters_from_type(linetype).thickness
		self.linetype = linetype

	@staticmethod
	def from_angle_distance_point(
			angle: float, 
			distance: float, 
			point: BasicElements.Point = BasicElements.Point(0, 0),
			source: Abstracts.AbstractMapLines = DEFAULTS["source"],
			linetype: str = DEFAULTS["linetype"]
	):
		'''
		Generate line from one point, angle and distance:
		- 'angle' - angle in radians of oriented line (between 0 and PI)
		- 'distance' - distance between points (can be negative to orientate it in negative direction)
		- 'point' - first point in 2d space
		- 'source': source abstract class of line types [AbstractMapLines]
		- 'linetype': type of the line
		'''

		if not isinstance(point, BasicElements.Point):
			point = BasicElements.Point(0, 0)

		point2 = point.get_second_point_from_angle_distance(angle, distance)
		return MapLine(point, point2, source, linetype)

	#Other classic methods

	def __str__(self):
		return f"""MapLine:
		Point 1: \t{self.point1}, 
		Point 2: \t{self.point2},
		Distance: \t{self.distance},
		Angle:  \t{self.angle},
		Thickness: \t{self.thickness},
		Type:   \t{self.linetype}"""

	def __repr__(self):
		return f"MapLine[p1: {self.point1}, p2: {self.point2}, t: {self.linetype}]"


class MapCircle:
	
	DEFAULTS = {
		"point": BasicElements.Point(0, 0),
		"source": Abstracts.AbstractMapCircles(),
		"circletype": "default",
	}
	POSSIBLE_CIRCLETYPES = ["outside", "inside", "default"]

	#Initializer
	def __init__(self, 
		point: BasicElements.Point = DEFAULTS["point"],
		source: Abstracts.AbstractMapCircles = DEFAULTS["source"],
		circletype: str = DEFAULTS["circletype"]
	):
		if circletype not in self.POSSIBLE_CIRCLETYPES:
			circletype = self.DEFAULTS["circletype"]

		self.point = point
		self.radius = source.get_parameters_from_type(circletype).radius
		self.sourcetypes = source
		self.circletype = circletype

	#Other classic methods

	def __str__(self):
		return f"""MapCircle:
		Center: \t{self.point}, 
		Radius: \t{self.radius},
		Type:   \t{self.circletype}"""

	def __repr__(self):
		return f"MapCircle[c: {self.point}, r: {self.radius}, t: {self.circletype}]"

