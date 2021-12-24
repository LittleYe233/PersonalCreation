# -*- coding: utf-8 -*-

"""A module for text special effects."""


from datetime import timedelta
from functools import partial
from typing import Any, Callable, Generator, List, Literal, Tuple, Union

import srt
import math
import pylrc
from PIL import Image, ImageDraw, ImageFilter, ImageFont


# Type aliases
_RGB = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
_Ink = Union[str, int, _RGB]


# Subclasses
class SrtWithFadeLine:
    """A class for srt line with fading special effects."""

    def __init__(
        self,
        content: Union[str, None] = None,
        start_fade_in: Union[str, timedelta] = None,
        end_fade_in: Union[str, timedelta] = None,
        start_fade_out: Union[str, timedelta] = None,
        end_fade_out: Union[str, timedelta] = None
    ):
        self.content = content
        self.start_fade_in = start_fade_in
        self.end_fade_in = end_fade_in
        self.start_fade_out = start_fade_out
        self.end_fade_out = end_fade_out

    def __repr__(self):
        attrs = ('content', 'start_fade_in', 'end_fade_in', 'start_fade_out',
                 'end_fade_out')
        attrs_str = ', '.join('%s=%r' % (k, getattr(self, k)) for k in attrs)
        return '%s(%s)' % (type(self).__name__, attrs_str)


##################
# Special Effects
##################

def fade(
    nframes: int,
    text: Union[str, bytes],
    fill: Union[_Ink, None] = None,
    font: Union[ImageFont.FreeTypeFont, None] = None,
    spacing: float = 4,
    align: Literal['left', 'center', 'right'] = 'left',
    direction: Union[Literal['rtl', 'ltr', 'ttb'], None] = None,
    features: Union[Any, None] = None,
    language: Union[str, None] = None,
    stroke_width: int = 0,
    stroke_fill: Union[_Ink, None] = None,
    embedded_color: bool = False,
    shadow_fill: Union[_Ink, None] = None,
    shadow_filter: Union[ImageFilter.Filter, None] = None,
    size_expand: Union[Tuple[int, int, int, int], None] = None,
    mode: Literal['in', 'out'] = 'in'
) -> Callable[[int], Image.Image]: 
    """Create a RGBA image of the string with fade-in special effect at the
    given position and make it into a generation function.
    
    "Fade-in" means the text animated from being fully transparent to the
    maximum opacity linearly.

    :param nframes: the number of frames the special effect lasts

    :param shadow_filter: the filter of optional shadow of text

    :param size_expand: how the size of image expands
    NOTE: The order of elements is (left, top, right, bottom).

    :param mode: specify if fading in or fading out

    See documentation of ``PIL.ImageDraw.ImageDraw.multiline_text()`` for other
    paramenters.
    NOTE: ``fill`` and ``stroke_fill`` must be a 4-tuple, and with ``None``
    value the function still returns the generation function but with
    unexpected results.. ``font`` must be an ``ImageFont.FreeTypeFont`` object.

    :returns: A generation function whose ``n`` should begin with 0, returning
    an ``Image.Image`` object with mode RGBA, background color (0, 0, 0, 0) and
    left-up corner position (0, 0).

    NOTE: This function is so awful and ugly and I have found how to code it
    better. But I don't have enough time and willingness to rewrite it.
    """

    if mode not in ('in', 'out'):
        raise ValueError('invalid mode')

    def _multiline_check(text):
        """See ``_multiline_check()`` source code in ``PIL.ImageDraw``."""
        split_character = '\n' if isinstance(text, str) else b'\n'
        return split_character in text

    if _multiline_check(text):
        size = font.getsize_multiline(text, direction, spacing, features,
                                      language, stroke_width)
    else:
        size = font.getsize(text, direction, features, language, stroke_width)
    if size_expand is not None:
        size = (size[0] + size_expand[0] + size_expand[2],
                size[1] + size_expand[1] + size_expand[3])
    center = (size[0] // 2, size[1] // 2)
    if fill is not None:
        if mode == 'in':
            color: Callable[[int], Tuple] = (
                lambda n: (
                    *fill[:3],
                    math.floor(n / nframes * fill[3] + 0.5)))
        else:
            color: Callable[[int], Tuple] = (
                lambda n: (
                    *fill[:3],
                    255 - math.floor(n / nframes * fill[3] + 0.5)))
    else:
        color: Callable[[int], None] = lambda n: None
    if stroke_fill is not None:
        if mode == 'in':
            stroke_color: Callable[[int], Tuple] = (
                lambda n: (
                    *stroke_fill[:3],
                    math.floor(n / nframes * stroke_fill[3] + 0.5)))
        else:
            stroke_color: Callable[[int], Tuple] = (
                lambda n: (
                    *stroke_fill[:3],
                    255 - math.floor(n / nframes * stroke_fill[3] + 0.5)))
    else:
        stroke_color: Callable[[int], None] = lambda n: None
    if shadow_filter is not None:
        if shadow_fill is None:
            shadow_fill = (255, 255, 255)
        if mode == 'in':
            shadow_color: Callable[[int], Tuple] = (
                lambda n: (
                    *shadow_fill[:3],
                    math.floor(n / nframes * shadow_fill[3] + 0.5)))
        else:
            shadow_color: Callable[[int], Tuple] = (
                lambda n: (
                    *shadow_fill[:3],
                    255 - math.floor(n / nframes * shadow_fill[3] + 0.5)))

    def genfunc(n: int) -> Image.Image:
        img = Image.new('RGBA', size)
        draw = ImageDraw.Draw(img)
        if shadow_filter is not None:
            draw.text(center, text, shadow_color(n), font, 'mm', spacing,
                      align, direction, features, language, stroke_width,
                      stroke_color(n), embedded_color)
            img = img.filter(shadow_filter)
            draw = ImageDraw.Draw(img)
        draw.text(center, text, color(n), font, 'mm', spacing, align,
                  direction, features, language, stroke_width, stroke_color(n),
                  embedded_color)
        return img

    return genfunc

fade_in = partial(fade, mode='in')
fade_out = partial(fade, mode='out')

#########
# Parser
#########

def parse_lrc_to_srt_iter(
    lrc: str
) -> Generator:
    """Parse .lrc file content to a generator in ``srt`` module.

    :param lrc: .lrc file content

    :returns: a generator of ``srt.Subtitle``
    """

    return srt.parse(pylrc.parse(lrc).toSRT())


def parse_lrc_to_srt(
    lrc: str
) -> str:
    """Parse .lrc file content to SRT string.

    :param lrc: .lrc file content

    :returns: SRT string
    """

    return pylrc.parse(lrc).toSRT()


# NOTE: You have no need to consider many possible situations. The user is
# yourself, and you are not a noob user!

def parse_srt_with_fade(
    s: str,
    fade_in: float,
    fade_out: float
) -> List[SrtWithFadeLine]:
    """Parse SRT string and add with fade-in and fade-out times.

    :param s: SRT string

    :param fade_in: seconds of fading in

    :param fade_out: seconds of fading out

    This function will try to solve all time conflicts. If there is a conflict
    between fading out of the previous line and fading in of the current line,
    it will first try to rearrange the fade-in and fade-out durations with the
    same ratio as ``fade_in / fade_out``. But if the two lines are so close
    that a conflict happens, the rearrangement will still be done, but
    ``start_fade_out`` of the previous line and ``end_fade_in`` of the current
    line will be shifted towards opposite directions to make the durations
    reach the specified parameters respectively thus the duration of the line
    in stable view status (opacity reaches maximum) shrinking. And if there is
    still any conflict, a ``ValueError`` will be raised.

    :returns: list of ``SrtWithFadeLine``
    NOTE: It's obvious that the line starts at ``end_fade_in`` and ends at
    ``start_fade_out``.
    """

    srts = list(srt.parse(s))
    results: List[SrtWithFadeLine] = []
    for i, line in enumerate(srts):
        start_fade_in = line.start - timedelta(seconds=fade_in)
        if i > 0 and start_fade_in <= results[i - 1].end_fade_out:
            ratio = fade_out / fade_in
            delta = line.start - results[i - 1].start_fade_out
            anchor = (line.start - delta / (1 + ratio)) // 1000 * 1000
            new_start_fade_out = anchor - timedelta(seconds=fade_out)
            if results[i - 1].end_fade_in > new_start_fade_out:
                raise ValueError('special effect timestamps conflicted')
            results[i - 1].start_fade_out = new_start_fade_out
            results[i - 1].end_fade_out = anchor
            
            results.append(SrtWithFadeLine(
                line.content,
                anchor + timedelta(milliseconds=1),
                anchor + timedelta(seconds=fade_in),
                line.end,
                line.end + timedelta(seconds=fade_out)
            ))
        else:
            results.append(SrtWithFadeLine(
                line.content,
                start_fade_in,
                line.start,
                line.end,
                line.end + timedelta(seconds=fade_out)
            ))
    
    return results