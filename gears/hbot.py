"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import os
import datetime

"""This is a simply a file to store functions and or things I may use too save space"""

def h_len_file(file):
    """Return the file length for a given file"""
    try:
        with open(file, encoding="utf8") as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    except Exception as e:
        print(e)
        return 0

def h_get_files(directory: str=None):
    """Return every file using recursion"""
    files = []
    if directory:
        if directory == "__pycache__":
            directories = []
        else:
            directories = os.listdir(directory)
            filepath = directory + "/"
    else:
        filepath = ""
        directories = os.listdir()

    for file in directories: 
        if file.endswith(".exe") or file.endswith(".png") or file.endswith(".pyc"):
            pass
        elif "." not in file:
            recursion = h_get_files(f"{filepath}{file}")
            files = files + recursion
        else:
            files.append(f"{filepath}{file}")
    return files

async def h_get_prefix(bot, message):
    """Gets the prefix from built cache, if a guild isn't found (Direct Messages) assumes prefix is the below"""
    if message.guild is None:
        return "t>"
    else:
        return bot.prefix_cache[str(message.guild.id)]

def h_get_time():
    """Discord.py 2.0 involves some changes, 1 being that date objects are taken differently. To avoid this replacing it with this function which we can later change"""
    return h_get_time()