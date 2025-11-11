from utils import send_amf_request, save_to_json, open_json_to_dict , flatten_json, get_data_by_id, StatManager, CUCSG
import struct
from typing import List
import config
import time
import keyboard
import random

battle_hash = "eyJpdGVtcyI6eyJhY2Nlc3NvcnkiOiJhY2Nlc3NvcnlfMDQiLCJiYWNrX2l0ZW0iOiJiYWNrXzIyMDIiLCJ3ZWFwb24iOiJ3cG5fMjIxMyIsInNldCI6InNldF84MzFfMCJ9LCJfX19fIjpbeyJfIjoic2tpbGxfMDQiLCJfXyI6MjMzOTd9LHsiXyI6InNraWxsXzIzMDciLCJfXyI6NTQxMTR9LHsiXyI6InNraWxsXzAzIiwiX18iOjIyOTM0fSx7Il8iOiJza2lsbF82NTMiLCJfXyI6ODE1MTJ9LHsiXyI6InNraWxsXzE5NSIsIl9fIjo2NTczM30seyJfIjoic2tpbGxfMzE0IiwiX18iOjUyNjgxfSx7Il8iOiJza2lsbF8xODciLCJfXyI6NDc1Nzl9LHsiXyI6InNraWxsXzE2NCIsIl9fIjo1NDQ0NH1dLCJzdGF0dXMiOnsiZWFydGgiOjAsImxpZ2h0bmluZyI6MCwiZmlyZSI6MCwid2F0ZXIiOjAsIndpbmQiOjczfSwiYnl0ZXMiOnsiX19fIjoiMTc2Mjg0MzY2NjQwMzY3YzNjYzk5OWE5ZjllOTUxYTFkMzMyMTE1NDViODRiMmQ1YTYzOTMzYjAwMjA0MzMwMDBjM2JiNDEwZmIxNzYyODQzNjY2MTc2Mjg0MzY2NjE3NjI4NDM2NjYxNzYyODQzNjY2IiwiX19fX19fIjo4MjI4NDQ3LCJfIjo4MjI4NDQ3LCJfXyI6ODIyODQ0NywiX19fXyI6MTc2Mjg0MzY2NiwiX19fX18iOjgyMjg0NDd9fQ=="
enemy_list = open_json_to_dict("data/enemy.json")

def fight_cd_event():
    # char_data = open_json_to_dict("char_data.json")

    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]

    session_key = config.login_data["sessionkey"]
    
    parameters = [char_id,session_key]
    event_battle = send_amf_request("ConfrontingDeathEvent2025.getBattleData", parameters)
    
    print(event_battle['energy']," energy available for CD Event Boss fights.")

    for i in range(event_battle['energy']):
        print(f"Starting CD Event Boss Fight ")
        boss_id = "ene_2112"
        agility = StatManager.calculate_stats_with_data("agility", char_data)
        boss_attr = "id:ene_2112|hp:30000|agility:150"

        hash_input = str(char_id) + str(boss_id) + boss_attr + str(agility)
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, boss_id, agility, boss_attr, mission_hash, session_key]

        event_battle_data = send_amf_request("ConfrontingDeathEvent2025.startBattle", parameters)
        
        time.sleep(10)

        battle_dmg = random.randint(5000, 10000)
        hash_input = str(char_id) + str(boss_id) + event_battle_data['code'] + str(battle_dmg) + battle_hash
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, boss_id, event_battle_data['code'], battle_dmg, mission_hash, battle_hash, session_key]
        event_battle_result = send_amf_request("ConfrontingDeathEvent2025.finishBattle", parameters)
        
        if event_battle_result['status'] == 1:
            print(f"Successfully defeated CD Event Boss","Gained xp: ",event_battle_result['result'][0],"Gained Gold: ",event_battle_result['result'][1])
    print("Finished fighting Confronting Death Event Boss. No energy left")


def fight_pumpkin_event(enemy_id=None):

    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]
    
    session_key = config.login_data["sessionkey"]
    
    parameters = [char_id,session_key]
    event_battle = send_amf_request("HalloweenEvent2025.getBattleData", parameters)
    # {'status': 1, 'error': 0, 'energy': 0, 'kill_counts': {'ene_2104': 12, 'ene_2105': 0, 'ene_2106': 0, 'ene_2103': 0, 'ene_2102': 0}, 'final_boss_unlocked': False}
    
    pumpkin_number_to_id = {
        "1": "ene_2104",
        "2": "ene_2105",
        "3": "ene_2106",
        "4": "ene_2103",
        "5": "ene_2102"
    }
    print(event_battle['energy']," energy available for Pumpkin Event fights.")
    if enemy_id is None:
        print("Choose your enemy to fight:")
        print("1. Pumpkin Minion",event_battle["kill_counts"]["ene_2104"])
        print("2. Skeleton Ninja",event_battle["kill_counts"]["ene_2105"])
        print("3. Zombie Samurai",event_battle["kill_counts"]["ene_2106"])
        print("4. Headless Pumpkin Horseman",event_battle["kill_counts"]["ene_2103"])
        print("5. Cursed Pumpkin King",event_battle["kill_counts"]["ene_2102"])

        chosen_enemy = input("What enemy do you want to fight ? ")
        enemy_id = pumpkin_number_to_id.get(chosen_enemy)
    # char_data = open_json_to_dict("char_data.json")
    enemy_data = get_data_by_id(enemy_id, enemy_list)
    

    # print(event_battle)

    for i in range(event_battle['energy']):
        print(f"Starting Pumpkin event Fight ")
        agility = StatManager.calculate_stats_with_data("agility", char_data)
        enemy_attr = "id:"+enemy_id+"|hp:"+str(enemy_data['hp'])+"|agility:"+str(enemy_data['agility'])    
        # boss_attr = "id:ene_2112|hp:30000|agility:150"

        hash_input = str(char_id) + str(enemy_id) + enemy_attr + str(agility)
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, agility, enemy_attr, mission_hash, session_key]

        event_battle_data = send_amf_request("HalloweenEvent2025.startBattle", parameters)
        
        time.sleep(10)
        battle_dmg = random.randint(5000, 10000)

        hash_input = str(char_id) + str(enemy_id) + event_battle_data['code'] + str(battle_dmg) + battle_hash
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, event_battle_data['code'], battle_dmg, mission_hash, battle_hash, session_key]
        event_battle_result = send_amf_request("HalloweenEvent2025.finishBattle", parameters)
        
        if event_battle_result['status'] == 1:
            print(f"Successfully defeated Pumpkin Event","Gained xp: ",event_battle_result['result'][0],"Gained Gold: ",event_battle_result['result'][1])
    print("Finished fighting Pumpkin Event. No energy left")


def fight_yinyang_event(enemy_id=None):

    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]
    
    session_key = config.login_data["sessionkey"]
    
    parameters = [char_id,session_key]
    event_battle = send_amf_request("YinYangEvent.getBattleData", parameters)
    yinyang_number_to_id = {
        "1": "ene_2100",
        "2": "ene_2101",
    }
    print(event_battle['energy']," energy available for Yin Yang Event fights.")

    if(enemy_id is None):
        print("Choose your enemy to fight:")
        print("1. Yin Tiger",event_battle["yin_kills"])
        print("2. Yang Dragon",event_battle["yang_kills"])

        chosen_enemy = input("What enemy do you want to fight ? ")
        enemy_id = yinyang_number_to_id.get(chosen_enemy)
    # char_data = open_json_to_dict("char_data.json")
    enemy_data = get_data_by_id(enemy_id, enemy_list)
    

    for i in range(event_battle['energy']):
        print(f"Starting Yin Yang event Fight ")
        agility = StatManager.calculate_stats_with_data("agility", char_data)
        enemy_attr = "id:"+enemy_id+"|hp:"+str(enemy_data['hp'])+"|agility:"+str(enemy_data['agility'])    
        # boss_attr = "id:ene_2112|hp:30000|agility:150"

        hash_input = str(char_id) + str(enemy_id) + enemy_attr + str(agility)
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, agility, enemy_attr, mission_hash, session_key]

        event_battle_data = send_amf_request("YinYangEvent.startBattle", parameters)
        
        time.sleep(10)

        battle_dmg = random.randint(5000, 10000)
        hash_input = str(char_id) + str(enemy_id) + event_battle_data['code'] + str(battle_dmg) + battle_hash
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, event_battle_data['code'], battle_dmg, mission_hash, battle_hash, session_key]
        event_battle_result = send_amf_request("YinYangEvent.finishBattle", parameters)
        
        if event_battle_result['status'] == 1:
            print(f"Successfully defeated Yin Yang Event","Gained xp: ",event_battle_result['result'][0],"Gained Gold: ",event_battle_result['result'][1])
    print("Finished fighting Yin Yang Event. No energy left")

def fight_gi_event(enemy_id=None):
    gi_to_id = {
        "1": "ene_2095",
        "2": "ene_2096",
        "3": "ene_2097",
        "4": "ene_2098",
        "5": "ene_2099"
    }
    
    if(enemy_id is None):
        print("1. Lembuswana")
        print("2. Besukih")
        print("3. Leak")
        print("4. Ahool")
        print("5. Sembrani")
        chosen_enemy = input("What enemy do you want to fight ? ")
        enemy_id = gi_to_id.get(chosen_enemy)
    # char_data = open_json_to_dict("char_data.json")
    enemy_data = get_data_by_id(enemy_id, enemy_list)
    

    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]
    
    session_key = config.login_data["sessionkey"]
    
    parameters = [char_id,session_key]
    event_battle = send_amf_request("IndependenceEvent2025.getBattleData", parameters)
    
    print(event_battle['energy']," energy available for Independence Event fights.")

    for i in range(event_battle['energy']):
        print(f"Starting Independence event Fight ")
        agility = StatManager.calculate_stats_with_data("agility", char_data)
        enemy_attr = "id:"+enemy_id+"|hp:"+str(enemy_data['hp'])+"|agility:"+str(enemy_data['agility'])    
        # boss_attr = "id:ene_2112|hp:30000|agility:150"

        hash_input = str(char_id) + str(enemy_id) + enemy_attr + str(agility)
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, agility, enemy_attr, mission_hash, session_key]

        event_battle_data = send_amf_request("IndependenceEvent2025.startBattle", parameters)
        
        time.sleep(10)

        battle_dmg = random.randint(5000, 10000)

        hash_input = str(char_id) + str(enemy_id) + event_battle_data['code'] + str(battle_dmg) + battle_hash
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, event_battle_data['code'], battle_dmg, mission_hash, battle_hash, session_key]
        event_battle_result = send_amf_request("IndependenceEvent2025.finishBattle", parameters)
        
        if event_battle_result['status'] == 1:
            print(f"Successfully defeated Independence Event","Gained xp: ",event_battle_result['result'][0],"Gained Gold: ",event_battle_result['result'][1])
    print("Finished fighting Independence Event. No energy left")