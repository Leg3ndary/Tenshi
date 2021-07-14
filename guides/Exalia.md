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