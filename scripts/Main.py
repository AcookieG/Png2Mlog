from math import sqrt
from PIL import Image

#TODO: more options, convert to base36, split channels, take multiple frames (should be easy, frames are recorded as frame1, frame2...)

#config
splitChannels=False
applyPalette=False
width, height=128, 128
numberOfBlocksX, numberOfBlocksY = 4, 4

#Def
def pixelPercentToASCII(pixel):
	r=convertToASCII(int(pixel[0])); g=convertToASCII(int(pixel[1])); b=convertToASCII(int(pixel[2]));
	return r, g, b

def convertToASCII(colorPercent):
	#TODO shorten
	colorUnicode=chr(round(colorPercent/colorRange+colorOffset))
	if colorUnicode==(34 or 39 or 92): colorUnicode+=1
	return colorUnicode

def matchToPal(pixel,pal):
	#TODO convert to base36
	best=2**32
	pickedColor="000000"
	for elem in pal:
		r=pixel[0]; g=pixel[1]; b=pixel[2];
		rPal=elem[0]; gPal=elem[1]; bPal=elem[2];
		distance=(r-rPal)**2+(g-gPal)**2+(b-bPal)**2
		if distance<best: best=distance, pickedColor=str(r)+str(g)+str(b)
	return pickedColor

#Init
colorRange=(126-32)/100
colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=""
pal=[]

#main
if splitChannels: numberOfBlocksY=1; numberOfBlocksX=1;
blockWidth, blockHeight = int(width/numberOfBlocksX), int(height/numberOfBlocksY)

if applyPalette: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks--palette"
elif splitChannels: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-x3-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks--RGB"
else: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks"
filename+=".txt"

with Image.open("image.png") as Image:
	Image.load()
	Image.resize((width,height))
	frames=Image.n_frames
	for Y in range(numberOfBlocksY):
		for X in range(numberOfBlocksX):
			print("block",X+numberOfBlocksX*Y,"/",numberOfBlocksY*numberOfBlocksX)
			allPixelBlock=""
			for y in range(blockHeight):
				for x in range(blockWidth):
					pixel=tuple(Image.getpixel((x+X*blockWidth,y+Y*blockHeight)))
					if applyPalette: a=1
					elif splitChannels:
						pixelUnicode=pixelPercentToASCII(pixel)
						allPixelR+=str(pixelUnicode[0]); allPixelG+=str(pixelUnicode[1]); allPixelB+=str(pixelUnicode[2]);
					else:
						pixelUnicode=pixelPercentToASCII(pixel)
						allPixelBlock+=str(pixelUnicode[0])+str(pixelUnicode[1])+str(pixelUnicode[2]);
			allPixel+=allPixelBlock+"\n\n"
	with open(filename, "w") as f:
			if splitChannels:
				f.write(allPixelR+"\n\n"+allPixelG+"\n\n"+allPixelB)
			else:
				f.write(allPixel)
	print("All done!")
	print("Saved under",filename)
