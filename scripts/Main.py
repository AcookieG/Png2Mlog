from math import sqrt
from PIL import Image

#Def
def colorMatch(pixel):
	r=convert(int(pixel[0])); g=convert(int(pixel[1])); b=convert(int(pixel[2]));
	return r, g, b

def convert(colorHex):
	#TODO shorten
	if chr(round(colorHex/3+33))==(36 or 72): colorUnicode=chr(round(colorHex/3+33))
	else: colorUnicode=chr(round(colorHex/3+33))
	return colorUnicode

#Init
allPixels256=[]
allPixelR=allPixelG=allPixelB=""
width, height=128, 128
palette=[]
with Image.open("image.png") as Image:
	Image.load()
	Image.resize((width,height))
	frames=Image.n_frames;
	#Main
	for x in range(width):
		for y in range(height):
			pixel=tuple(Image.getpixel((x,y)))
			allPixels256.append(pixel)
			pixelUnicode=colorMatch(pixel)
			allPixelR+=str(pixelUnicode[0]); allPixelG+=str(pixelUnicode[1]); allPixelB+=str(pixelUnicode[2]);
	with open("filename.txt", "w") as f:
		f.write(allPixelR+"\n\n"+allPixelG+"\n\n"+allPixelB)


