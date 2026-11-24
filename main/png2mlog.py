#(By AcookieG / AKayoCookie, 2026)
# Frames should be named frame1, frame2 ...
# please have widths and heights be divisible by your X,Y divisons :3
# Please have divisions be a multiple of 2

from PIL import Image
from timeit import default_timer
import argparse
from pymsch import Block, Content, Schematic, ProcessorConfig, ProcessorLink

### --- Def ---

def pixelToASCII(pixel):
	r=convertToASCII(pixel[0]); g=convertToASCII(pixel[1]); b=convertToASCII(pixel[2]);
	return r, g, b

def convertToASCII(color):
	colorUnicode=round(color*colorRange+colorOffset)
	if colorUnicode==34 or colorUnicode==39 or colorUnicode==92: colorUnicode+=1
	return chr(colorUnicode)

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

def attention(issue, text):
	if issue:
		if str(input(f'''\033[38;2;255;144;12mWARNING!\033[0m
 | An issue with your parameters has been found: {text}
 | This may lead to a broken display.
 | Continue? (Y/n)''')).upper()=="Y": 0
		else: print(" | Parameters are being discarded."); return False
	return True

def attentionCheck():
	for elem in attentionList:
		if not elem:
			return False
	return True

def loadFrames(frames, frame):
	for i in range(frames):
		with Image.open(images[i]) as frame[i]:
			frame[i]=frame[i].resize((width,height))
		print(f" {slideBar(i/frames, 15, "--", "..")} {i} / {frames}", end="\r")
	return frame

def procPlacePaletteMode(X,Y, text):
	#ProcLinks, Proc position
	procLinks=[]
	procX, procY = X*blockWidth, YDivisions-Y*2-1
	if Y>=YDivisions//2: procY += -height
	for y in range(blockHeight):
		for x in range(blockWidth):
			procLinks.append(ProcessorLink(x,-y-Y*blockHeight-procY, f"sorter{x+y*blockWidth}"))
	procLinks.append(ProcessorLink(blockWidth, 0, "processor1"))

	#MLog
	codeConf=ProcessorConfig(f'''print "LINE {Y} COLUMN {X}"; set n 0; set li 0; set VAR "{text}"; sensor blockSize VAR @size; op sub array @links 1; read pixel VAR n; getlink link li; op add li li 1; op add n n 1; op sub pixel pixel 60; lookup item pixel pixel; control config link pixel 0 0 0; jump 6 lessThan li array; write STOP processor1 "STOP"; jump 18 equal STOP 1; set li 0; jump 6 lessThan n blockSize; write STOP processor1 "STOP"''', procLinks)

	schem.add_block(Block(Content.LOGIC_PROCESSOR, procX, procY, codeConf, 0))

def procPlaceCanvasMode(X,Y, text):
	#ProcLinks, Proc position
	procLinks=[]
	procX, procY = X*2-XDivisions, Y*2-YDivisions
	if X>=XDivisions//2: procX+=3
	procLinks.append(ProcessorLink(-procX,-procY, "display1"))

	#MLog
	codeConf=ProcessorConfig(f'''print "LINE {YDivisions-Y} COLUMN {X}"; set n 0; set VAR "{text}"; sensor blockSize VAR @size; set xmin {X*blockWidth}; set ymin {(YDivisions-Y)*blockHeight}; op add xmax xmin {blockWidth}; op add ymax ymin {blockHeight}; set x xmin; set y ymax; read R VAR n; op add n n 1; read G VAR n; op add n n 1; read B VAR n; op add n n 1; op add R R -32; op add G G -32; op add B B -32; op mul R R 2.7234; op mul G G 2.7234; op mul B B 2.7234; draw color R G B 255 0 0; draw rect x y -1 1 0 0; op add x x 1; jump 10 lessThan x xmax; drawflush display1; set x xmin; op sub y y 1; select y equal y ymin ymax y; jump 10 lessThan n blockSize''', procLinks)

	schem.add_block(Block(Content.LOGIC_PROCESSOR, procX, procY, codeConf, 0))

def procPlaceRGBMode(X,Y, R, G, B):
	#ProcLinks, Proc position
	procLinks=[]
	procX, procY = X*2-XDivisions, Y*2-YDivisions
	if X>=XDivisions//2: procX+=3
	procLinks.append(ProcessorLink(-procX,-procY, "display1"))

	#MLog
	codeConf=ProcessorConfig(f'''print "LINE {YDivisions-Y} COLUMN {X}"; set n 0; set Rp "{R}"; set Gp "{G}"; set Bp "{B}"; sensor blockSize Rp @size; set xmin {X*blockWidth}; set ymin {(YDivisions-Y)*blockHeight}; op add xmax xmin {blockWidth}; op add ymax ymin {blockHeight}; set x xmin; set y ymax; read R Rp n; read G Gp n; read B Bp n; op add n n 1; op add R R -32; op add G G -32; op add B B -32; op mul R R 2.7234; op mul G G 2.7234; op mul B B 2.7234; draw color R G B 255 0 0; draw rect x y -1 1 0 0; op add x x 1; jump 12 lessThan x xmax; drawflush display1; set x xmin; op sub y y 1; select y equal y ymin ymax y; jump 12 lessThan n blockSize''', procLinks)

	schem.add_block(Block(Content.LOGIC_PROCESSOR, procX, procY, codeConf, 0))

def snakeBar(percent, length): #Slow but cute
	bar=""
	progress=round(percent*length)
	for i in range(progress): bar+="~"
	if progress%4==0: bar+="C"
	else: bar+="c"
	for i in range(length-progress):
		if (i+progress)%4==0: bar+="¤"
		else: bar+=" "
	return f"[{bar}]"

def slideBar(percent, length, text, text2):
	bar=""
	progress=round(percent*length)
	for i in range(progress): bar+=text
	for i in range(length-progress): bar+=text2
	return f"[{bar}]"

### --- Init ---

#schem

schem = Schematic()
schem.set_tag('description', 'By [pink]A[salmon]K[orange]a[gold]y[yellow]oC[]o[]o[]k[]ie[]')
parser = argparse.ArgumentParser(prog="Png to MLog",description="Play mp4 videos in with Mindustry's processors")

#Parse

parser.add_argument("--xy", nargs=2, help="Width, Height. int int", dest="xy", default=(64,36), type=str)
parser.add_argument("--XY", nargs=2, help="Length-wise divisions, Cross-wise divisions. int int", dest="XY", default=(32,6), type=str)
parser.add_argument("-f", "--frames", nargs="?", help="Amount of frames. int", dest="frames", default=250, type=int)
parser.add_argument("-j", "--jump", nargs="?", help="Frame jump size. int", dest="jumpedFrames", default=1, type=int)

parser.add_argument("-o", "--output", "--filename", nargs="?", dest="filename", default="!name", type=str)
parser.add_argument("-c", "--channels", nargs="?", help="Do not split R, G and B color channels in three strings. bool", dest="splitChannels", default=True, type=bool)
parser.add_argument("-p", "--palette", nargs="?", help="Do not apply Mindustry's 22 sorter colors. bool", dest="applyPalette", default=True, type=bool)
parser.add_argument("-b", "--bottom", nargs="?", help="Have all the processors only at the bottom of the image. Ignore if the height is above 18. Only works if --palette is True. bool", dest="bottomProcs", default=False, type=bool)
parser.add_argument("-s", "--schematic", "--save", nargs="?", help="Save schematic as .schm file. bool", dest="save", default=False, type=bool)
parser.add_argument("-d", "--default", nargs="?", help="Use preset: 64x36, 32x6, 250, @1.  bool", type=bool)

parameters=parser.parse_args()
[width, height] = parameters.xy
[XDivisions, YDivisions] = parameters.XY
width, height, XDivisions, YDivisions = int(width), int(height), int(XDivisions), int(YDivisions)
frames, jumpedFrames = parameters.frames, parameters.jumpedFrames
filename, save = parameters.filename, parameters.save

if parameters.splitChannels != True: splitChannels = False
else: splitChannels = True
if parameters.applyPalette != True: applyPalette = False
else: applyPalette = True
if parameters.bottomProcs != False: bottomProcs = True
else: bottomProcs = False

if applyPalette: splitChannels=False


### --- Variables ---

#Color
colorRange=(126-32)/256; colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=allPixelBlock=""
pal=["d99d73","8c7fa9","ebeef5","b2c6d2","f7cba4","272727","8da1e3","f9a3c7","777777","53565c","cbd97f","f4ba6e","f3e979","7457ce","ff795e","ffaa5f","3a8f64","768a9a","e4ffd6","89769a"] #,"5e988d","df824d"

#Channels
blockWidth, blockHeight = int(width/XDivisions), int(height/YDivisions)

#Pixels and Frames
if jumpedFrames<=1: jumpedFrames=1
frames=frames//jumpedFrames
totalPixels=width*height*frames
PxPb=blockWidth*blockHeight*frames
n=0

#Warnings
attentionList=[
attention(height%2==1, "Odd height"),
attention(YDivisions%2==1, "Odd YDivisions"),
attention(XDivisions%2==1, "Odd XDivisions"),

attention(width/XDivisions%1 != 0, f"Block width of {width/XDivisions} tiles"),
attention(height/YDivisions%1 != 0, f"Block width of {height/YDivisions} tiles"),

attention(XDivisions==width, "Width / Xdivisions = 1"),
attention(bottomProcs and height>18, "Bottom and height>18"),
attention(PxPb>16000, "Memory cap exceeded (16Kib Uncompressed)")
]
execute=attentionCheck()
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
if splitChannels:
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
frame=loadFrames(frames, frame)
t2=default_timer()
print(f"Loaded {frames}/{frames}, {round(t2-t1, 2)}s                                               \n")

#applyPalette extras
if applyPalette:
	for x in range(width):
		for y in range(height):
			schem.add_block(Block(Content.SORTER, x, -y, None, 0)) #sorters
	for i in range(YDivisions):
		schem.add_block(Block(Content.ROUTER, width, i+1, None, 0))
		schem.add_block(Block(Content.ROUTER, width, -i-height, None, 0)) #routers

#Canvas extras
else:
	schem.add_block(Block(Content.LOGIC_DISPLAY, 1, 1, None, 0))
	schem.add_block(Block(Content.ROUTER, 0, -1, None, 0))
	schem.add_block(Block(Content.ROUTER, 1, -1, None, 0))
	schem.add_block(Block(Content.ROUTER, 2, -1, None, 0))
	schem.add_block(Block(Content.OVERDRIVE_DOME, 1, -3, None, 0))
	schem.add_block(Block(Content.POWER_SOURCE, 0, -5, None, 0))
	schem.add_block(Block(Content.ITEM_SOURCE, 1, -5, Content.SILICON, 0))
	schem.add_block(Block(Content.ITEM_SOURCE, 2, -5, Content.PHASE_FABRIC, 0))

#Loop
#Render X -> Y -> i -> y -> x -> pixel
for X in range(XDivisions):
	for Y in range(YDivisions):
		for i in range(frames):
			for y in range(blockHeight):
				for x in range(blockWidth):
					pixel=tuple(frame[i].getpixel((x+X*blockWidth,y+Y*blockHeight))) #returns (r, g, b, a) with rgba<256.
					if applyPalette: allPixelBlock+=matchToPal(pixel,pal)
					elif splitChannels:
						pixelUnicode=pixelToASCII(pixel)
						allPixelR+=pixelUnicode[0]; allPixelG+=pixelUnicode[1]; allPixelB+=pixelUnicode[2];
					else:
						pixelUnicode=pixelToASCII(pixel)
						allPixelBlock+=pixelUnicode[0]+pixelUnicode[1]+pixelUnicode[2];
		n+=PxPb
		t2=default_timer()
		print(f" {slideBar(n/totalPixels, 30, "|", ".")} {n} / {totalPixels} - {round(t2-t1, 2)}s", end="\r")

		#Add and reset at block
		allPixel+=allPixelBlock+"\n\n"

		#MLog Palette + Schematic
		if applyPalette: procPlacePaletteMode(X, Y, allPixelBlock)

		#Mlog
		elif not splitChannels: procPlaceCanvasMode(X, Y, allPixelBlock)

		#Mlog RGB
		else:
			procPlaceRGBMode(X, Y, allPixelR, allPixelG, allPixelB)
			allPixelR=allPixelG=allPixelB=""

		allPixelBlock=""

print(f"All done! - {round(t2-t1, 2)}s OwO                                               ")
if execute:

	#Load msch file
	with open(filename+".msch", "wb") as m:
		m.write(schem._write())
	schem.__init__()
	print(f"Schematic saved under",f"\033[38;2;144;164;255m{filename}.msch\033[0m")

	#Load txt file
	with open(filename+".txt", "w") as f: f.write(allPixel)
	print(f"Colors saved under",f"\033[38;2;144;164;255m{filename}.txt\033[0m")



