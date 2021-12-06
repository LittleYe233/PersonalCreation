# -*- coding: utf-8 -*-

"""A module for audio visualization."""


import wave
from typing import Generator, Iterable, Union

import matplotlib.pyplot as plt
import numpy as np


def get_wave_dots(wr: wave.Wave_read) -> np.ndarray:
    """Get y-axis positions of wave dots of all channels.
    
    :param wr: a ``Wave_read`` object

    :return: a ``numpy.ndarray`` with all expected positions
    """
    
    # get parameters of a wave file
    params = wr.getparams()
    # the number of channels, sample width, frame rate, the number of frames
    nchannels, nframes = params[0], params[3]
    # read frames as bytes
    str_data = wr.readframes(nframes)
    # convert bytes to ``numpy.ndarray``
    w = np.frombuffer(str_data, dtype=np.int16)
    # normalize the array, since the maximum is 32767
    # NOTE: There are both positive and negative numbers in the array.
    w = w * 1.0 / max(abs(w))
    # reshape the array
    # NOTE: The first dimension is a period of one frame. The second dimension
    # is the number of channels.
    w = np.reshape(w, (nframes, nchannels))

    return w


def iter_wave_dots(
    wr: wave.Wave_read,
    chunk: int = 0
) -> Generator:
    """Return a generator of wave dots.
    
    :param wr: a ``Wave_read`` object
    
    :param chunk: The number of handled wave dots in every iteration. 0 means
    returning all the wave dots. (default: 0)

    :return: a generator object
    """

    # get parameters of a wave file
    params = wr.getparams()
    # the number of channels, sample width, frame rate, the number of frames
    nchannels, nframes = params[0], params[3]

    # validate chunk
    if not isinstance(chunk, int):
        raise TypeError('chunk should be an integer')
    elif chunk < 0:
        raise ValueError('chunk should not be negative')
    elif chunk == 0:
        chunk = nframes

    # force to rewind
    wr.rewind()
    # NOTE: must get max of abs of ``w`` first
    max_abs_w = max(abs(np.frombuffer(wr.readframes(nframes), dtype=np.int16)))
    # force to rewind
    wr.rewind()

    while True:
        # reach end of file
        if wr.tell() == nframes:
            break
        # read frames as bytes
        str_data = wr.readframes(chunk)
        # convert bytes to ``numpy.ndarray``
        w = np.frombuffer(str_data, dtype=np.int16)
        # normalize the array, since the maximum is 32767
        # NOTE: There are both positive and negative numbers in the array.
        w = w * 1.0 / max_abs_w
        # reshape the array
        # NOTE: The first dimension is a period of one frame. The second
        # dimension is the number of channels.
        w = np.reshape(w, (w.shape[0] // nchannels, nchannels))
        yield w


def show_wave(
    wave_dots: np.ndarray,
    framerate: int,
    channels: Union[Iterable[int], int, None] = None
):
    """Show the figure of waves.
    
    :param wave_dots: a ``numpy.ndarray`` of wave dots

    :param framerate: frame rate of the waves

    :param channels: a list of integers or an integer of channels
    """

    # check which wave figure of channels should be shown
    max_channels = wave_dots.shape[1]
    if channels is None:
        channels = range(1, max_channels + 1)
    elif isinstance(channels, int):
        channels = [channels]
    elif not isinstance(channels, Iterable):
        raise TypeError('channels should be iterable or an integer')
    for channel in channels:
        if not (1 <= channel <= max_channels):
            raise ValueError('channel out of index')
    
    nframes = wave_dots.shape[0]
    len_channels = len(channels)
    x_pos = np.arange(0, nframes) * 1.0 / framerate
    plt.figure()
    for idx, channel in enumerate(channels):
        plt.subplot(len_channels, 1, idx + 1)
        plt.plot(x_pos, wave_dots[:, idx])
        plt.xlabel('Time (s)')
        plt.title('Channel %d' % (idx + 1))
    plt.show()