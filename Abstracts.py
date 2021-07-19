"""
Module for working with abstract lines and circles
Has it's individual custom length and thickness for lines, and radius for circles 
"""

class AbstractMapLineParameters:
	'''
	AbstractMapLineParameters - class for generating information about map line. 
	Containing parameters: 
	- 'thickness' of line (float)
	- 'length' of line (float)
	- 'distance' between lines (float)
	Comment:
	For 'outside' line there is only thickness and length
	For 'inside' line there is thickness, length, and distance from previous line (must be less than smallest distance to outside line)
	For 'central' line there is only thickness of the line
	For 'connecting' line there is thickness and distance (distance means separation from boundaries of previous line)
	'''

	#Initializer
	def __init__(self, thickness: float = 1, length: float = 1, distance: float = 1):
		self.thickness = thickness
		self.length = length
		self.distance = distance

	#Other classic methods
	
	def __str__(self):
		return f"AbstractMapLineParameters: Length - '{self.length}', Thickness - '{self.thickness}', Distance - '{self.distance}'"

	def __repr__(self):
		return f"AbstractMapLineParameters{{length={self.length}, thikness={self.thickness}, distance={self.distance}}}"


class AbstractMapLines:
	'''
	AbstractMapLines - class for generating information about lines on the map
	Contains parameters:
	- 'outside' line parameters (AbstractMapLineParameters)
	- 'inside' line parameters (AbstractMapLineParameters)
	- 'central' line parameters (AbstractMapLineParameters) [there is no length and distance]
	- 'connecting' line parameters (AbstractMapLineParameters) [there is no length]
	'''

	DEFAULTS = {
		"outside": AbstractMapLineParameters(3, 100, 0),
		"inside": AbstractMapLineParameters(2, 50, 10),
		"central": AbstractMapLineParameters(2, 0, 0),
		"connecting": AbstractMapLineParameters(2, 0, 15),
	}

	#Initializer
	def __init__(self, 
			outside: AbstractMapLineParameters = DEFAULTS["outside"], 
			inside: AbstractMapLineParameters = DEFAULTS["inside"], 
			central: AbstractMapLineParameters = DEFAULTS["central"], 
			connecting: AbstractMapLineParameters = DEFAULTS["connecting"]
	):
		self.outside = outside
		self.inside = inside
		self.central = central
		self.connecting = connecting
		self.types = {
			"outside": self.outside, 
			"inside": self.inside, 
			"central": self.central,
			"connecting": self.connecting,
			"default": self.connecting
		}

	#Getters

	def get_parameters_from_type(self, typename):
		'''Get line type parameters from typename, with default value as 'connecting' '''
		return self.types.get(typename, self.types["default"])

	#Other classic methods

	def __str__(self):
		return f"""AbstractMapLines: 
		Outside \t- {self.outside}
		Inside  \t- {self.inside}
		Central \t- {self.central}
		Connecting \t- {self.connecting}"""

	def __repr__(self):
		return f"AbstractMapLines[outside={self.outside}, inside={self.inside}, central={self.central}, connecting={self.connecting}]"


class AbstractMapCircleParameters:
	'''
	AbstractMapCircleParameters - class for generating information about map circle. 
	Containing parameters: 
	- 'radius' of the circle (float)
	'''

	#Initializer
	def __init__(self, radius: float = 3, thickness: float = -1):
		self.radius = radius
		self.thickness = thickness

	#Setters

	def set_radius(self, radius: float):
		self.radius = radius

	#Other classic methods

	def __str__(self):
		return f"AbstractMapCircleParameters: Radius - '{self.radius}', Thickness - '{self.thickness}'"

	def __repr__(self):
		return f"AbstractMapCircleParameters{{radius={self.radius}, thickness={self.thickness}}}"


class AbstractMapCircles:
	'''
	AbstractMapCircle - class for generating information about circles on the map
	Contains parameters:
	- 'outside' circle parameters (AbstractMapCircleParameters)
	- 'inside' circle parameters (AbstractMapCircleParameters)
	'''

	DEFAULTS = {
		"outside": AbstractMapCircleParameters(5),
		"inside": AbstractMapCircleParameters(6),
		"rings": AbstractMapCircleParameters(15, 2),
		"connecting": AbstractMapCircleParameters(2),
	}

	#Initializer
	def __init__(self, 
			outside: AbstractMapCircleParameters = DEFAULTS["outside"], 
			inside: AbstractMapCircleParameters = DEFAULTS["inside"], 
			rings: AbstractMapCircleParameters = DEFAULTS["rings"],
			connecting: AbstractMapCircleParameters = DEFAULTS["connecting"], 
	):
		self.outside = outside
		self.inside = inside
		self.rings = rings
		self.connecting = connecting
		self.types = {
			"outside": self.outside, 
			"inside": self.inside, 
			"rings": self.rings,
			"connecting": self.connecting, 
			"default": self.outside
		}

	#Getters

	def get_parameters_from_type(self, typename):
		'''Get circle type parameters from typename, with default value as 'connecting' '''
		return self.types.get(typename, self.types["default"])

	#Other classic methods

	def __str__(self):
		return f"""AbstractMapCircles: 
		Outside \t- {self.outside}
		Inside  \t- {self.inside}
		Rings   \t- {self.rings}
		Connecting\t- {self.connecting}"""

	def __repr__(self):
		return f"AbstractMapCircles[outside={self.outside}, inside={self.inside}, rings={self.rings}, connecting={self.connecting}]"