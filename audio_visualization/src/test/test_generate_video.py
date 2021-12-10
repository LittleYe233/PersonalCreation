# -*- coding: utf-8 -*-


import os
import sys

from ..generate_video import generate


os.chdir(os.path.dirname(sys.argv[0]))
fp = open('out.log', 'a')
print()  # leave a blank line for output
generate('out.mp4', (1920, 1080), 60, 'h264', 2000, 5, '../../audio/in.wav',
         '../../images/in.jpg', fp, fp)
fp.close()