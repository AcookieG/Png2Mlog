#(By AcookieG / AKayoCookie, 2026)
# Frames should be named frame1, frame2 ...
# please have widths and heights be divisible by your X,Y divisons :3
# Please have divisions be a multiple of 2

from PIL import Image
from timeit import default_timer
import argparse
from pymsch import Block, Content, Schematic, ProcessorConfig, ProcessorLink

#schem init

schem = Schematic()
schem.set_tag('description', 'By [pink]A[salmon]K[orange]a[gold]y[yellow]oC[]o[]o[]k[]ie[]')
parser = argparse.ArgumentParser(prog="Png to MLog",description="Play mp4 videos in with Mindustry's processors")

#Parse init

parser.add_argument("--xy", nargs=2, help="Width, Height. int int", dest="xy", default=(64,36), type=str)
parser.add_argument("--XY", nargs=2, help="Length-wise divisions, Cross-wise divisions. int int", dest="XY", default=(32,6), type=str)
parser.add_argument("-f", "--frames", nargs="?", help="Amount of frames. int", dest="frames", default=250, type=int)
parser.add_argument("-j", "--jump", nargs="?", help="Frame jump size. int", dest="jumpedFrames", default=1, type=int)

parser.add_argument("-o", "--output", "--filename", nargs="?", dest="filename", default="!name", type=str)
parser.add_argument("-c", "--channels", nargs="?", help="Split R, G and B color channels in three strings. bool", dest="splitChannels", default=False, type=bool)
parser.add_argument("-p", "--palette", nargs="?", help="Apply Mindustry's 22 sorter colors. File will be saved in the x22 format. bool", dest="applyPalette", default=True, type=bool)
parser.add_argument("-b", "--bottom", nargs="?", help="Have all the processors only at the bottom of the image. Ignore if the height is above 18. Only works if --palette is True. bool", dest="bottomProcs", default=False, type=bool)
parser.add_argument("-s", "--schematic", "--save", nargs="?", help="Save schematic as .schm file. bool", dest="save", default=False, type=bool)
parser.add_argument("-d", "--default", nargs="?", help="Use preset: 64x36, 32x6, 250, @1, , --Palette. bool", type=bool)

parameters=parser.parse_args()
[width, height] = parameters.xy
[XDivisions, YDivisions] = parameters.XY
width, height, XDivisions, YDivisions = int(width), int(height), int(XDivisions), int(YDivisions)
frames, jumpedFrames = parameters.frames, parameters.jumpedFrames
filename, save = parameters.filename, parameters.save

if parameters.splitChannels != False: splitChannels = True
else: splitChannels = False
if parameters.applyPalette != True: applyPalette = False
else: applyPalette = True
if parameters.bottomProcs != False: bottomProcs = True
else: bottomProcs = False


#Config (Deprecated)
# if str(input(" | Use preset?\n(64x36, 32x6, 250, @1, filename, --Palette) (y/n) "))=="y":
#	#preset
#	width, height, XDivisions, YDivisions, frames, jumpedFrames, filename, splitChannels, applyPalette = 64, 36, 32, 6, 250, 1, "filename", False, True
#else:
#	#custom
#	width, height, XDivisions, YDivisions=tuple(input(" | width, height, Length-wise divisions, cross-wise divisions: ").split(","))
#	width, height, XDivisions, YDivisions=int(width), int(height), int(XDivisions), int(YDivisions)
#	frames, jumpedFrames=tuple(input(" | frames, frame jump size: ").split(","))
#	frames, jumpedFrames=int(frames), int(jumpedFrames)
#	filename=str(input(" | filename: "))
#	splitChannels=(str(input(" | Split channels?\n |     Will split R, G and B color channels in three strings. (y/n):"))=="y")
#	applyPalette=(str(input(" | Apply Mindustry palette?\n |     Will apply Mindustry's 26 sorter colors. Output will be in base 22, in the same order as Vanilla. (y/n):"))=="y")


### --- Def ---

def pixelToASCII(pixel):
	r=convertToASCII(pixel[0]); g=convertToASCII(pixel[1]); b=convertToASCII(pixel[2]);
	return r, g, b

def convertToASCII(color):
	colorUnicode=chr(round(color*colorRange+colorOffset))
	if colorUnicode==(34 or 39 or 92): colorUnicode+=1
	return colorUnicode

def matchToPal(pixel,pal):
	shortest=2**40
	pickedColor=0
	count=0
	r=pixel[0]; g=pixel[1]; b=pixel[2];
	for elem in pal:
		rPal=int(elem[0:2], 16); gPal=int(elem[2:4], 16); bPal=int(elem[4:6], 16);
		distance=(r-rPal)**2+(g-gPal)**2+(b-bPal)**2
		if distance<shortest:
			shortest=distance
			pickedColor=chr(count+60)
		count+=1
	return pickedColor

def attention(issue, execute, text):
	if issue and execute:
		if str(input(f'''\033[38;2;255;144;12mWARNING!\033[0m
 | An issue with your parameters has been found: {text}
 | This will lead to a broken display.
 | Continue? (Y/n)''')).upper()=="Y": 0
		else: execute=False; print(" | Parameters are being discarded.")
	return execute


### --- Variables ---

#Color
colorRange=(126-32)/256; colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=allPixelBlock=""
pal=["d99d73","8c7fa9","ebeef5","b2c6d2","f7cba4","272727","8da1e3","f9a3c7","777777","53565c","cbd97f","f4ba6e","f3e979","7457ce","ff795e","ffaa5f","3a8f64","768a9a","e4ffd6","89769a"] #,"5e988d","df824d"

#Channels
if splitChannels: XDivisions,YDivisions =1,1
blockWidth, blockHeight = int(width/XDivisions), int(height/YDivisions)

#Pixels and Frames
if jumpedFrames<=1: jumpedFrames=1
frames=frames//jumpedFrames
totalPixels=width*height*frames
PxPb=blockWidth*blockHeight*frames
n=0

#Warnings
execute=True
execute=attention(height%2==1, execute, "Odd height")
execute=attention(YDivisions%2==1, execute, "Odd YDivisions")
execute=attention(XDivisions%2==1, execute, "Odd XDivisions")
execute=attention(XDivisions==width, execute, "Width / Xdivisions = 1")
execute=attention(bottomProcs and height>18, execute, "Bottom and height>18")
execute=attention(PxPb*width*height>16000000, execute, "Memory cap exceeded (16Mib Uncompressed)")
if not execute: frames=0

#Images
images=["frame"+str(i*jumpedFrames+1)+".png" for i in range(0, frames)]
frame=[None for i in range(0, frames)]

#Filename
filenameTags=""
if applyPalette:
	palette=" --palette"
	filenameTags+="--palette"
else: palette="";
if splitChannels and not applyPalette:
	channels=" --channels"
	filenameTags+="--channels"
else: channels="";
if bottomProcs and palette:
	bottom=" --bottom"
	filenameTags+="--bottom"
else: bottom="";
schem.set_tag('name', filename)
print(f" |\n | selected parameters: {filename}: {width}x{height}, {XDivisions}x{YDivisions}, @{frames},{channels}{palette}{bottom}")
print(" | Results will be saved in the same directory as frames. (Usually \033[38;2;144;164;255m~/home\033[0m or the \033[38;2;144;164;255mpng2mlog.py\033[0m directory)\n")
filename+=f"-{PxPb}pxpb-{YDivisions*XDivisions}blocks{filenameTags}"

### --- Main ---

t1=default_timer()
print("Loading...")

#Load frames
for i in range(frames):
	with Image.open(images[i]) as frame[i]:
		frame[i].load()
		frame[i]=frame[i].resize((width,height))
t2=default_timer()
print(f"Loaded {frames}/{frames}, {round(t2-t1, 2)}s\n")

#Loop
for X in range(XDivisions):
	#Add sorters
	if applyPalette:
		for y in range(height):
			for x in range(blockWidth):
				schem.add_block(Block(Content.SORTER, x+2*X, -y+1, None, 0))

	#Render X -> Y -> i -> y -> x -> pixel
	for Y in range(YDivisions):
		for i in range(frames):
			for y in range(blockHeight):
				for x in range(blockWidth):
					pixel=tuple(frame[i].getpixel((x+X*blockWidth,y+Y*blockHeight))) #returns (r, g, b, a) with rgba<256.
					if applyPalette: allPixelBlock+=matchToPal(pixel,pal)
					elif splitChannels:
						pixelUnicode=pixelToASCII(pixel)
						allPixelR+=str(pixelUnicode[0]); allPixelG+=str(pixelUnicode[1]); allPixelB+=str(pixelUnicode[2]);
					else:
						pixelUnicode=pixelToASCII(pixel)
						allPixelBlock+=str(pixelUnicode[0])+str(pixelUnicode[1])+str(pixelUnicode[2]);
		n+=PxPb
		t2=default_timer()
		print(f"{n} / {totalPixels} - {round(t2-t1, 2)}s", end="\r")

		#Add and reset at block
		allPixel+=allPixelBlock+"\n\n"

		#MLog Palette + Schematic
		if applyPalette:

			#ProcLinks, Proc position
			procLinks=[]
			if Y<YDivisions//2:
				procX, procY = X*blockWidth, YDivisions-Y*2
				for y in range(blockHeight):
					for x in range(blockWidth):
						procLinks.append(ProcessorLink(x,-y-Y*blockHeight-procY+1, f"sorter{x+y*blockWidth+1}"))
			else:
				procX, procY = X*blockWidth, -height-Y*2+YDivisions
				for y in range(blockHeight):
					for x in range(blockWidth):
						procLinks.append(ProcessorLink(x,-y-Y*blockHeight+1+height+2*Y-YDivisions, f"sorter{x+y*blockWidth+1}"))
			procLinks.append(ProcessorLink(blockWidth, 0, "processor1"))

			#MLog
			codeConf=ProcessorConfig(f'''print "LINE {Y+1} COLUMN {X+1}"; set n 0; set li 0; set VAR "{allPixelBlock}"; sensor blockSize VAR @size; op sub array @links 1; read ascii VAR n; getlink link li; op add li li 1; op add n n 1; op sub itemID ascii 60; lookup item pixel itemID; control config link pixel 0 0 0; jump 6 lessThan li array; jump 17 equal STOP 1; set li 0; jump 6 lessThan n blockSize; write "STOP" processor1 STOP''', procLinks)

			schem.add_block(Block(Content.LOGIC_PROCESSOR, procX, procY, codeConf, 0))

		#Mlog RGB
		elif splitChannels: codeConf=""

		#Mlog Canvas
		else: splitChannels: codeConf=""

		allPixelBlock=""

for i in range(YDivisions):
	schem.add_block(Block(Content.ROUTER, width, i+2, None, 0))
	schem.add_block(Block(Content.ROUTER, width, -i+1-height, None, 0))

if execute:
	#f"\n\n-----------------------------------------------\n====== BLOCK COLUMN {X+1} ======\n-----------------------------------------------\n\n"
	with open(filename+".msch", "wb") as m:
		m.write(schem._write())
	schem.__init__()

	#Load txt file
	with open(filename+".txt", "w") as f:
		if splitChannels:
			f.write(allPixelR+"\n\n"+allPixelG+"\n\n"+allPixelB)
		else:
			f.write(allPixel)
	print(f"Colors saved under",f"\033[38;2;144;164;255m{filename}.txt\033[0m")

print(f"All done! - {round(t2-t1, 2)}s OwO       ")



