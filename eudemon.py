from utils import send_amf_request, save_to_json, open_json_to_dict , flatten_json, get_data_by_id, StatManager, CUCSG
import struct
from typing import List
import config
import time
import keyboard

gamedata = open_json_to_dict("data/gamedata.json")
battle_hash = "eyJpdGVtcyI6eyJhY2Nlc3NvcnkiOiJhY2Nlc3NvcnlfMDQiLCJiYWNrX2l0ZW0iOiJiYWNrXzIyMDIiLCJ3ZWFwb24iOiJ3cG5fMjIxMyIsInNldCI6InNldF84MzFfMCJ9LCJfX19fIjpbeyJfIjoic2tpbGxfMDQiLCJfXyI6MjMzOTd9LHsiXyI6InNraWxsXzIzMDciLCJfXyI6NTQxMTR9LHsiXyI6InNraWxsXzAzIiwiX18iOjIyOTM0fSx7Il8iOiJza2lsbF82NTMiLCJfXyI6ODE1MTJ9LHsiXyI6InNraWxsXzE5NSIsIl9fIjo2NTczM30seyJfIjoic2tpbGxfMzE0IiwiX18iOjUyNjgxfSx7Il8iOiJza2lsbF8xODciLCJfXyI6NDc1Nzl9LHsiXyI6InNraWxsXzE2NCIsIl9fIjo1NDQ0NH1dLCJzdGF0dXMiOnsiZWFydGgiOjAsImxpZ2h0bmluZyI6MCwiZmlyZSI6MCwid2F0ZXIiOjAsIndpbmQiOjczfSwiYnl0ZXMiOnsiX19fIjoiMTc2Mjg0MzY2NjQwMzY3YzNjYzk5OWE5ZjllOTUxYTFkMzMyMTE1NDViODRiMmQ1YTYzOTMzYjAwMjA0MzMwMDBjM2JiNDEwZmIxNzYyODQzNjY2MTc2Mjg0MzY2NjE3NjI4NDM2NjYxNzYyODQzNjY2IiwiX19fX19fIjo4MjI4NDQ3LCJfIjo4MjI4NDQ3LCJfXyI6ODIyODQ0NywiX19fXyI6MTc2Mjg0MzY2NiwiX19fX18iOjgyMjg0NDd9fQ=="


def fight_eudemon_boss():

    char_data = flatten_json(config.char_data)
    char_id = char_data["character_data_character_id"]
    char_level = char_data["character_data_character_level"]
    session_key = config.login_data["sessionkey"]
    
    parameters = [session_key,char_id]
    available_bosses = send_amf_request("EudemonGarden.getData", parameters)['data']
    available_bosses = list(map(int, available_bosses.split(",")))

    boss = get_data_by_id("eudemon", gamedata)["data"]["bosses"]

    # Check if 'q' is pressed at the start of each iteration
    for b in boss:
        if keyboard.is_pressed('q'):
            print("Stopped by user")
            break
            
        if int(b['lvl']) > char_level:
            break
        for i in range(available_bosses[b['num']]):
            # Check for 'q' key press in inner loop too
            if keyboard.is_pressed('q'):
                print("Stopped by user")
                break
            print(f"Fighting boss: {b['name']} (Level: {b['lvl']})")
            parameters = [char_id, b['num'], session_key]
            eudemon_boss_battle_data = send_amf_request("EudemonGarden.startHunting", parameters)
            # print(eudemon_boss_battle_data)
            battle_id = eudemon_boss_battle_data['code']
            time.sleep(30)
            _loc2_ = CUCSG.hash(str(b['num']) + str(char_id) + battle_id)

            parameters = [char_id, b['num'], battle_id, _loc2_, session_key, battle_hash]

            eudemon_boss_battle_result = send_amf_request("EudemonGarden.finishHunting", parameters)
            
            if eudemon_boss_battle_result['status'] == 1:
                print(f"Successfully defeated boss","Gained xp: ",eudemon_boss_battle_result['result'][0],"Gained Gold: ",eudemon_boss_battle_result['result'][1])
        else:
            continue  # Only executed if inner loop didn't break
        break  # Break outer loop if inner loop broke
    print("Finished fighting available Eudemon bosses.")
    print("")





