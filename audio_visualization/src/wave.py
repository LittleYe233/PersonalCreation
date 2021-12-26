# -*- coding: utf-8 -*-


import os
import sys

from .generate_video import generate


os.chdir(os.path.dirname(sys.argv[0]))
fp = open('../build/out.log', 'a')
print()  # leave a blank line for output
generate('../dist/out.mp4', (1920, 1080), 60, 'h264', 10000, 5,
         '../build/in.wav', 'aac', 'adelay=delays=6000:all=1',
         '../images/in.jpg', {'zh': 'in_zh.lrc', 'ja': 'in_ja.lrc'},
         fp, fp)
fp.close()
