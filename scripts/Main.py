from math import sqrt
from PIL import Image

#Def
def colorMatch(pixel):
	r=pixel[0]; g=pixel[1]; b=pixel[2]
	rU, gU, bU=convert(r), convert(g), conver(b)
	return rU, gU, bU

def convert(colorHex):
	#TODO shorten
	if ord(int(colorHex)/10+33)==(36 or 72): colorUnicode=ord(int(colorHex)/10+34)
	else: colorUnicode=ord(int(colorHex)/10+33)
	return colorUnicode

#Init
allPixels256=[]
allPixelTuples=[]
palette=[]
with Image.open("image.png") as Image:
	Image.load()
	imageWidth=Image.width; imageHeight=Image.height; frames=Image.n_frames
	#Main
	for x in range(imageWidth):
		for y in range(imageHeight):
			pixel=str(Image.getpixel((x,y)))
			allPixels256.append(pixel)
			allPixelTuples.append(colorMatch(pixel))


