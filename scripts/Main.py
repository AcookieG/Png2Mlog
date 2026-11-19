from math import sqrt
from PIL import Image#, ImageShow

### Frames should be named frame1, frame2 ...
### please have widths and heights be divisible by your X,Y divisons :3

#Config
splitChannels=False
applyPalette=True
width, height=32, 18
XDivisions, YDivisions = 16, 1
frames=264
shavedFrames=0
jumpedFrames=0
filename="Miku"



#Def
def pixelToASCII(pixel):
	r=convertToASCII(pixel[0]); g=convertToASCII(pixel[1]); b=convertToASCII(pixel[2]);
	return r, g, b

def convertToASCII(color):
	colorUnicode=chr(round(color*colorRange+colorOffset))
	if colorUnicode==(34 or 39 or 92): colorUnicode+=1
	return colorUnicode

def matchToPal(pixel,pal):
	shortest=2**32
	pickedColor=0
	count=0
	r=pixel[0]; g=pixel[1]; b=pixel[2];
	for elem in pal:
		rPal=int(elem[0:2], 16); gPal=int(elem[2:4], 16); bPal=int(elem[4:6], 16);
		#distance=(r-rPal)**2+(g-gPal)**2+(b-bPal)**2
		if (r-rPal)**2+(g-gPal)**2+(b-bPal)**2<shortest:
			shortest=(r-rPal)**2+(g-gPal)**2+(b-bPal)**2
			pickedColor=alphabet[count]
		count+=1
	return pickedColor


#Init
colorRange=(126-32)/256
colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=allPixelBlock=""
alphabet="0123456789abcdefghijklmnopqrstuvwxyz"
pal=["d99d73","8c7fa9","ebeef5","b2c6d2","f7cba4","272727","8da1e3","f9a3c7","777777","53565c","cbd97f","f4ba6e","f3e979","7457ce","ff795e","ffaa5f","3a8f64","768a9a","e4ffd6","89769a","5e988d","df824d"]
items=[] #TODO add item ID in base36

if jumpedFrames<=1: jumpedFrames=1
images=["frame"+str(i*jumpedFrames+1)+".png" for i in range(0, (frames-shavedFrames)//jumpedFrames)]
frame=[None for i in range(0, (frames-shavedFrames)//jumpedFrames)]

if splitChannels: XDivisions=1; YDivisions=1;
blockWidth, blockHeight = int(width/XDivisions), int(height/YDivisions)

n=0
totalPixels=width*height*len(images)
PxPb=blockWidth*blockHeight*len(images)

if applyPalette: filename+="-"+str(PxPb)+"pxpb-"+str(YDivisions*XDivisions)+"blocks--palette"
elif splitChannels: filename+="-"+str(PxPb)+"pxpb-x3-"+str(YDivisions*XDivisions)+"blocks--RGB"
else: filename+="-"+str(PxPb*3)+"pxpb-"+str(YDivisions*XDivisions)+"blocks"
filename+=".txt"


#Main

print("Loading...")

#Load frames
for i in range(len(images)): 
	with Image.open(images[i]) as frame[i]:
		frame[i].load()
		frame[i]=frame[i].resize((width,height))

print("Loaded",str(len(images))+"/"+str(len(images)))


#Render Y -> X -> i -> y -> x -> pixel 
for Y in range(YDivisions):
	for X in range(XDivisions):
		for i in range(len(images)):
			for y in range(blockHeight):
				for x in range(blockWidth):
					pixel=tuple(frame[i].getpixel((x+X*blockWidth,y+Y*blockHeight))) #returns (r, g, b, a) with rgba<256.
					if applyPalette: allPixelBlock+=str(matchToPal(pixel,pal))
					elif splitChannels:
						pixelUnicode=pixelToASCII(pixel)
						allPixelR+=str(pixelUnicode[0]); allPixelG+=str(pixelUnicode[1]); allPixelB+=str(pixelUnicode[2]);
					else:
						pixelUnicode=pixelToASCII(pixel)
						allPixelBlock+=str(pixelUnicode[0])+str(pixelUnicode[1])+str(pixelUnicode[2]);
		#add and reset at every new block
		n+=PxPb
		allPixel+=allPixelBlock+"\n\n"
		allPixelBlock=""
		print(n,"/",totalPixels)


with open(filename, "w") as f:
	if splitChannels:
		f.write(allPixelR+"\n\n"+allPixelG+"\n\n"+allPixelB)
	else:
		f.write(allPixel)
print("All done!")
print("Saved under",filename)


