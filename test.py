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
	LinesInfo,
	"outside"
)

InsideLine = MapElements.MapLine(
	BasicElements.Point(1, 0), 
	BasicElements.Point(2, 1),
	LinesInfo,
	"inside"
)

ConnectingLine = MapElements.MapLine(
	BasicElements.Point(2, 0), 
	BasicElements.Point(3, 1),
	LinesInfo,
	"connecting"
)

OutsideCircle = MapElements.MapCircle(
	BasicElements.Point(0, 5),
	CirclesInfo,
	"outside"
)

InsideCircle = MapElements.MapCircle(
	BasicElements.Point(5, 5),
	CirclesInfo,
	"inside"
)

print(OutsideLine)
print(InsideLine)
print(ConnectingLine)
print(OutsideCircle)
print(InsideCircle)