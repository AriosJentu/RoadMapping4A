import Abstracts
import BasicElements
import MapElements

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

import matplotlib.pyplot as plt

a, b = OutsideLine.get_xy_lists()
plt.plot(a, b)
plt.show()