"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import datetime 
import os
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

# Default Items basically
common_items = {
    "1": {
        "name": "Wooden Sword",
        "rarity": "common",
        "cost": 10,
        "sell": 1,
        "type": "meelee",
        "attack": 1,
        "effects": [],
    },
    "2": {
        "name": "Wooden Bow",
        "rarity": "common",
        "cost": 10,
        "sell": 1,
        "type": "ranged",
        "attack": 2,
        "effects": [],
    },
    "3": {
        "name": "Wooden Staff",
        "rarity": "common",
        "cost": 10,
        "sell": 1,
        "type": "magic",
        "attack": 1,
        "effects": [],
    }
}

# Rare items
rare_items = {
    "1": {
        "name": "Iron Sword",
        "rarity": "rare",
        "cost": 25,
        "sell": 5,
        "type": "meelee",
        "attack": 3,
        "effects": [],
    },
    "2": {
       "name": "Iron Bow",
        "rarity": "rare",
        "cost": 25,
        "sell": 5,
        "type": "ranged",
        "attack": 5,
        "effects": [],
    },
    "3": {
        "name": "Iron Staff",
        "rarity": "rare",
        "cost": 25,
        "sell": 5,
        "type": "magic",
        "attack": 2,
        "effects": [],
    }
}

# Epic rarity
epic_items = {

}

# Legendary Items :D
legendary_items = {

}

# Not actually unobtainable, just to make it sound cool
unobtainable_items = {

}


effects = {

}



async def i_get_item_data(item_id: str, rarity: str):
    """Retrieve the given items data, including drop rate, stats, what it does, you get the gist"""
    # The lowers aren't technically needed but its a precaution
    if rarity.lower() == "common":
        item_dict = common_items

    elif rarity.lower() == "rare":
        item_dict = rare_items

    elif rarity.lower() == "epic":
        item_dict = epic_items
    
    elif rarity.lower() == "legendary":
        item_dict = legendary_items

    elif rarity.lower() == "unobtainable":
        item_dict = unobtainable_items

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


async def i_add_item(id: str, item_id: str, rarity: str, amount: int=1):
    """Add an item to a user"""

async def i_del_item(id: str, item_id: str, rarity: str, amount: int=1):
    """Removes an item from a user"""