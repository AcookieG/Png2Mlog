# Png2Mlog
 Converts an image or video to MLog using Python3.14.
 
## How to use:

Convert your video to individual frames (I use ffmpeg)
	❯ ffmpeg -i ~/video.mp4 frame%d.png

Use your cli to execute the script
	❯ python /png2mlog.py 

options:
	-h, --help						 show this help message and exit
	--xy XY XY						 Width, Height. int int
	--XY XY XY						 Length-wise divisions, Cross-wise divisions. int int
	-f, --frames [FRAMES]			 Amount of frames. int
	-j, --jump [JUMPEDFRAMES]		 Frame jump size. int
	-o, --output, --filename [FILENAME]
	-c, --channels [SPLITCHANNELS]	 Split R, G and B color channels in three strings. Boolean
	-p, --palette [APPLYPALETTE]	 apply Mindustry's 22 sorter colors. File will be saved in the x22 format. Boolean
	-d, --default [DEFAULT]			 (Deprecated) Use preset: 64x36, 32x6, 250, @1, filename, --Palette. Boolean
	
## Dependencies:
Python 3.14 - https://www.python.org/downloads/release/python-31410/ 
PIL - https://python-pillow.org/
Argparse - https://github.com/python/cpython/blob/3.15/Lib/argparse.py
pymsch - https://github.com/SkyeTheFoxyFox/pymsch https://pypi.org/project/pymsch/
