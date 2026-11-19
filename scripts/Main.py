from math import sqrt
from PIL import Image

#TODO: more options, take multiple frames (should be easy, frames are recorded as frame1, frame2...)

#Config
splitChannels=False
applyPalette=True
width, height=128, 128
numberOfBlocksX, numberOfBlocksY = 4, 4
frames=1
shavedFrames=0
jumpedFrames=1

#Def
def pixelToASCII(pixel):
	r=convertToASCII(pixel[0]); g=convertToASCII(pixel[1]); b=convertToASCII(pixel[2]);
	return r, g, b

def convertToASCII(color):
	colorUnicode=chr(round(color*colorRange+colorOffset))
	if colorUnicode==(34 or 39 or 92): colorUnicode+=1
	return colorUnicode

def matchToPal(pixel,pal):
	best=2**32
	pickedColor=0
	count=0
	r=pixel[0]; g=pixel[1]; b=pixel[2];
	for elem in pal:
		rPal=int(elem[0:2], 16); gPal=int(elem[2:4], 16); bPal=int(elem[4:6], 16);
		distance=(r-rPal)**2+(g-gPal)**2+(b-bPal)**2
		if distance<best:
			best=distance
			pickedColor=alphabet[count]
		count+=1
	return pickedColor

#Init
colorRange=(126-32)/256
colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=""
alphabet="0123456789abcdefghijklmnopqrstuvwxyz"
pal=["d99d73","8c7fa9","ebeef5","b2c6d2","f7cba4","272727","8da1e3","f9a3c7","777777","53565c","cbd97f","f4ba6e","f3e979","7457ce","ff795e","ffaa5f","3a8f64","768a9a","e4ffd6","89769a","5e988d","df824d"]
items=[] #TODO add item ID in base36
if jumpedFrames<=1: jumpedFrames=1
images=["frame"+str(i*jumpedFrames+1)+".png" for i in range(0, frames-shavedFrames)]

#Main
if splitChannels: numberOfBlocksY=1; numberOfBlocksX=1;
blockWidth, blockHeight = int(width/numberOfBlocksX), int(height/numberOfBlocksY)

if applyPalette: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks--palette"
elif splitChannels: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-x3-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks--RGB"
else: filename="filename-"+str(blockWidth*blockHeight)+"pxpb-"+str(numberOfBlocksY*numberOfBlocksX)+"blocks"
filename+=".txt"

with Image.open(images[0]) as Image:
	Image.load()
	Image.resize((width,height))
	for Y in range(numberOfBlocksY):
		print("block column",Y,"/",numberOfBlocksY)
		for X in range(numberOfBlocksX):
			allPixelBlock=""
			for y in range(blockHeight):
				for x in range(blockWidth):
					pixel=tuple(Image.getpixel((x+X*blockWidth,y+Y*blockHeight))) #returns (r, g, b, a) with values between 0 and 256.
					if applyPalette: allPixelBlock+=matchToPal(pixel,pal)
					elif splitChannels:
						pixelUnicode=pixelToASCII(pixel)
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
