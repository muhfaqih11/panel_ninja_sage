from utils import send_amf_request, flatten_json, get_data_by_id, StatManager, CUCSG,open_json_to_dict
import time
import keyboard
import config

mission_list = open_json_to_dict("data/mission.json")
enemy_list = open_json_to_dict("data/enemy.json")
battle_hash = "eyJpdGVtcyI6eyJhY2Nlc3NvcnkiOiJhY2Nlc3NvcnlfMDEiLCJiYWNrX2l0ZW0iOiJiYWNrXzAxIiwid2VhcG9uIjoid3BuXzAxIiwic2V0Ijoic2V0XzAxXzAifSwic3RhdHVzIjp7ImVhcnRoIjowLCJmaXJlIjowLCJ3YXRlciI6MCwibGlnaHRuaW5nIjowLCJ3aW5kIjowfSwiYnl0ZXMiOnsiXyI6ODIyODQ0NywiX18iOjgyMjg0NDcsIl9fXyI6IjE3NjI3NDY2NTk0MDM2N2MzY2M5OTlhOWY5ZTk1MWExZDMzMjExNTQ1Yjg0YjJkNWE2MzkzM2IwMDIwNDMzMDAwYzNiYjQxMGZiMTc2Mjc0NjY1OTE3NjI3NDY2NTkxNzYyNzQ2NjU5MTc2Mjc0NjY1OSIsIl9fX19fIjo4MjI4NDQ3LCJfX19fX18iOjgyMjg0NDcsIl9fX18iOjE3NjI3NDY2NTl9LCJfX19fIjpbeyJfIjoic2tpbGxfMTMiLCJfXyI6MjkxMzR9XX0="


def get_levelling_mission(char_level):
    prohibited_grades = ["daily", "tp", "ss", ""]
    if char_level <= 60:
        levelling_mission = [m for m in mission_list if m['level'] == char_level and m['grade'] not in prohibited_grades]
    else:
        levelling_mission = [m for m in mission_list if m['level'] == 60 and m['grade'] not in prohibited_grades]
    return levelling_mission[0] if levelling_mission else None


def build_enemy_attributes(mission_same_level):
    enemies = []
    enemy_attrs = []
    for enemy in mission_same_level['enemies']:
        enemy_attr = get_data_by_id(enemy, enemy_list)
        enemies.append(enemy)
        enemy_attrs.append(f"id:{enemy}|hp:{enemy_attr['hp']}|agility:{enemy_attr['agility']}")
    return enemies, "#".join(enemy_attrs)


def start_battle(mission_same_level, char_id, char_level, session_key):
    enemies, enemy_attrs = build_enemy_attributes(mission_same_level)
    agility = StatManager.calculate_stats_with_data("agility", flatten_json(config.char_data))

    hash_input = ",".join(enemies) + enemy_attrs + str(agility)
    mission_hash = CUCSG.hash(hash_input)

    parameters = [char_id, mission_same_level["id"], ",".join(enemies), enemy_attrs, agility, mission_hash, session_key]
    battle_id = send_amf_request("BattleSystem.startMission", parameters)

    time.sleep(1.5)
    return battle_id


def finish_battle(mission_id, char_id, battle_id, session_key):
    hash_input = f"{mission_id}{char_id}{battle_id}0"
    _loc2_ = CUCSG.hash(hash_input)

    parameters = [char_id, mission_id, battle_id, _loc2_, 0, session_key, battle_hash, 0]
    result = send_amf_request("BattleSystem.finishMission", parameters)

    return result


def process_mission(mission_same_level, char_level, char_id, session_key):
    mission_id = mission_same_level["id"]
    battle_id = start_battle(mission_same_level, char_id, char_level, session_key)
    result = finish_battle(mission_id, char_id, battle_id, session_key)

    if result["status"] == 1:
        print(f"Mission completed successfully! Gained Gold: {result['result'][0]} Gained EXP: {result['result'][1]} Current Level: {result['level']}")
        return result['level']
    return char_level


def start_leveling(loop_times=None):
    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]
    char_level = char_data["character_data_character_level"]
    session_key = config.login_data["sessionkey"]

    if loop_times is None:
        while True:
            if keyboard.is_pressed('q'):
                print("Stopping the levelling...")
                break

            mission_same_level = get_levelling_mission(char_level)

            char_level = process_mission(mission_same_level, char_level, char_id, session_key)
    else:
        for i in range(loop_times):

            if keyboard.is_pressed('q'):
                print("Stopping the levelling...")
                break

            mission_same_level = get_levelling_mission(char_level)

            char_level = process_mission(mission_same_level, char_level, char_id, session_key)
