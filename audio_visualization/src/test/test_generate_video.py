# -*- coding: utf-8 -*-


import os
import sys

from ..generate_video import generate


os.chdir(os.path.dirname(sys.argv[0]))
generate('out.mp4', (1920, 1080), 60, 'mp4v', 5, '../../audio/in.wav',
         '../../images/in.jpg')
print()  # leave a blank line for output