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
	'''

	#Initializer
	def __init__(self, thickness: float = 1, length: float = 1):
		self.thickness = thickness
		self.length = length

	#Other classic methods
	
	def __str__(self):
		return f"AbstractMapLineParameters: Length - '{self.length}', Thickness - '{self.thickness}'"

	def __repr__(self):
		return f"AbstractMapLineParameters{{length={self.length}, thikness={self.thickness}}}"


class AbstractMapLines:
	'''
	AbstractMapLines - class for generating information about lines on the map
	Contains parameters:
	- 'outside' line parameters (AbstractMapLineParameters)
	- 'inside' line parameters (AbstractMapLineParameters)
	- 'connecting' line parameters (AbstractMapLineParameters) [length for this line means section from outside line from boundaries]
	'''

	DEFAULTS = {
		"outside": AbstractMapLineParameters(1, 10),
		"inside": AbstractMapLineParameters(1, 5),
		"connecting": AbstractMapLineParameters(1, 2)
	}

	#Initializer
	def __init__(self, 
			outside: AbstractMapLineParameters = DEFAULTS["outside"], 
			inside: AbstractMapLineParameters = DEFAULTS["inside"], 
			connecting: AbstractMapLineParameters = DEFAULTS["connecting"]
	):
		self.outside = outside
		self.inside = inside
		self.connecting = connecting
		self.types = {
			"outside": self.outside, 
			"inside": self.inside, 
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
		Connecting \t- {self.connecting}"""

	def __repr__(self):
		return f"AbstractMapLines[outside={self.outside}, inside={self.inside}, connecting={self.connecting}]"


class AbstractMapCircleParameters:
	'''
	AbstractMapCircleParameters - class for generating information about map circle. 
	Containing parameters: 
	- 'radius' of the circle (float)
	'''

	#Initializer
	def __init__(self, radius: float = 3):
		self.radius = radius

	#Setters

	def set_radius(self, radius: float):
		self.radius = radius

	#Other classic methods

	def __str__(self):
		return f"AbstractMapCircleParameters: Radius - '{self.radius}'"

	def __repr__(self):
		return f"AbstractMapCircleParameters{{radius={self.radius}}}"


class AbstractMapCircles:
	'''
	AbstractMapCircle - class for generating information about circles on the map
	Contains parameters:
	- 'outside' circle parameters (AbstractMapCircleParameters)
	- 'inside' circle parameters (AbstractMapCircleParameters)
	'''

	DEFAULTS = {
		"outside": AbstractMapCircleParameters(2),
		"inside": AbstractMapCircleParameters(3),
	}

	#Initializer
	def __init__(self, 
			outside: AbstractMapCircleParameters = DEFAULTS["outside"], 
			inside: AbstractMapCircleParameters = DEFAULTS["inside"], 
	):
		self.outside = outside
		self.inside = inside
		self.types = {
			"outside": self.outside, 
			"inside": self.inside, 
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
		Inside  \t- {self.inside}"""

	def __repr__(self):
		return f"AbstractMapCircles[outside={self.outside}, inside={self.inside}]"