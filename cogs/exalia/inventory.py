"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime 
from cogs.colors import *
import os
import time
import asyncio
import motor.motor_asyncio

exalia_client = motor.motor_asyncio.AsyncIOMotorClient(
    f"""mongodb+srv://{os.getenv("ExaliaUser")}:{os.getenv("ExaliaPass")}@exalia.w0dur.mongodb.net/users?retryWrites=true&w=majority"""
)

users = exalia_client["users"]

data = users["data"]
inv = users["inv"]

"""
Simple file so we can organize inventories and items and how they work...
"""

# Default Items can have a common up to epic rarity
default_items = {
    "1": {
        "name": "Sword",
        "cost": 10,
        "sell": 1,
        "type"
        "stats": {}
    }
}


# Legendary Items :D
legendary_items = {

}


# Mythical Items
mythical_items = {

}


# Not actually unobtainable, just to make it sound cool
unobtainable_items = {

}


effects = {

}


"""Turning this into an async function just cuz"""
async def i_get_item_data(item_id: str, rarity: str):
    """Retrieve the given items data, including drop rate, stats, what it does, you get the gist"""
    if rarity.lower() in ["common", "uncommon", "rare", "epic"]:
        item_dict = default_items
    
    elif rarity.lower() == "legendary":
        item_dict = legendary_items

    elif rarity.lower() == "mythical":
        item_dict = mythical_items

    else:
        item_dict = unobtainable_items

    item_data = item_dict.get(item_id, None)

    # If item is somehow not found
    if not item_data:
        raise Exception(f"Item not Found.\nItem ID: {item_id}\nDict: {item_dict}\n{datetime.datetime.utcnow()}")

    # Moving on
    else:
        item_data = {
            
        }

    return item_data