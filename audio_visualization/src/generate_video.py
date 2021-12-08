# -*- coding: utf-8 -*-

"""Main script of generating a video."""


import math
import pathlib
import time
import wave
from typing import Tuple, Union

import numpy as np
from PIL import Image, ImageDraw

from video_conductor import VideoConductor


def generate(
    outfile: Union[str, pathlib.Path],
    size: Tuple[int, int],
    fps: int,
    fourcc: str,
    speed: int,
    audiofile: Union[str, pathlib.Path],
    backgroundfile: Union[str, pathlib.Path]
):
    """A function to generate the final creation.
    
    NOTE: We assume that all parameters are valid.
    """

    # Step 1: Add background image
    with Image.open(backgroundfile) as _:
        bg = _.convert('RGBA')
    draw_bg = ImageDraw.Draw(bg)
    
    # Step 2: Draw anchor line (default: 5/6 of width)
    anchor_width = size[0] // 6 * 5
    anchor_left = (size[0] - anchor_width) // 2
    anchor_right = anchor_left + anchor_width - 1
    anchor_up = math.ceil(size[1] / 2 - 1)
    anchor_down = math.floor(size[1] / 2)
    draw_bg.rectangle((anchor_left, anchor_up, anchor_right, anchor_down),
                      (255, 255, 255, 255))

    # Step 3: Pre-process wave (default: 1/5 of height)
    wr = wave.open(audiofile, 'rb')
    nframes = wr.getnframes()
    framerate = wr.getframerate()
    wave_max_height = size[1] // 5
    audio_frames_per_px = framerate / fps / speed
    # NOTE: must get max of abs of ``w`` first
    max_abs_w = max(abs(np.frombuffer(wr.readframes(nframes), dtype=np.int16)))
    # force to rewind
    wr.rewind()

    # Step 4: Define generation function
    layer_wave_height = wave_max_height * 2 + anchor_down - anchor_up + 1
    layer_wave = Image.new('RGBA', (anchor_width, layer_wave_height))
    draw_layer_wave = ImageDraw.Draw(layer_wave)

    # def callback(d: dict):
    #     if d['status'] != 'error':
    #         if d['status'] != 'write_current_frame':
    #             return
    #         if d['current_frame_pos'] % 60 != 0:
    #             return
    #     d['time'] = time.strftime('%Y-%m-%d %H:%M:%S',
    #                               time.localtime(d['time']))
    #     del d['video_writer']
    #     if 'current_frame' in d:
    #         del d['current_frame']
    #     if 'cur_frame' in d:
    #         del d['cur_frame']
    #     print(d)

    def callback(d: dict):
        if 'current_frame' in d:
            del d['current_frame']
        d['time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(d['time']))
        print(d)

    def genfunc(n: int) -> np.ndarray:
        frame = bg.copy()

        # Step 4.1: Move wave
        layer_wave.paste(layer_wave, (-speed, 0))

        for i in range(speed):
            # Step 4.2: Draw new part of wave
            wr.setpos((n * speed + i) * math.floor(audio_frames_per_px))
            str_data = wr.readframes(1)
            w = np.frombuffer(str_data, dtype=np.int16)
            w = abs(w * 1.0 / max_abs_w)  # shape: (2,)
            draw_layer_wave.line((
                anchor_right - speed + i,
                anchor_up - math.floor(wave_max_height * w[0] + 0.5),
                anchor_right - speed + i,
                anchor_down + math.floor(wave_max_height * w[1] + 0.5)
            ), (255, 255, 255, 255))
        
        # Step 4.3: Apply all layers
        frame.paste(layer_wave, (anchor_left, anchor_up - wave_max_height),
                    layer_wave)

        return np.array(frame.convert('RGB'))

    # Step 5: Launch video conductor
    vc = VideoConductor(outfile, size, fps, fourcc, genfunc)
    vc.conduct(callback=callback)
