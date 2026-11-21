# Png2Mlog
 Converts an image or video to MLog using Python3.14. \n
 
## How to use:

Convert your video to individual frames (I use ffmpeg) \n
	❯ ffmpeg -i ~/video.mp4 frame%d.png \n

Use your cli to execute the script \n
	❯ python /png2mlog.py \n

options: \n
	-h, --help						 show this help message and exit \n
	--xy XY XY						 Width, Height. int int \n
	--XY XY XY						 Length-wise divisions, Cross-wise divisions. int int \n
	-f, --frames [FRAMES]			 Amount of frames. int \n
	-j, --jump [JUMPEDFRAMES]		 Frame jump size. int \n
	-o, --output, --filename [FILENAME] \n
	-c, --channels [SPLITCHANNELS]	 Split R, G and B color channels in three strings. Boolean \n
	-p, --palette [APPLYPALETTE]	 apply Mindustry's 22 sorter colors. File will be saved in the x22 format. Boolean \n
	-d, --default [DEFAULT]			 (Deprecated) Use preset: 64x36, 32x6, 250, @1, filename, --Palette. Boolean \n
	
## Dependencies:
Python 3.14 - https://www.python.org/downloads/release/python-31410/  \n
PIL - https://python-pillow.org/ \n
Argparse - https://github.com/python/cpython/blob/3.15/Lib/argparse.py \n
pymsch - https://github.com/SkyeTheFoxyFox/pymsch https://pypi.org/project/pymsch/ \n
