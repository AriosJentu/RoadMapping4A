import BasicElements

class Functions:

	@staticmethod
	def intersect_line_line(line1: BasicElements.Line, line2: BasicElements.Line):
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
	def intersect_line_circle(line: BasicElements.Line, circle: BasicElements.Circle):
		'''Function to get intersection points of the line and circle, or detect there is no intersection'''
		A1, B1, C1 = circle.get_equation().get_coefficients()
		A2, B2, C2 = line.get_equation().get_coefficients()

		#Solving system of (x, y): {x**2 + y**2 + A1x + B1y + C1 = 0, A2x + B2y + C2 = 0}

		#If line contains y value:
		if B2 != 0:
			#Isolate y
			yf = lambda x: (-C2 - A2*x)/B2

			#Generate the quadratic equation for x: Ax**2 + Bx + C = 0 from system of (x, y)
			A = A2**2 + B2**2
			B = B2**2 * A1 + 2*A2*C2 - A2*B2*B1
			C = C2**2 - B2*C2*B1 + B2**2 * C1

			D = B**2 - 4*A*C
			if D < 0 or A == 0:
				#If discriminant is negative, or line is not presented as function - there is no intersection
				return None

			if D == 0:
				x = -B/(2*A)
				y = yf(x)
				return [BasicElements.Point(x, y)]
			else:
				points = []
				rD = D**(1/2)
				for sign in [-1, 1]:
					x = (-B+sign*rD)/(2*A)
					y = yf(x)
					points.append(BasicElements.Point(x, y))

				return points
		else:
			#Isolate x
			x = -C2/A2
			#Get coefficitients for quadratic equation in terms of y
			A = 1
			B = B1
			C = C1 - A1*C2/A2 + C2**2 / A2**2

			D = B**2 - 4*A*C
			if D < 0:
				#If discriminant is negative, or line is not presented as function - there is no intersection
				return None

			if D == 0:
				y = -B/(2*A)
				return [BasicElements.Point(x, y)]

			else:
				points = []
				rD = D**(1/2)
				for sign in [-1, 1]:
					y = (-B+sign*rD)/(2*A)
					points.append(BasicElements.Point(x, y))

				return points

	@staticmethod
	def intersect_circle_circle(circle1: BasicElements.Circle, circle2: BasicElements.Circle):
		pass