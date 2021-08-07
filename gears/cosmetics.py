"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

"""Anything to do with emojis, colors, aesthetics etc."""

import random

def c_random_color():
    """Get a random color from tenshis default colors"""
    return colors[random.choice(color_list)]

def c_get_color(color: str):
    """Return a specified color from tenshis dict."""
    return colors[color]

def c_get_emoji(emoji: str):
    """Get an emoji from tenshis emoji dict..."""
    return emojis[emoji]

colors = {
    "_id": "default",
    "navy": 0x001F3F,
    "blue": 0x0074D9,
    "aqua": 0x7FDBFF,
    "teal": 0x39CCCC,
    "olive": 0x3D9970,
    "green": 0x2ECC40,
    "lime": 0x01FF70,
    "yellow": 0xFFDC00,
    "orange": 0xFF851B,
    "red": 0xFF4136,
    "maroon": 0x85144b,
    "pink": 0xF012BE,
    "purple": 0xB10DC9,
    "black": 0x111111,
    "gray": 0xAAAAAA,
    "silver": 0xDDDDDD,
    "white": 0xFFFFFF
}

emojis = {
    "check": "<:tenshi_checkmark:873657241876705300>",
    "cancel": "<:tenshi_cancel:873659861395718227>"
}

color_list = ["navy", "blue", "aqua", "teal", "olive", "green", "lime", "yellow", "orange", "red", "maroon", "pink", "purple", "black", "gray", "silver", "white"]