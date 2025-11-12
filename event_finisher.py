# from event import fight_cd_event, fight_pumpkin_event, fight_yinyang_event, fight_gi_event, EventBattleSystem
# from leveling import start_leveling
# import time

# def event_finisher():
#     system = EventBattleSystem()
#     print(system.check_energy("cd"))
#     # times_loop = int(input("How many times you want to complete your event : "))
#     # gi_to_id = {
#     #     "1": "ene_2095",
#     #     "2": "ene_2096",
#     #     "3": "ene_2097",
#     #     "4": "ene_2098",
#     #     "5": "ene_2099"
#     # }
#     # yinyang_number_to_id = {
#     #     "1": "ene_2100",
#     #     "2": "ene_2101",
#     # }
#     # pumpkin_number_to_id = {
#     #     "1": "ene_2104",
#     #     "2": "ene_2105",
#     #     "3": "ene_2106",
#     #     "4": "ene_2103",
#     #     "5": "ene_2102"
#     # }
#     # print("Choose your enemy to fight:")
#     # print("1. Pumpkin Minion")
#     # print("2. Skeleton Ninja")
#     # print("3. Zombie Samurai")
#     # print("4. Headless Pumpkin Horseman")
#     # print("5. Cursed Pumpkin King")

#     # p_enemy = input("What enemy do you want to fight ? ")
#     # p_enemy_id = pumpkin_number_to_id.get(p_enemy)
#     # print("")
#     # print("Choose your enemy to fight:")
#     # print("1. Yin Tiger")
#     # print("2. Yang Dragon")

#     # y_enemy = input("What enemy do you want to fight ? ")
#     # y_enemy_id = yinyang_number_to_id.get(y_enemy)
#     # print("")
#     # print("Choose your enemy to fight:")
#     # print("1. Lembuswana")
#     # print("2. Besukih")
#     # print("3. Leak")
#     # print("4. Ahool")
#     # print("5. Sembrani")

#     # gi_enemy = input("What enemy do you want to fight ? ")
#     # gi_enemy_id = gi_to_id.get(gi_enemy)

#     # enemy_list = ["ene_2112",p_enemy_id,y_enemy_id,gi_enemy_id]

#     # for i in range(times_loop):
#     #     print("doing event")
#     #     fight_cd_event()
#     #     fight_pumpkin_event(enemy_list[1])
#     #     fight_yinyang_event(enemy_list[2])
#     #     fight_gi_event(enemy_list[3])
#     #     start_leveling(3200)


#     # print("All selected event bosses have been fought. Restarting the cycle...")


from event import fight_cd_event, fight_pumpkin_event, fight_yinyang_event, fight_gi_event, EventBattleSystem
from leveling import start_leveling
import time

def event_finisher():
    system = EventBattleSystem()
    
    # Configure your targets here
    pumpkin_target = {
        "ene_2104": 1,  # Pumpkin Minion - 10 times
        "ene_2105": 1    # Skeleton Ninja - 5 times
    }
    
    yinyang_target = {
        "ene_2100": 1,  # Yin Tiger - 15 times
        "ene_2101": 1   # Yang Dragon - 10 times
    }
    
    independence_target = {
        "ene_2095": 1,  # Lembuswana - 20 times
        "ene_2097": 1   # Leak - 15 times
    }
    
    cd_target = 1  # CD event - 30 times (only 1 enemy)
    
    # Create working copies of targets (so we can track progress)
    pumpkin_remaining = pumpkin_target.copy()
    yinyang_remaining = yinyang_target.copy()
    independence_remaining = independence_target.copy()
    cd_remaining = cd_target
    
    # Main event loop
    print("\n" + "="*50)
    print("Starting event battles...")
    print("="*50)
    
    while True:
        # Check if all targets are completed
        all_completed = (
            cd_remaining <= 0 and
            not pumpkin_remaining and 
            not yinyang_remaining and 
            not independence_remaining
        )
        
        if all_completed:
            print("\n✓ All configured enemies have been defeated!")
            break
        
        battles_performed = False
        
        # CD Event
        if cd_remaining > 0:
            energy = system.check_energy("cd")
            print(f"\nCD Event Energy: {energy}")
            while energy > 0 and cd_remaining > 0:
                print(f"Fighting CD boss ({cd_remaining} kills remaining)")
                fight_cd_event(num_loops=1)
                cd_remaining -= 1
                battles_performed = True
                if cd_remaining <= 0:
                    print("✓ CD event target completed!")
                    break
                # Re-check energy for next iteration
                energy = system.check_energy("cd")
            if energy <= 0 and cd_remaining > 0:
                print("⚠ No energy left for CD event")
        
        # Pumpkin Event
        if pumpkin_remaining:
            energy = system.check_energy("pumpkin")
            print(f"\nPumpkin Event Energy: {energy}")
            while energy > 0 and pumpkin_remaining:
                # Get first enemy from remaining targets
                enemy_id = next(iter(pumpkin_remaining))
                kills_left = pumpkin_remaining[enemy_id]
                print(f"Fighting Pumpkin enemy {enemy_id} ({kills_left} kills remaining)")
                fight_pumpkin_event(enemy_id=enemy_id, num_loops=1)
                pumpkin_remaining[enemy_id] -= 1
                battles_performed = True
                if pumpkin_remaining[enemy_id] <= 0:
                    del pumpkin_remaining[enemy_id]
                    print(f"✓ Enemy {enemy_id} target completed!")
                if not pumpkin_remaining:
                    print("✓ All Pumpkin targets completed!")
                    break
                # Re-check energy for next iteration
                energy = system.check_energy("pumpkin")
            if energy <= 0 and pumpkin_remaining:
                print("⚠ No energy left for Pumpkin event")
        
        # Yin-Yang Event
        if yinyang_remaining:
            energy = system.check_energy("yinyang")
            print(f"\nYin-Yang Event Energy: {energy}")
            while energy > 0 and yinyang_remaining:
                enemy_id = next(iter(yinyang_remaining))
                kills_left = yinyang_remaining[enemy_id]
                print(f"Fighting Yin-Yang enemy {enemy_id} ({kills_left} kills remaining)")
                fight_yinyang_event(enemy_id=enemy_id, num_loops=1)
                yinyang_remaining[enemy_id] -= 1
                battles_performed = True
                if yinyang_remaining[enemy_id] <= 0:
                    del yinyang_remaining[enemy_id]
                    print(f"✓ Enemy {enemy_id} target completed!")
                if not yinyang_remaining:
                    print("✓ All Yin-Yang targets completed!")
                    break
                # Re-check energy for next iteration
                energy = system.check_energy("yinyang")
            if energy <= 0 and yinyang_remaining:
                print("⚠ No energy left for Yin-Yang event")
        
        # Independence Event
        if independence_remaining:
            energy = system.check_energy("independence")
            print(f"\nIndependence Event Energy: {energy}")
            while energy > 0 and independence_remaining:
                enemy_id = next(iter(independence_remaining))
                kills_left = independence_remaining[enemy_id]
                print(f"Fighting Independence enemy {enemy_id} ({kills_left} kills remaining)")
                fight_gi_event(enemy_id=enemy_id, num_loops=1)
                independence_remaining[enemy_id] -= 1
                battles_performed = True
                if independence_remaining[enemy_id] <= 0:
                    del independence_remaining[enemy_id]
                    print(f"✓ Enemy {enemy_id} target completed!")
                if not independence_remaining:
                    print("✓ All Independence targets completed!")
                    break
                # Re-check energy for next iteration
                energy = system.check_energy("independence")
            if energy <= 0 and independence_remaining:
                print("⚠ No energy left for Independence event")
        
        # Leveling between battles if any battle was performed
        if battles_performed:
            # Check if all targets are completed
            all_completed_check = (
                cd_remaining <= 0 and
                not pumpkin_remaining and 
                not yinyang_remaining and 
                not independence_remaining
            )
            
            if not all_completed_check:
                print("\nStarting leveling session (waiting for 3200 energy)...")
                start_leveling(3200)
            else:
                print("\nAll targets completed! Skipping leveling.")
        
        # Check if we're out of energy for all events but targets remain
        if not battles_performed:
            print("\n⚠ Out of energy for all events but targets remain.")
            print("Waiting for energy regeneration...")
            time.sleep(300)  # Wait 5 minutes before checking again


if __name__ == "__main__":
    event_finisher()