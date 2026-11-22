# Png2Mlog
 Converts an image or video to MLog using Python3.14.   
 
## How to use:

Convert your video to individual frames (I use ffmpeg)   
 `❯ ffmpeg -i ~/video.mp4 frame%d.png`   

Use your cli to execute the script   
 `❯ python /png2mlog.py`   

options:   
  | `command` | Description | Default |   
  | ----------------------------------------------- | ----------------------------------------------- | ------------ |   
  | `-h, --help` | show this help message and exit |  |   
  | `--xy [X Y]` | Width, Height. int int | `64 36` |   
  | `--XY [X Y]` | Length-wise divisions, Cross-wise divisions. int int | `32 6` |   
  | `-f, --frames [FRAMES]` | Amount of frames. int | `250` |   
  | `-j, --jump [JUMPEDFRAMES]` | Frame jump size. int | `1` |   
  | `-o, --output, --filename [FILENAME]` |  | `!name` |   
  | `-c, --channels [SPLITCHANNELS]` | Split R, G and B color channels in three strings. True if mentioned. | `False` |   
  | `-p, --palette [APPLYPALETTE]` | Apply Mindustry's 22 sorter colors. File will be saved in the x22 format. True if mentioned. | `True` |   
  | `-b, --bottom [BOTTOMPROCS]` | Have all the processors only at the bottom of the image. Ignore if the height is above 18. Only works if --palette is True. False if mentioned. | `False` |   
  | `-d, --default [DEFAULT]` | (Deprecated) Use preset: 64x36, 32x6, 250, @1, filename, --Palette. bool |  |   
 
## Dependencies:
Python 3.14 - https://www.python.org/downloads/release/python-31410/    
PIL - https://python-pillow.org/   
Argparse - https://github.com/python/cpython/blob/3.15/Lib/argparse.py   
pymsch - https://github.com/SkyeTheFoxyFox/pymsch https://pypi.org/project/pymsch/   
