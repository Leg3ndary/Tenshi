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

reversed_colors = {
    7999: "navy",
    29913: "blue",
    8379391: "aqua",
    3787980: "teal",
    4036976: "olive",
    3066944: "green",
    130928: "lime",
    16768000: "yellow",
    16745755: "orange",
    16728374: "red",
    8721483: "maroon",
    15733438: "pink",
    11603401: "purple",
    1118481: "black",
    11184810: "gray",
    14540253: "silver",
    16777215: "white"
}

emojis = {
    "check": "<:tenshi_checkmark:873657241876705300>",
    "cancel": "<:tenshi_cancel:873659861395718227>",
    "left": "<:tenshi_left:873755995074101248>",
    "right": "<:tenshi_right:873755994486890497>",
    "pauseplay": "<:tenshi_pp:873758110030888990>",
    "stop": "<:tenshi_stop:873758679378321458>",
    "search": "<:tenshi_search:874031008733863956>"
}

emoji_filenames = {
    "check": "tenshi_checkmark.png",
    "cancel": "tenshi_cancel.png",
    "left": "tenshi_left.png",
    "right": "tenshi_right.png",
    "pauseplay": "tenshi_pp.png",
    "stop": "tenshi_stop.png",
    "search": "tenshi_search.png"
}

emoji_descriptions = {
    "check": "Half of a lopsided X that means ",
    "cancel": "tenshi_cancel.png",
    "left": "tenshi_left.png",
    "right": "tenshi_right.png",
    "pauseplay": "tenshi_pp.png",
    "stop": "tenshi_stop.png",
    "search": "tenshi_search.png"
}

color_list = ["navy", "blue", "aqua", "teal", "olive", "green", "lime", "yellow", "orange", "red", "maroon", "pink", "purple", "black", "gray", "silver", "white"]