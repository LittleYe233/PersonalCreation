# -*- coding: utf-8 -*-

"""A module for video conductor."""


import pathlib
import time
from typing import Any, Callable, Dict, Iterable, Tuple, Union

import cv2
import numpy as np


class VideoConductor:
    """A class for video conductor."""

    def __init__(
        self,
        outfile: Union[str, pathlib.Path],
        size: Tuple[int, int],
        fps: int,
        fourcc: str,
        genfunc: Callable[[int], Union[np.ndarray, None]]
    ):
        """A video conductor object.
        
        :param outfile: the output video path

        :param size: size tuple of every frame

        :param fps: frames per second

        :param fourcc: a str with a length of 4 to get the fourcc code
        NOTE: For example, 'XVID' refers to XVID MPEG-4 and 'X264' refers to
        H.264. Visit https://www.fourcc.org/codecs.php for more information.

        :param genfunc: generation function
        NOTE: ``genfunc`` should accept an integer ``n`` referring to the
        ``n``-th frame and return a 2-d-like array as the frame pixels,
        returning ``None`` only if reaching the end of generation.
        """
        
        self._outfile = outfile
        self._size = size
        self._fps = fps
        self._fourcc = fourcc
        self._genfunc = genfunc

    def conduct(
        self,
        nframes: int = -1,
        callback: Union[Callable[[Dict], Any], None] = None
    ):
        """Conduct the video.
        
        Many settings of the conducted video have been handled when
        initialization. Other parameters are as below:

        :param nframes: The number of at most generated frames. -1 if using all
        frames. Other negative values will be regarded as -1. (default: -1)

        :param callback: Callback function. The function should accept a dict
        with many values. (default: None)
        """

        if not isinstance(nframes, int):
            raise TypeError('nframes should be an integer')

        if not isinstance(callback, Callable):
            raise TypeError('callback should be callable')
        
        fourcc_code = cv2.VideoWriter_fourcc(*self.fourcc)
        writer = cv2.VideoWriter(self.outfile, fourcc_code, self.fps, self.size)
        cur_frame_pos = 0
        try:
            while True:
                if cur_frame_pos == nframes:
                    callback({
                        'time': time.time(),
                        'status': 'finish_generating_frames',
                        'cause': 'reach_nframes_limit',
                        'video_writer': writer,
                        'current_frame_pos': cur_frame_pos
                    })
                    break
                cur_frame = self.genfunc(cur_frame_pos)
                if cur_frame is None:
                    callback({
                        'time': time.time(),
                        'status': 'finish_generating_frames',
                        'cause': 'generate_blank_frame',
                        'video_writer': writer,
                        'current_frame_pos': cur_frame_pos
                    })
                    break
                callback({
                    'time': time.time(),
                    'status': 'before_write_frame',
                    'video_writer': writer,
                    'current_frame_pos': cur_frame_pos,
                    'current_frame': cur_frame
                })
                writer.write(cur_frame)
                callback({
                    'time': time.time(),
                    'status': 'after_write_frame',
                    'video_writer': writer,
                    'current_frame_pos': cur_frame_pos,
                    'current_frame': cur_frame
                })
                cur_frame_pos += 1
        except Exception as e:
            callback({
                'time': time.time(),
                'status': 'error',
                'video_writer': writer,
                'current_frame_pos': cur_frame_pos,
                'current_frame': cur_frame,
                'err': e
            })
        
        writer.release()
        callback({
            'time': time.time(),
            'status': 'finish',
            'video_writer': writer,
            'current_frame_pos': cur_frame_pos,
            'current_frame': cur_frame
        })

    @property
    def outfile(self): return self._outfile

    @property
    def size(self): return self._size

    @property
    def fps(self): return self._fps
    
    @property
    def fourcc(self): return self._fourcc

    @property
    def genfunc(self): return self._genfunc

    @outfile.setter
    def outfile(self, val: Union[str, pathlib.Path]):

        if not isinstance(val, (str, pathlib.Path)):
            raise TypeError('argument should be str or a path-like object')
        self._outfile = val

    @size.setter
    def size(self, val: Tuple[int, int]):

        if not isinstance(val, Iterable):
            raise TypeError('argument should be iterable')
        if len(val) != 2:
            raise ValueError('length of argument should be 2')
        if not isinstance(val[0], int) or not isinstance(val[1], int):
            raise TypeError('elements of argument should be an integer')
        if val[0] <= 0 or val[1] <= 0:
            raise ValueError('elements of argument should not be negative')
        self._size = val

    @fps.setter
    def fps(self, val: int):

        if not isinstance(val, int):
            raise TypeError('argument should be an integer')
        if val <= 0:
            raise ValueError('argument should not be negative')
        self._fps = val

    @fourcc.setter
    def fourcc(self, val: str):

        if not isinstance(val, str):
            raise TypeError('argument should be str')
        if len(val) != 4:
            raise ValueError('length of argument should be 4')
        self._fourcc = val

    @genfunc.setter
    def genfunc(self, val: Callable):

        if not isinstance(val, Callable):
            raise TypeError('argument should be callable')
        self._genfunc = val
