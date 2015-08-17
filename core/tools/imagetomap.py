image_path = "../../westeros.tif"
mod_name= "westeros"
map_name = "westeros_full"

WATER = (0, 138, 255)
GRASS = (0, 198, 16)
FOREST = (16, 138, 25)
MOUNTAINS = (123, 125, 123)
DIRT = (165, 125, 82)

from PIL import Image

image = Image.open(image_path)
width = image.size[0]
height = image.size[1]

lines = []

pix = image.load()

# load colors to lines
for iy in range(0, height -1):
	linestr = "\""
	for ix in range(0, width -1):
		color = pix[ix, iy]
		lds = "W"
		if color == GRASS:
			lds = "G"
		elif color == FOREST:
			lds = "F"
		elif color == MOUNTAINS:
			lds = "M"
		elif color == DIRT:
			lds = "D"
		linestr += lds
	linestr += "\","
	lines.append(linestr)

mapfile = open("../../mods/" + mod_name + "/maps/" + map_name + ".json", "w")
for line in lines:
	mapfile.write(line + "\n")
mapfile.close()