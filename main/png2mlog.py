from PIL import Image
from timeit import default_timer
import argparse
from pymsch import Block, Content, Schematic, ProcessorConfig

### Frames should be named frame1, frame2 ...
### please have widths and heights be divisible by your X,Y divisons :3

schem=Schematic()
parser=argparse.ArgumentParser(prog="Png to MLog",description="Play mp4 videos in with Mindustry's processors")

#Parse

parser.add_argument("--xy", nargs=2, help="Width, Height. int int", dest="xy", default=(64,36), type=str)
parser.add_argument("--XY", nargs=2, help="Length-wise divisions, Cross-wise divisions. int int", dest="XY", default=(32,6), type=str)
parser.add_argument("-f", "--frames", nargs="?", help="Amount of frames. int", dest="frames", default=250, type=int)
parser.add_argument("-j", "--jump", nargs="?", help="Frame jump size. int", dest="jumpedFrames", default=1, type=int)

parser.add_argument("-o", "--output", "--filename", nargs="?", dest="filename", default="", type=str)
parser.add_argument("-c", "--channels", nargs="?", help="Split R, G and B color channels in three strings. Boolean", dest="splitChannels", default=False, type=bool)
parser.add_argument("-p", "--palette", nargs="?", help="Apply Mindustry's 22 sorter colors. File will be saved in the x22 format. Boolean", dest="applyPalette", default=True, type=bool)
parser.add_argument("-s", "--schematic", "--save", nargs="?", help="Save schematic as .schm file. Boolean", dest="save", default=False, type=bool)
parser.add_argument("-d", "--default", nargs="?", help="Use preset: 64x36, 32x6, 250, @1, , --Palette. Boolean", type=bool)

parameters=parser.parse_args()
[width, height]=parameters.xy
[XDivisions, YDivisions]=parameters.XY
width, height, XDivisions, YDivisions = int(width), int(height), int(XDivisions), int(YDivisions)
frames=parameters.frames
jumpedFrames=parameters.jumpedFrames
filename=parameters.filename
splitChannels=parameters.splitChannels
applyPalette=parameters.applyPalette
save=parameters.save
splitChannels, applyPalette, save = bool(splitChannels), bool(applyPalette), bool(save)
if splitChannels: channels=" --channels"
else: channels=""
if applyPalette: palette=" --palette"
else: palette=""
print(f" | selected parameters: {filename}: {width}x{height}, {XDivisions}x{YDivisions}, @{frames//jumpedFrames},{channels}{palette}")

#Config
"""
 if str(input(" | Use preset?\n(64x36, 32x6, 250, @1, filename, --Palette) (y/n) "))=="y":
	#preset
	width, height, XDivisions, YDivisions, frames, jumpedFrames, filename, splitChannels, applyPalette = 64, 36, 32, 6, 250, 1, "filename", False, True
else:
	#custom
	print(" | ")
	width, height, XDivisions, YDivisions=tuple(input(" | width, height, Length-wise divisions, cross-wise divisions: ").split(","))
	width, height, XDivisions, YDivisions=int(width), int(height), int(XDivisions), int(YDivisions)
	print(" | ")
	frames, jumpedFrames=tuple(input(" | frames, frame jump size: ").split(","))
	frames, jumpedFrames=int(frames), int(jumpedFrames)
	print(" | ")
	filename=str(input(" | filename: "))
	print(" | ")
	splitChannels=(str(input(" | Split channels?\n |     Will split R, G and B color channels in three strings. (y/n):"))=="y")
	print(" | ")
	applyPalette=(str(input(" | Apply Mindustry palette?\n |     Will apply Mindustry's 26 sorter colors. Output will be in base 22, in the same order as Vanilla. (y/n):"))=="y")
	print(" | ")
"""
print(" | Result will be saved in the same directory as frames. (Usually ~/home or the png2mlog.py directory)\n")


#Defwidth
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

def addProcessor(column, line, text):
	codeConf=ProcessorConfig(f'''set n 0
set li 0
set VAR "{text}"
sensor blockSize VAR @size
op sub array @links 1
read pixel VAR n
getlink link li
op add li li 1
op add n n 1
op sub pixel pixel 60
lookup item pixel pixel
control config link pixel 0 0 0
jump 5 lessThan li array
jump 36 equal STOP 1
write "STOP" processor1 STOP
set li 0
jump 5 lessThan n blockSize
end''', [])
	schem.add_block(Block(Content.LOGIC_PROCESSOR, column*2, line*2, codeConf, 0))

#Init
colorRange=(126-32)/256; colorOffset=32
allPixelsPercent=[]
allPixelR=allPixelG=allPixelB=allPixel=allPixelBlock=""
pal=["d99d73","8c7fa9","ebeef5","b2c6d2","f7cba4","272727","8da1e3","f9a3c7","777777","53565c","cbd97f","f4ba6e","f3e979","7457ce","ff795e","ffaa5f","3a8f64","768a9a","e4ffd6","89769a","5e988d","df824d"]

if jumpedFrames<=1: jumpedFrames=1
images=["frame"+str(i*jumpedFrames+1)+".png" for i in range(0, frames//jumpedFrames)]
frame=[None for i in range(0, frames//jumpedFrames)]

if splitChannels: XDivisions,YDivisions =1,1
blockWidth, blockHeight = int(width/XDivisions), int(height/YDivisions)

n=0
totalPixels=width*height*len(images)
PxPb=blockWidth*blockHeight*len(images)

if applyPalette: filename+=f"-{PxPb}pxpb-{YDivisions*XDivisions}blocks--palette"
elif splitChannels: filename+=f"-{PxPb}pxpb-x3-{YDivisions*XDivisions}blocks--RGB"
else: filename+=f"-{PxPb*3}pxpb-{YDivisions*XDivisions}blocks"

#Main
t1=default_timer()
print("Loading...")

#Load frames
for i in range(len(images)):
	with Image.open(images[i]) as frame[i]:
		frame[i].load()
		frame[i]=frame[i].resize((width,height))

t2=default_timer()
print(f"Loaded {len(images)}/{len(images)}, {round(t2-t1)}s\n")

#Load msch file
with open(filename+".3msch", "w") as m:

	#Render Y -> X -> i -> y -> x -> pixel
	for Y in range(YDivisions):
		schem.set_tag('name', str(Y+1))
		schem.set_tag('description', '')
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
			codeConf=ProcessorConfig(f'''set n 0
set li 0
set VAR "{allPixelBlock}"
sensor blockSize VAR @size
op sub array @links 1
read pixel VAR n
getlink link li
op add li li 1
op add n n 1
op sub pixel pixel 60
lookup item pixel pixel
control config link pixel 0 0 0
jump 5 lessThan li array
jump 36 equal STOP 1
write "STOP" processor1 STOP
set li 0
jump 5 lessThan n blockSize
end''', []) #MLog code block
			schem.add_block(Block(Content.LOGIC_PROCESSOR, X*2, Y*2, codeConf, 0))
			allPixelBlock=""
			t2=default_timer()
			print(f"{n} / {totalPixels} - {round(t2-t1)}s", end="\r")
		m.write(f"\n\n-----------------------------------------------\n====== BLOCK LINE {Y+1} ======\n-----------------------------------------------\n\n{schem.write_str()}") #Write 3 msch file
		schem.__init__()

#Load txt file
with open(filename+".txt", "w") as f:
	if splitChannels:
		f.write(allPixelR+"\n\n"+allPixelG+"\n\n"+allPixelB)
	else:
		f.write(allPixel)

print(f"All done! - {round(t2-t1)}s OwO       ")
print("Saved under",filename)

#Schem Code
code=f'''set n 0
set li 0
set VAR "{colorRange}"
sensor blockSize VAR @size
op sub array @links 1
read pixel VAR n
getlink link li
op add li li 1
op add n n 1
op sub pixel pixel 60
lookup item pixel pixel
control config link pixel 0 0 0
jump 5 lessThan li array
jump 36 equal STOP 1
write "STOP" processor1 STOP
set li 0
jump 5 lessThan n blockSize
end'''
