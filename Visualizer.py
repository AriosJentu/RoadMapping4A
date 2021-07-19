from PIL import Image, ImageDraw

import BasicElements
import MapElements
import MapGenerator

class Visualizer:

	def __init__(self, map_info: MapGenerator.MapInfo, pixels_per_unit: float = 10, image_size: (int, int) = (2048, 2048)):
		self.map_info = map_info
		self.pixels_per_unit = pixels_per_unit
		self.image_size = image_size

	def draw_plot(self, filename: str):
		
		blank = Image.new("RGBA", self.image_size, (255,255,255,0))
		image = ImageDraw.Draw(blank)

		offset = BasicElements.Point(*self.image_size)/2

		updated_map_info = self.map_info.scale(-self.pixels_per_unit)	#Negative because image coordinate system is inverted in terms of real coordinate system for Y axis
		updated_map_info = updated_map_info.move(offset)

		for line in updated_map_info.get_lines():
			image.line(
				[point.int().get_coordinates() for point in line.get_boundaries()], 
				fill=(0, 0, 0, 255), 
				width=line.get_thickness()*self.pixels_per_unit
			)

		for circle in updated_map_info.get_circles():
			print(circle)
			circle.scale(self.pixels_per_unit)
			image.ellipse(
				[point.int().get_coordinates() for point in circle.get_boundary_box()], 
				fill=(0, 0, 0, 255), 
			)

		blank.save(filename, "PNG")


gen = MapGenerator.Generator(sides_count=3, generation_count=1).generate()
vis = Visualizer(gen)
vis.draw_plot("Hello world.png")