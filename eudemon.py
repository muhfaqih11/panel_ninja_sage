from utils import send_amf_request, save_to_json, open_json_to_dict , flatten_json, get_data_by_id, StatManager, CUCSG, save_fight_data
import struct
from typing import List
import config
import time
import keyboard

gamedata = open_json_to_dict("data/gamedata.json")
battle_hash = config.BATTLE_HASH


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
            if(eudemon_boss_battle_data['status']!=1):
                print("finished due to error")
                break
            # print(eudemon_boss_battle_data)
            battle_id = eudemon_boss_battle_data['code']
            time.sleep(30)
            _loc2_ = CUCSG.hash(str(b['num']) + str(char_id) + battle_id)

            parameters = [char_id, b['num'], battle_id, _loc2_, session_key, battle_hash]

            eudemon_boss_battle_result = send_amf_request("EudemonGarden.finishHunting", parameters)
            save_fight_data(eudemon_boss_battle_result)

            if eudemon_boss_battle_result['status'] == 1:
                print(f"Successfully defeated boss","Gained xp: ",eudemon_boss_battle_result['result'][0],"Gained Gold: ",eudemon_boss_battle_result['result'][1])
        else:
            continue  # Only executed if inner loop didn't break
        break  # Break outer loop if inner loop broke
    print("Finished fighting available Eudemon bosses.")
    print("")





