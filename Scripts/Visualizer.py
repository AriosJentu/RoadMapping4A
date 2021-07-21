from PIL import Image, ImageDraw, ImageFilter

from . import BasicElements
from . import MapElements
from . import MapGenerator

class Visualizer:

	def __init__(self, map_info: MapGenerator.MapInfo, pixels_per_unit: float = 10, image_size: (int, int) = (2048, 2048), blur_pixels: int = 0):
		self.map_info = map_info
		self.pixels_per_unit = pixels_per_unit
		self.image_size = image_size
		self.blur_pixels = blur_pixels

	def get_offset_map_info(self) -> MapGenerator.MapInfo:
		'''Function to get new map information with Image offsets'''
		offset = BasicElements.Point(*self.image_size)/2

		updated_map_info = self.map_info.scale(-self.pixels_per_unit)	#Negative because image coordinate system is inverted in terms of real coordinate system for Y axis
		updated_map_info = updated_map_info.move(offset)

		return updated_map_info

	def get_map_image(self) -> Image:
		'''Function to draw road map for this map info'''

		blank = Image.new("RGBA", self.image_size, (255,255,255,0))
		image = ImageDraw.Draw(blank)
	
		updated_map_info = self.get_offset_map_info()

		for circle in updated_map_info.get_circles():
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

		return blank

	def get_map_boundaries_image(self) -> Image:
		'''Function to draw boundaries of the image'''

		blank = Image.new("RGBA", self.image_size, (255, 255, 255, 0))
		image = ImageDraw.Draw(blank)

		updated_map_info = self.get_offset_map_info()

		image.polygon(
			[
				point.int().get_coordinates()
				for point in updated_map_info.get_boundaries()
			], fill=(255, 255, 255, 255)
		)

		return blank

	def apply_blur_to_image(self, image: Image) -> Image:
		'''Function to apply blur to image'''
		image = image.filter(ImageFilter.GaussianBlur(self.blur_pixels))
		return image

	def merge_layers(self, layers: list[Image]) -> Image:
		'''Function to merge layers containing images'''
		blank = Image.new("RGBA", self.image_size, (255, 255, 255, 0))
		for image in layers:
			blank = Image.alpha_composite(blank, image)

		return blank

	def save_image(self, filename: str):
		'''Function to save image to file'''
		blank = self.get_map_image()
		blank = self.apply_blur_to_image(blank)
		boundaries = self.get_map_boundaries_image()
		blank = self.merge_layers([boundaries, blank])

		blank.save(filename, "PNG")
		