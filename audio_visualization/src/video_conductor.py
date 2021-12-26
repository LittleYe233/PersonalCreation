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
        genfunc: Callable[[int], Union[np.ndarray, None]],
        vcodec: Union[str, None] = None,
        bv: Union[int, None] = None,
        audiofile: Union[str, pathlib.Path, None] = None,
        acodec: Union[str, None] = None,
        filter_complex: Union[str, None] = None
    ):
        """A video conductor object.
        
        :param outfile: the output video path

        :param size: size tuple of every frame

        :param fps: frames per second

        :param genfunc: generation function
        NOTE: ``genfunc`` should accept an integer ``n`` referring to the
        ``n``-th frame and return an HxWx3 array as the frame pixels or a
        PIL.Image.Image object with "RGB" mode (returns will be regarded as an
        Image object if it is not an array), returning ``None`` only if
        reaching the end of generation.

        :param vcodec: FFmpeg video codec string (e.g. h264). Use ``None``
        to remove this option in FFmpeg args. (default: None)

        :param bv: FFmpeg video bitrate (unit: Kb/s). Use ``None`` to remove
        this option in FFmpeg args. (default: None)

        :param audiofile: The audio file path. Use ``None`` to remove this
        option in FFmpeg args. (default: None)

        :param acodec: FFmpeg audio codec string (e.g. aac). Use ``None``
        to remove this option in FFmpeg args. You can't set a specific codec
        if ``.audiofile`` is None. (default: None)

        :param filter_complex: FFmpeg filter_complex string. Use ``None``
        to remove this option in FFmpeg args. (default: None)
        """
        
        self._outfile = outfile
        self._size = size
        self._fps = fps
        self._genfunc = genfunc
        self._vcodec = vcodec
        self._bv = bv
        self._audiofile = audiofile
        self._acodec = acodec
        self._filter_complex = filter_complex

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
        
        # parse args
        args = ['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg',
                '-r', str(self.fps), '-i', '-']
        if self.audiofile is not None:
            args.extend(['-i', self.audiofile])
        if self.vcodec is not None:
            args.extend(['-vcodec', self.vcodec])
        args.extend(['-r', str(self.fps), '-vf', 'scale=%d:%d' % self.size])
        if self.bv is not None:
            args.extend(['-b:v', '%dK' % self.bv])
        if self.acodec is not None:
            args.extend(['-acodec', self.acodec])
        if self.filter_complex is not None:
            args.extend(['-filter_complex', self.filter_complex])
        args.append(self.outfile)

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
            # ffmpeg_proc.stdin.close()
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
    def vcodec(self): return self._vcodec

    @property
    def genfunc(self): return self._genfunc

    @property
    def fps(self): return self._fps

    @property
    def bv(self): return self._bv

    @property
    def audiofile(self): return self._audiofile

    @property
    def acodec(self): return self._acodec

    @property
    def filter_complex(self): return self._filter_complex

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

    @genfunc.setter
    def genfunc(self, val: Callable):

        if not isinstance(val, Callable):
            raise TypeError('argument should be callable')
        self._genfunc = val

    @vcodec.setter
    def vcodec(self, val: Union[str, None]):

        if not isinstance(val, str) and val is not None:
            raise TypeError('argument should be str or None')
        self._vcodec = val

    @bv.setter
    def bv(self, val: Union[int, None]):

        if not isinstance(val, int) and val is not None:
            raise TypeError('argument should be an integer or None')
        if val <= 0:
            raise ValueError('argument should not be negative')
        self._bv = val

    @audiofile.setter
    def audiofile(self, val: Union[str, pathlib.Path, None]):

        if not isinstance(val, (str, pathlib.Path)) and val is not None:
            raise TypeError('argument should be str, a path-like object or '
                            'None')
        self._audiofile = val

    @acodec.setter
    def acodec(self, val: Union[str, None]):

        if val is not None and self.audiofile is None:
            raise ValueError('audio file is not specified')

        if not isinstance(val, str) and val is not None:
            raise TypeError('argument should be str or None')
        self._acodec = val

    @filter_complex.setter
    def filter_complex(self, val: Union[str, None]):

        if not isinstance(val, str) and val is not None:
            raise TypeError('argument should be str or None')
        self._filter_complex = val