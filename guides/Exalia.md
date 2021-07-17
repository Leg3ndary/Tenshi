# Exalia
Welcome to the universe Exalia, a collection of sky islands across many galaxies.

Sadly many of them are now lost and your goal is to find them.

# Getting Started
First you will need to choose a class, there are 5 in total, each of them start with varying items, stats and skills (Unlockable later on).

After that you will need a subclass each class will have 3.

1. Knight
    - Stats
        - Attack 5
        - Defence 5
        - Magic 1
        - Health 5
        - Armor 5
        - Speed 4
    - Items
        - Sword
        - Armor

2. Wizard
    - Stats
        - Attack 2
        - Defence 1
        - Magic 10
        - Health 4
        - Armor 4
        - Speed 4
    - Starts with
        - Staff
        - Potions

3. Archer
    - Stats
        - Attack 8
        - Defence 3
        - Magic 3
        - Health 4
        - Armor 4
        - Speed 3
    - Starts with
        - Bow
        - Shortsword

4. Assassin
    - Stats
        - Attack 6
        - Defence 2
        - Magic 2
        - Health 3
        - Armor 4
        - Speed 8
    - Starts with
        - Daggers
        - 

5. Giant
    - Stats
        - Attack 7
        - Defence 7
        - Magic 1
        - Health 8
        - Armor 1
        - Speed 1

    - Starts with
        - Mace
        - 

## Subclasses

Subclasses give you a few boosts in stats, they always give 5 more points to your stats

1. Knight
    - Tank
        - Get +3 Armor and +4 Health and -2 Speed
    - Swordsman
        - Get +4 Attack and +1 Defence

2. Wizard
    - Arcanist
        - Get +5 Magic
    - Scholar
        - Get +2 Attack and +2 Defence and +1 Magic

3. Archer
    - Sniper
        - Get +5 Attack
    - Hunter
        - Get +1 Health and +2 Armor and +2 Speed

4. Assassin
    - Fighter
        - Get +3 Attack and +2 Defence
    - Runner
        - Get +3 Speed and +2 Attack

5. Giant
    - Golem
        - Get +5 Armor
    - Berserker
        - Get +2 Health
        - Get +3 Speed


# Stats
Stats determine what traits you're strong in.
Each trait has a maximum of 5x your default value, for example if you have a 10 in attack you would have max of 50 attack.

| Stat | Description |
|--- | --- |
| Attack | Your attack points is your attack number. |
| Defence | All attack points under this level is reduced by half |
| Magic | An alternative to attack, once divided by 2 that is your magic points, this ignores armor |
| Health | Your health points |
| Armor | An auto regenerating "Shield" that attack points must "break" before damaging health |
| Speed | Determines who "Attacks" first |

# Battles
Battles will always have at max 5 turns (Each turn consists of you attacking and defending).

```diff
+ Player did some dmg
- Player took some dmg
+ Player did some dmg
- Player took some dmg
+ Player did some dmg
- Player took some dmg
+ Player did some dmg
- Player took some dmg
+ Player did some dmg
- Player took some dmg
--- Outcome ---
+ Win
or 
- Loss
```

# Weapons/Items/Collectables
In Exalia items are split into 3 types, remember every items can be sold and or traded to other players.

## Collectables
Don't do anything, merely for self pleasure or trading.

These aren't all useless though!

In special events and or a future stock market, you'll be able to use these to earn some extra coins and gems!


## Items
Will always have a usable function, also known as consumable

Usually gives some sort of stat or new command.


## Weapons
Armor falls under this class, anything that will be used in battle for offence or defense.

Each weapon has 4 (Technically 3) stats for battle:

1. Type
    - Meelee, Ranged, Magic
        - Meelee will use your regular attack points as damage.
        - Ranged will use your regular attack points as damage however you will not have any defence, however generally ranged weapons will be stronger.
        - Magic will use your magic power as damage, in addition to that you will usually have bonus effects at the cost of an overall weaker weapon

2. Effects
    - Effects your weapon might have, meelee weapons might have one, ranged will almost never have one, magic will always have one
    - Listed below are all the possible effects in a table
    - Each effect will have an I, II, or III level, this will multiply the effects power by its respective level, this is unchangeable.

| Effect | Description (Remember every turn consists of you attacking **and** defending) |
|--- | --- |
| Fire | For 2 turns your enemy will take 2 points of damage each turn |
| Poison | For 5 turns your enemy will take 1 point of damage each turn |
| Spikes | For 3 turns your enemy will take 1 point of damage |
| Lucky Shot | Have a 5% chance of inflicting **double** damage. Chance increases per level |
| Paralysis | Have a 5% chance of making the enemy miss a turn |
| Lifesteal | Have a 5% chance of stealing half of your attack points health from your enemy |

3. Secondary Effect
A bonus second effect you might get for your weapon, literally just a second effect from the list above

4. Attack
- An additional attack damage to add to every attack minimum 1