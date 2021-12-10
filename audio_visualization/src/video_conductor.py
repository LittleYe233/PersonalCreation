# -*- coding: utf-8 -*-

"""A module for video conductor."""


import pathlib
import subprocess
import time
from io import IOBase
from typing import Any, Callable, Dict, Iterable, Tuple, Union

import numpy as np
from PIL import Image


class VideoConductor:
    """A class for video conductor."""

    def __init__(
        self,
        outfile: Union[str, pathlib.Path],
        size: Tuple[int, int],
        fps: int,
        vcodec: str,
        bv: int,
        genfunc: Callable[[int], Union[np.ndarray, None]],
        audiofile: Union[str, pathlib.Path, None] = None
    ):
        """A video conductor object.
        
        :param outfile: the output video path

        :param size: size tuple of every frame

        :param fps: frames per second

        :param vcodec: FFmpeg video codec string (e.g. h264)

        :param bv: FFmpeg video bitrate (unit: Kb/s)

        :param genfunc: generation function
        NOTE: ``genfunc`` should accept an integer ``n`` referring to the
        ``n``-th frame and return an HxWx3 array as the frame pixels or a
        PIL.Image.Image object with "RGB" mode (returns will be regarded as an
        Image object if it is not an array), returning ``None`` only if
        reaching the end of generation.

        :param audiofile: the audio file path (default: None)
        NOTE: The default codec is AAC and can't be changed now.
        """
        
        self._outfile = outfile
        self._size = size
        self._fps = fps
        self._vcodec = vcodec
        self._bv = bv
        self._genfunc = genfunc
        self._audiofile = audiofile

    def conduct(
        self,
        nframes: int = -1,
        stdout: Union[int, IOBase, None] = None,
        stderr: Union[int, IOBase, None] = None,
        callback: Union[Callable[[Dict], Any], None] = None
    ):
        """Conduct the video.
        
        Many settings of the conducted video have been handled when
        initialization. Other parameters are as below:

        :param nframes: The number of at most generated frames. -1 if using all
        frames. Other negative values will be regarded as -1. (default: -1)

        :param stdout: Standard output parameter for ``subprocess.Popen()``.
        See Python documentation on this function for more details.

        :param stderr: Standard error parameter for ``subprocess.Popen()``.
        See Python documentation on this function for more details.

        :param callback: Callback function. The function should accept a dict
        with many values. (default: None)
        """

        if not isinstance(nframes, int):
            raise TypeError('nframes should be an integer')

        if not isinstance(callback, Callable):
            raise TypeError('callback should be callable')

        if not isinstance(stdout, (int, IOBase, None)):
            raise TypeError('stdout should be a special constant defined in '
                            '"subprocess" module, an existing file object or '
                            'None')

        if not isinstance(stderr, (int, IOBase, None)):
            raise TypeError('stderr should be a special constant defined in '
                            '"subprocess" module, an existing file object or '
                            'None')
        
        if self.audiofile is None:
            args = ['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg',
                    '-r', str(self.fps), '-i', '-',
                    '-vcodec', self.vcodec, '-r', str(self.fps), '-vf',
                    'scale=%d:%d' % self.size, '-b:v', '%dK' % self.bv,
                    self.outfile]
        else:
            args = ['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg',
                    '-r', str(self.fps), '-i', '-',
                    '-i', self.audiofile,
                    '-vcodec', self.vcodec, '-r', str(self.fps), '-vf',
                    'scale=%d:%d' % self.size, '-b:v', '%dK' % self.bv,
                    '-acodec', 'aac',
                    self.outfile]
        ffmpeg_proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                       stdout=stdout, stderr=stderr)
        cur_frame_pos = 0
        try:
            while True:
                if nframes >= 0 and cur_frame_pos >= nframes:
                    callback({
                        'time': time.time(),
                        'status': 'finish_generating_frames',
                        'cause': 'reach_nframes_limit',
                        'ffmpeg_process': ffmpeg_proc,
                        'current_frame_pos': cur_frame_pos
                    })
                    break
                cur_frame = self.genfunc(cur_frame_pos)
                if cur_frame is None:
                    callback({
                        'time': time.time(),
                        'status': 'finish_generating_frames',
                        'cause': 'generate_blank_frame',
                        'ffmpeg_process': ffmpeg_proc,
                        'current_frame_pos': cur_frame_pos
                    })
                    break
                callback({
                    'time': time.time(),
                    'status': 'before_write_frame',
                    'ffmpeg_process': ffmpeg_proc,
                    'current_frame_pos': cur_frame_pos,
                    'current_frame': cur_frame
                })
                if isinstance(cur_frame, np.ndarray):
                    img = Image.fromarray(cur_frame)
                else:
                    img = cur_frame
                img.save(ffmpeg_proc.stdin, 'JPEG')
                callback({
                    'time': time.time(),
                    'status': 'after_write_frame',
                    'ffmpeg_process': ffmpeg_proc,
                    'current_frame_pos': cur_frame_pos,
                    'current_frame': cur_frame
                })
                cur_frame_pos += 1
        except Exception as e:
            ffmpeg_proc.stdin.close()
            callback({
                'time': time.time(),
                'status': 'error',
                'ffmpeg_process': ffmpeg_proc,
                'current_frame_pos': cur_frame_pos,
                'current_frame': cur_frame,
                'err': e
            })
        
        ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()
        callback({
            'time': time.time(),
            'status': 'finish',
            'ffmpeg_process': ffmpeg_proc,
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
    def bv(self): return self._bv
    
    @property
    def vcodec(self): return self._vcodec

    @property
    def genfunc(self): return self._genfunc

    @property
    def audiofile(self): return self._audiofile

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

    @vcodec.setter
    def vcodec(self, val: str):

        if not isinstance(val, str):
            raise TypeError('argument should be str')
        self._vcodec = val

    @bv.setter
    def bv(self, val: int):

        if not isinstance(val, int):
            raise TypeError('argument should be an integer')
        if val <= 0:
            raise ValueError('argument should not be negative')
        self._bv = val

    @genfunc.setter
    def genfunc(self, val: Callable):

        if not isinstance(val, Callable):
            raise TypeError('argument should be callable')
        self._genfunc = val

    @audiofile.setter
    def audiofile(self, val: Union[str, pathlib.Path, None]):

        if not isinstance(val, (str, pathlib.Path)) and val is not None:
            raise TypeError('argument should be str, a path-like object or '
                            'None')
        self._audiofile = val