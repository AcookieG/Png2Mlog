# Png2Mlog
 Converts an image or video to MLog using Python3.14.   
 
## How to use:

Convert your video to individual frames (I use ffmpeg)   
```bash
 ❯ ffmpeg -i ~/video.mp4 frame%d.png
```   

Use your cli to execute the script   
```bash
 ❯ python /png2mlog.py
```   

### options:   
  | `command` | Description | Default |   
  | ----------------------------------------------- | ----------------------------------------------- | ------------ |   
  | `-h, --help` | show this help message and exit |  |   
  | `--xy [X Y]` | Width, Height. `int int` | `64 36` |   
  | `--XY [X Y]` | Length-wise divisions, Cross-wise divisions. `int int` | `32 6` |   
  | `-f, --frames [FRAMES]` | Amount of frames. `int` | `250` |   
  | `-j, --jump [JUMPEDFRAMES]` | Frame jump size. `int` | `1` |   
  | `-o, --output, --filename [FILENAME]` | `str` | `!name` |   
  | `-c, --channels [SPLITCHANNELS]` | Split R, G and B color channels in three strings. A bit faster than standard. `False` if mentioned. | `True` |   
  | `-p, --palette [APPLYPALETTE]` | Apply Mindustry's 22 sorter colors. File will be saved in the x22 format. `False` if mentioned. | `True` |   
  | `-b, --bottom [BOTTOMPROCS]` | (WIP )Have all the processors only at the bottom of the image. Ignore if height is above 18. Only works if --palette is True. `False` if mentioned. | `False` |   
  | `-d, --default [DEFAULT]` | (Deprecated) Use preset: 64x36, 32x6, 250, @1, filename, --Palette. `bool` |  |   

### Example:
```bash
 ❯ python /png2mlog.py -b --xy 32 18 --XY 16 2
```
returns 
```
| selected parameters: !name: 32x18, 16x2, @250, --palette --bottom
Colors saved under !name-4500pxpb-32blocks--palette--bottom.txt
```
Accompanied by the text file `!name-4500pxpb-32blocks--palette--bottom.txt`   
and the schematic `!name-4500pxpb-32blocks--palette--bottom.msch` containing a 32x18 Sorter grid and 32 processors rendering 250 frames.  
## Dependencies:
Python 3.14 - https://www.python.org/downloads/release/python-31410/    
PIL - https://python-pillow.org/   
Argparse - https://github.com/python/cpython/blob/3.15/Lib/argparse.py   
pymsch - https://github.com/SkyeTheFoxyFox/pymsch https://pypi.org/project/pymsch/   
