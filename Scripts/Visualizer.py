from PIL import Image, ImageDraw

from . import BasicElements
from . import MapElements
from . import MapGenerator

class Visualizer:

	def __init__(self, map_info: MapGenerator.MapInfo, pixels_per_unit: float = 10, image_size: (int, int) = (2048, 2048)):
		self.map_info = map_info
		self.pixels_per_unit = pixels_per_unit
		self.image_size = image_size

	def save_image(self, filename: str):
		
		blank = Image.new("RGBA", self.image_size, (255,255,255,0))
		image = ImageDraw.Draw(blank)

		offset = BasicElements.Point(*self.image_size)/2

		updated_map_info = self.map_info.scale(-self.pixels_per_unit)	#Negative because image coordinate system is inverted in terms of real coordinate system for Y axis
		updated_map_info = updated_map_info.move(offset)

		for circle in updated_map_info.get_circles():
			print(circle)
			circle.scale(self.pixels_per_unit)
			
			fill = (0, 0, 0, 255)
			outline = (0, 0, 0, 0)
			width = 0
			if circle.get_thickness() > 0:
				fill = (0, 0, 0, 0)
				outline = (0, 0, 0, 255)
				width = circle.get_thickness()*self.pixels_per_unit

			image.ellipse(
				[point.int().get_coordinates() for point in circle.get_boundary_box()], 
				fill=fill,
				outline=outline, 
				width=width
			)

		for line in updated_map_info.get_lines():
			image.line(
				[point.int().get_coordinates() for point in line.get_boundaries()], 
				fill=(0, 0, 0, 255), 
				width=line.get_thickness()*self.pixels_per_unit
			)

		blank.save(filename, "PNG")
		