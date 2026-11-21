# Png2Mlog
 Converts an image or video to MLog using Python3.14.[eol]
 
## How to use:

Convert your video to individual frames (I use ffmpeg)[eol]
	`❯ ffmpeg -i ~/video.mp4 frame%d.png[eol]`

Use your cli to execute the script[eol]
	`❯ python /png2mlog.py[eol]`

options:[eol]
	`-h, --help`					 show this help message and exit[eol]
	`--xy [X Y]`					 Width, Height. int int[eol]
	`--XY [X Y]`					 Length-wise divisions, Cross-wise divisions. int int[eol]
	`-f, --frames [FRAMES]`			 Amount of frames. int[eol]
	`-j, --jump [JUMPEDFRAMES]`		 Frame jump size. int[eol]
	`-o, --output, --filename [FILENAME]`[eol]
	`-c, --channels [SPLITCHANNELS]	 Split R, G and B color channels in three strings. Boolean[eol]
	`-p, --palette [APPLYPALETTE]`	 apply Mindustry's 22 sorter colors. File will be saved in the x22 format. Boolean[eol]
	`-d, --default [DEFAULT]`		 (Deprecated) Use preset: 64x36, 32x6, 250, @1, filename, --Palette. Boolean[eol]
	
## Dependencies:
Python 3.14 - https://www.python.org/downloads/release/python-31410/ [eol]
PIL - https://python-pillow.org/[eol]
Argparse - https://github.com/python/cpython/blob/3.15/Lib/argparse.py[eol]
pymsch - https://github.com/SkyeTheFoxyFox/pymsch https://pypi.org/project/pymsch/[eol]
