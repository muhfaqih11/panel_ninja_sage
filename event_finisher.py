from cd_event import fight_cd_event, fight_pumpkin_event, fight_yinyang_event, fight_gi_event
from leveling import start_leveling
import time

def event_finisher():
    times_loop = int(input("How many times you want to complete your event : "))
    gi_to_id = {
        "1": "ene_2095",
        "2": "ene_2096",
        "3": "ene_2097",
        "4": "ene_2098",
        "5": "ene_2099"
    }
    yinyang_number_to_id = {
        "1": "ene_2100",
        "2": "ene_2101",
    }
    pumpkin_number_to_id = {
        "1": "ene_2104",
        "2": "ene_2105",
        "3": "ene_2106",
        "4": "ene_2103",
        "5": "ene_2102"
    }
    print("Choose your enemy to fight:")
    print("1. Pumpkin Minion")
    print("2. Skeleton Ninja")
    print("3. Zombie Samurai")
    print("4. Headless Pumpkin Horseman")
    print("5. Cursed Pumpkin King")

    p_enemy = input("What enemy do you want to fight ? ")
    p_enemy_id = pumpkin_number_to_id.get(p_enemy)
    print("")
    print("Choose your enemy to fight:")
    print("1. Yin Tiger")
    print("2. Yang Dragon")

    y_enemy = input("What enemy do you want to fight ? ")
    y_enemy_id = yinyang_number_to_id.get(y_enemy)
    print("")
    print("Choose your enemy to fight:")
    print("1. Lembuswana")
    print("2. Besukih")
    print("3. Leak")
    print("4. Ahool")
    print("5. Sembrani")

    gi_enemy = input("What enemy do you want to fight ? ")
    gi_enemy_id = gi_to_id.get(gi_enemy)

    enemy_list = ["ene_2112",p_enemy_id,y_enemy_id,gi_enemy_id]

    for i in range(times_loop):
        print("doing event")
        fight_cd_event()
        fight_pumpkin_event(enemy_list[1])
        fight_yinyang_event(enemy_list[2])
        fight_gi_event(enemy_list[3])
        start_leveling(3200)


    print("All selected event bosses have been fought. Restarting the cycle...")