# -*- coding: utf-8 -*-

"""Main script of generating a video."""


from functools import partial
import math
import pathlib
import time
import wave
from io import IOBase
from typing import Callable, Dict, List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from .video_conductor import VideoConductor
from .text_effects import SrtWithFadeLine, parse_lrc_to_srt, parse_srt_with_fade
from .text_effects import fade_in, fade_out


AVAILABLE_LRC_LANGS = ['zh', 'ja']
DEFAULT_FONTS = {
    # STKaiti
    'zh': ImageFont.truetype('./fonts/DFSHAONVW5.TTC', 72),
    # UD Digi Kyokasho N-R
    'ja': ImageFont.truetype('./fonts/UDDIGIKYOKASHON-R.TTC', 72)
}


def generate(
    outfile: Union[str, pathlib.Path],
    size: Tuple[int, int],
    fps: int,
    vcodec: str,
    bv: int,
    speed: int,
    audiofile: Union[str, pathlib.Path],
    acodec: Union[str, None],
    filter_complex: Union[str, None],
    backgroundfile: Union[str, pathlib.Path],
    lrcfiles: Dict[str, Union[str, pathlib.Path]],
    stdout: Union[int, IOBase, None],
    stderr: Union[int, IOBase, None]
) -> Image.Image:
    """A function to generate the final creation.
    
    NOTE: We assume that all parameters are valid.
    """

    # Step 1: Add background image
    with Image.open(backgroundfile) as _:
        bg_orig = _.convert('RGBA')
    bg = bg_orig.copy()
    draw_bg = ImageDraw.Draw(bg)
    
    # Step 2: Draw anchor line (default: 5/6 of width)
    anchor_width = size[0] // 6 * 5
    anchor_left = (size[0] - anchor_width) // 2
    anchor_right = anchor_left + anchor_width - 1
    anchor_up = math.ceil(size[1] / 2 - 1)
    anchor_down = math.floor(size[1] / 2)
    anchor_height = anchor_down - anchor_up + 1
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
    layer_wave_height = wave_max_height * 2 + anchor_height
    layer_wave = Image.new('RGBA', (anchor_width, layer_wave_height))
    draw_layer_wave = ImageDraw.Draw(layer_wave)

    def callback(d: dict):
        
        if d['status'] not in ('after_write_frame', 'error'):
            return
        tup = time.localtime(d['time'])
        if d['status'] != 'error' and d['current_frame_pos'] % 60 != 0:
            return
        # d['current_frame'].save('frames/%06d.png' % d['current_frame_pos'])
        print(time.strftime('%Y-%m-%d %H:%M:%S', tup), d['current_frame_pos'])
        # cv2.imwrite('frames/%06d.png' % d['current_frame_pos'],
        #             d['current_frame'])

    # Step 4.1: Fade in (default: background 6s, linear; anchor last 3s,
    # extend from center, linear)
    mask = Image.new('RGBA', size, (0, 0, 0, 255))

    def genfunc_fade_in(n: int) -> Image.Image:
        frame = bg_orig.copy()
        fps3 = 3 * fps
        if n >= fps3:
            w = anchor_width * (n - fps3) / fps3
            draw = ImageDraw.Draw(frame)
            draw.rectangle(
                (math.ceil((size[0] - w) / 2), anchor_up,
                 math.ceil((size[0] + w) / 2), anchor_down),
                (255, 255, 255, 255))
        
        return Image.blend(mask, frame, n / fps / 6).convert('RGB')

    # Step 4.2: Wave
    def genfunc_wave(n: int) -> Image.Image:
        frame = bg.copy()

        # Step 4.2.1: Move wave
        layer_wave.paste(layer_wave, (-speed, 0))

        # Step 4.2.2: Erase useless part of wave
        draw_layer_wave.rectangle(
            (anchor_width - speed, 0, anchor_width, layer_wave_height),
            (0, 0, 0, 0))

        for i in range(speed):
            # Step 4.2.3: Draw new part of wave
            wr.setpos((n * speed + i) * math.floor(audio_frames_per_px))
            str_data = wr.readframes(1) or b'\x00\x00\x00\x00'
            w = np.frombuffer(str_data, dtype=np.int16)
            w = abs(w * 1.0 / max_abs_w)  # shape: (2,)
            draw_layer_wave.line((
                anchor_width - speed + i,
                math.floor(wave_max_height * (1 - w[0]) + 0.5),
                anchor_width - speed + i,
                anchor_height - 1 + int(wave_max_height * (1 + w[1]) + 0.5)
            ), (255, 255, 255, 255))
        
        # Step 4.2.4: Apply all layers
        frame.paste(layer_wave, (anchor_left, anchor_up - wave_max_height),
                    layer_wave)

        return frame.convert('RGB')

    # Step 4.3: Subtitles (default: 500ms fade-in and -out, size=72,
    # shadow=BoxBlur(7), shadow_color=(140, 140, 140, 255))
    genfuncs: Dict[str,
                   List[Tuple[int, int, Callable[[int], Image.Image]]]] = {}

    def _get_frames(fps, line: SrtWithFadeLine):
        fade_in_secs = (line.end_fade_in - line.start_fade_in).total_seconds()
        line_secs = (line.start_fade_out - line.end_fade_in).total_seconds()
        fade_out_secs = (line.end_fade_out -
                         line.start_fade_out).total_seconds()
        fade_in_frames = math.floor(fps * fade_in_secs + 0.5)
        line_frames = math.floor(fps * line_secs + 0.5)
        fade_out_frames = math.floor(fps * fade_out_secs + 0.5)
        return (fade_in_frames, line_frames, fade_out_frames)

    def _genfunc_subtitle(n: int, fps, line: SrtWithFadeLine,
                          font: ImageFont.FreeTypeFont) -> Image.Image:
        """A full view of a subtitle line, including all special effects."""

        fade_in_frames, line_frames, fade_out_frames = _get_frames(fps, line)
        t1 = fade_in_frames + line_frames
        t2 = t1 + fade_out_frames

        def _multiline_check(text):
            """See ``_multiline_check()`` source code in ``PIL.ImageDraw``."""
            split_character = '\n' if isinstance(text, str) else b'\n'
            return split_character in text

        if _multiline_check(line.content):
            size = font.getsize_multiline(line.content)
        else:
            size = font.getsize(line.content)
        size = (size[0] + 20, size[1] + 20)  # expand a bit more

        # Step 4.3.1: Fade in
        if 0 <= n < fade_in_frames:
            return fade_in(fade_in_frames, line.content, (255, 255, 255, 255),
                           font, shadow_fill=(140, 140, 140, 255),
                           shadow_filter=ImageFilter.BoxBlur(7),
                           size_expand=(10, 10, 10, 10))(n)
        # Step 4.3.2: Stable view
        elif fade_in_frames <= n < t1:
            return fade_in(fade_in_frames, line.content, (255, 255, 255, 255),
                           font, shadow_fill=(140, 140, 140, 255),
                           shadow_filter=ImageFilter.BoxBlur(7),
                           size_expand=(10, 10, 10, 10))(fade_in_frames)
        # Step 4.3.3: Fade out
        elif t1 <= n < t2:
            return fade_out(fade_out_frames, line.content,
                            (255, 255, 255, 255), font,
                            shadow_fill=(140, 140, 140, 255),
                            shadow_filter=ImageFilter.BoxBlur(7),
                            size_expand=(10, 10, 10, 10))(n - t1)

    # Step 4.3.4: Construct with wave
    for lang, lrcfile in lrcfiles.items():
        if lang not in AVAILABLE_LRC_LANGS:
            raise ValueError('invalid subtitle language: %s' % lang)
        genfuncs[lang] = []
        with open(lrcfile, 'r', encoding='utf-8') as f:
            lrc_string = f.read()
        srt_string = parse_lrc_to_srt(lrc_string)
        fade_lines = parse_srt_with_fade(srt_string, 0.5, 0.5)

        for line in fade_lines:
            start_frame = int(fps * line.start_fade_in.total_seconds())
            t1, t2, t3 = _get_frames(fps, line)
            genfuncs[lang].append((
                start_frame,
                start_frame + t1 + t2 + t3,
                partial(_genfunc_subtitle, fps=fps, line=line,
                        font=DEFAULT_FONTS[lang])
            ))
    
    line_xy = {
        'ja': (size[0] // 2, (size[1] - layer_wave_height) // 4),
        'zh': (size[0] // 2, (3 * size[1] + layer_wave_height) // 4)
    }

    avail_langs = list(genfuncs.keys())
    line_ptrs = {k: 0 for k in avail_langs}

    if genfuncs:
        def genfunc_wave_with_subtitles(n: int) -> Image.Image:
            # Step 4.3.4.1: Generate wave layer
            img = genfunc_wave(n).convert('RGBA')

            # Step 4.3.4.2: Walk through subtitle lines by languages and apply
            # NOTE: assume that there is at least one subtitle
            for lang in avail_langs:
                lptr = line_ptrs[lang]
                if lptr >= len(genfuncs[lang]):
                    continue
                start_frame, end_frame, genfunc = genfuncs[lang][lptr]
                # This line should be applied.
                if start_frame <= n < end_frame:
                    img_line = genfunc(n - start_frame)
                    # left-top corner xy
                    lt_xy = (line_xy[lang][0] - img_line.size[0] // 2,
                             line_xy[lang][1] - img_line.size[1] // 2)
                    img.alpha_composite(img_line, lt_xy)
                # This line should be expired.
                elif n >= end_frame:
                    line_ptrs[lang] += 1

            return img.convert('RGB')
        
    # Step 4.3.5: fallback to the original `genfunc_wave` without subtitles
    else:
        genfunc_wave_with_subtitles = genfunc_wave

    # Step 4.4: Silence (default: await the whole wave fading out)
    silence_nframes = math.ceil(anchor_width / speed)

    def genfunc_still(n: int) -> Image.Image:
        frame = bg.copy()

        # Step 4.4.1: Move wave
        layer_wave.paste(layer_wave, (-speed, 0))

        # Step 4.4.2: Erase useless part of wave
        draw_layer_wave.rectangle(
            (anchor_width - speed, 0, anchor_width, layer_wave_height),
            (0, 0, 0, 0))

        # Step 4.4.3: Apply all layers
        frame.paste(layer_wave, (anchor_left, anchor_up - wave_max_height),
                    layer_wave)

        return frame.convert('RGB')

    # Step 5: Concat all generation functions
    video_nframes = math.ceil(nframes / framerate * fps)
    fps6 = 6 * fps

    def genfunc(n: int) -> Image.Image:
        if n < fps6:
            return genfunc_fade_in(n)
        elif n < fps6 + video_nframes:
            return genfunc_wave_with_subtitles(n - fps6)
        else:
            return genfunc_still(n - fps6 - video_nframes)

    # Step 6: Launch video conductor
    vc = VideoConductor(outfile, size, fps, genfunc, vcodec, bv, audiofile,
                        acodec, filter_complex)
    vc.conduct(video_nframes + fps6 + silence_nframes, stdout, stderr, callback)
