import Scripts.Abstracts as Abstracts
import Scripts.BasicElements as BasicElements
import Scripts.MapElements as MapElements
import Scripts.MapGenerator as MapGenerator
import Scripts.Visualizer as Visualizer

def test_1():

	OutsideLines = Abstracts.AbstractMapLineParameters(thickness=3, length=10)
	InsideLines = Abstracts.AbstractMapLineParameters(thickness=2, length=5)
	ConnectingLines = Abstracts.AbstractMapLineParameters(thickness=1, length=2)

	OutsideCircles = Abstracts.AbstractMapCircleParameters(radius=4)
	InsideCircles = Abstracts.AbstractMapCircleParameters(radius=5)

	LinesInfo = Abstracts.AbstractMapLines(outside=OutsideLines, inside=InsideLines, connecting=ConnectingLines)
	CirclesInfo = Abstracts.AbstractMapCircles(outside=OutsideCircles, inside=InsideCircles)

	OutsideLine = MapElements.MapLine(
		BasicElements.Point(0, 0), 
		BasicElements.Point(1, 1),
		OutsideLines
	)

	InsideLine = MapElements.MapLine(
		BasicElements.Point(1, 0), 
		BasicElements.Point(2, 1),
		InsideLines
	)

	ConnectingLine = MapElements.MapLine(
		BasicElements.Point(2, 0), 
		BasicElements.Point(3, 1),
		ConnectingLines
	)

	OutsideCircle = MapElements.MapCircle(
		BasicElements.Point(0, 5),
		OutsideCircles
	)

	InsideCircle = MapElements.MapCircle(
		BasicElements.Point(5, 5),
		InsideCircles
	)

	print(LinesInfo)
	print(CirclesInfo)

	print(OutsideLine)
	print(InsideLine)
	print(ConnectingLine)
	print(OutsideCircle)
	print(InsideCircle)

def test_2():
	
	outside_line_thickness = 3 
	outside_line_length = 100
	
	inside_line_thickness = 2
	inside_line_length = 40
	inside_line_distance_from_previous = 10
	
	central_line_thickness = 2
	
	connecting_line_thickness = 2
	connecting_line_separation_distance = 20

	outside_circle_radius = 5
	inside_circle_radius = 6
	connecting_circle_radius = 2
	
	rings_radius = 15
	rings_thickness = 2

	sides_count = 3
	rings_count = 1
	generation_count = 1

	outside_line = Abstracts.AbstractMapLineParameters(outside_line_thickness, outside_line_length)
	inside_line = Abstracts.AbstractMapLineParameters(inside_line_thickness, inside_line_length, inside_line_distance_from_previous)
	central_line = Abstracts.AbstractMapLineParameters(central_line_thickness)
	connecting_line = Abstracts.AbstractMapLineParameters(connecting_line_thickness, 0, connecting_line_separation_distance)

	outside_circle = Abstracts.AbstractMapCircleParameters(outside_circle_radius)
	inside_circle = Abstracts.AbstractMapCircleParameters(inside_circle_radius)
	connecting_circle = Abstracts.AbstractMapCircleParameters(connecting_circle_radius)

	inside_rings = Abstracts.AbstractMapCircleParameters(rings_radius, rings_thickness)

	generated_map = MapGenerator.Generator(
		outside_line=outside_line,
		inside_line=inside_line,
		central_line=central_line,
		connecting_line=connecting_line,
		outside_circle=outside_circle,
		inside_circle=inside_circle,
		inside_rings=inside_rings,
		connecting_circle=connecting_circle,
		sides_count=sides_count,
		rings_count=rings_count,
		generation_count=generation_count
	).generate()
	visualizer = Visualizer.Visualizer(generated_map)
	visualizer.save_image("Hello world.png")

test_2()