import BasicElements
import MapElements

class Functions:

	@staticmethod
	def intersect_line_line(line1: MapElements.MapLine, line2: MapElements.MapLine):
		'''Function to get intersection point of the lines, or detect there is no intersection, or say they are equal'''
		A1, B1, C1 = line1.get_equation().get_coefficients()
		A2, B2, C2 = line2.get_equation().get_coefficients()

		if A1 == A2 and B1 == B2 and C1 == C2:
			#If coefficients are equal, then this lines are the same
			return True

		#Solving system of linear equations with 2 variables (x, y): {eq1 = 0; eq2 = 0}
		#Find the determinant:
		det = A1*B2 - B1*A2

		if det == 0:
			#If determinant is zero, then lines are parallel
			return None

		#By the matrix product, got next formulas:
		x = (C2*B1 - C1*B2)/det
		y = (C1*A2 - C2*A1)/det

		return BasicElements.Point(x, y)

	@staticmethod
	def intersect_line_circle(line: MapElements.MapLine, circle: MapElements.MapCircle):
		pass

	@staticmethod
	def intersect_circle_circle(circle1: MapElements.MapCircle, circle2: MapElements.MapCircle):
		pass
