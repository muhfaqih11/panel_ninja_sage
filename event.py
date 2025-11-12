from utils import (
    send_amf_request, 
    flatten_json, 
    get_data_by_id, 
    StatManager, 
    CUCSG, 
    save_fight_data,
    open_json_to_dict
)
import config
import time
import sys
from typing import Optional, Dict, Tuple
from dataclasses import dataclass

BATTLE_HASH = config.BATTLE_HASH


@dataclass
class EventConfig:
    """Configuration for event battle systems."""
    name: str
    api_class: str
    enemy_choices: Dict[str, Tuple[str, str]]
    is_fixed_boss: bool = False
    boss_id: Optional[str] = None
    boss_hp: Optional[int] = None
    boss_agility: Optional[int] = None
    
    def get_battle_data_method(self) -> str:
        return f"{self.api_class}.getBattleData"
    
    def get_start_battle_method(self) -> str:
        return f"{self.api_class}.startBattle"
    
    def get_finish_battle_method(self) -> str:
        return f"{self.api_class}.finishBattle"


class EventBattleSystem:
    """Unified system for handling all event battles."""
    
    EVENT_CONFIGS = {
        "cd": EventConfig(
            name="Confronting Death Event",
            api_class="ConfrontingDeathEvent2025",
            enemy_choices={},
            is_fixed_boss=True,
            boss_id="ene_2112",
            boss_hp=30000,
            boss_agility=150
        ),
        "pumpkin": EventConfig(
            name="Pumpkin Event",
            api_class="HalloweenEvent2025",
            enemy_choices={
                "1": ("ene_2104", "Pumpkin Minion"),
                "2": ("ene_2105", "Skeleton Ninja"),
                "3": ("ene_2106", "Zombie Samurai"),
                "4": ("ene_2103", "Headless Pumpkin Horseman"),
                "5": ("ene_2102", "Cursed Pumpkin King"),
            }
        ),
        "yinyang": EventConfig(
            name="Yin Yang Event",
            api_class="YinYangEvent",
            enemy_choices={
                "1": ("ene_2100", "Yin Tiger"),
                "2": ("ene_2101", "Yang Dragon"),
            }
        ),
        "independence": EventConfig(
            name="Independence Event",
            api_class="IndependenceEvent2025",
            enemy_choices={
                "1": ("ene_2095", "Lembuswana"),
                "2": ("ene_2096", "Besukih"),
                "3": ("ene_2097", "Leak"),
                "4": ("ene_2098", "Ahool"),
                "5": ("ene_2099", "Sembrani"),
            }
        ),
    }
    
    def __init__(self):
        self.enemy_list = open_json_to_dict("data/enemy.json")
    
    @staticmethod
    def _get_character_data() -> Tuple[dict, str, str]:
        """Get character data and session info."""
        char_data = flatten_json(config.char_data)
        char_id = char_data["character_data_character_id"]
        session_key = config.login_data["sessionkey"]
        return char_data, char_id, session_key
    
    @staticmethod
    def _check_hack_detection(result: dict, initial_tokens: int) -> None:
        """Check for hack detection and exit if detected."""
        if result.get('account_tokens', float('inf')) < initial_tokens:
            print("Hack detected, exit system immediately")
            sys.exit()
    
    def _prompt_enemy_selection(self, event_config: EventConfig, battle_data: dict = None) -> str:
        """Prompt user to select an enemy."""
        print(f"Choose your enemy to fight:")
        
        for num, (enemy_id, enemy_name) in event_config.enemy_choices.items():
            kill_count = ""
            if battle_data:
                # Try to get kill count from various possible keys
                if 'kill_counts' in battle_data:
                    kill_count = f" ({battle_data['kill_counts'].get(enemy_id, 0)} kills)"
                elif 'yin_kills' in battle_data and enemy_id == "ene_2100":
                    kill_count = f" ({battle_data['yin_kills']} kills)"
                elif 'yang_kills' in battle_data and enemy_id == "ene_2101":
                    kill_count = f" ({battle_data['yang_kills']} kills)"
            
            print(f"{num}. {enemy_name}{kill_count}")
        
        choice = input("What enemy do you want to fight? ")
        enemy_id, _ = event_config.enemy_choices.get(choice, (None, None))
        return enemy_id
    
    def _create_battle_hash(self, char_id: str, enemy_id: str, 
                           battle_code: str, damage: int) -> str:
        """Create battle hash for validation."""
        hash_input = f"{char_id}{enemy_id}{battle_code}{damage}{BATTLE_HASH}"
        return CUCSG.hash(hash_input)
    
    def _execute_battle(self, char_data: dict, char_id: str, session_key: str,
                       enemy_id: str, enemy_data: dict, event_config: EventConfig) -> dict:
        """Execute a single battle."""
        agility = StatManager.calculate_stats_with_data("agility", char_data)
        enemy_attr = f"id:{enemy_id}|hp:{enemy_data['hp']}|agility:{enemy_data['agility']}"
        
        # Start battle
        hash_input = f"{char_id}{enemy_id}{enemy_attr}{agility}"
        mission_hash = CUCSG.hash(hash_input)
        parameters = [char_id, enemy_id, agility, enemy_attr, mission_hash, session_key]
        
        battle_data = send_amf_request(event_config.get_start_battle_method(), parameters)
        
        time.sleep(10)
        
        # Finish battle
        battle_dmg = 0
        mission_hash = self._create_battle_hash(char_id, enemy_id, battle_data['code'], battle_dmg)
        parameters = [char_id, enemy_id, battle_data['code'], battle_dmg, 
                     mission_hash, BATTLE_HASH, session_key]
        
        result = send_amf_request(event_config.get_finish_battle_method(), parameters)
        save_fight_data(result)
        
        return result
    def check_energy(self,event_type):

        if event_type not in self.EVENT_CONFIGS:
            raise ValueError(f"Unknown event type: {event_type}. "
                           f"Available: {', '.join(self.EVENT_CONFIGS.keys())}")
        event_config = self.EVENT_CONFIGS[event_type]
        _ , char_id, session_key = self._get_character_data()
        parameters = [char_id, session_key]
        battle_data = send_amf_request(event_config.get_battle_data_method(), parameters)
        return battle_data.get('energy', 0)
    
    def fight_event(self, event_type: str, enemy_id: Optional[str] = None, 
                    num_loops: Optional[int] = None) -> None:
        """
        Generic event fight handler for all event types.
        
        Args:
            event_type: Type of event ('cd', 'pumpkin', 'yinyang', 'independence')
            enemy_id: Optional enemy ID to fight (if None, user will be prompted)
            num_loops: Number of battles to execute (if None, uses all available energy)
        """
        if event_type not in self.EVENT_CONFIGS:
            raise ValueError(f"Unknown event type: {event_type}. "
                           f"Available: {', '.join(self.EVENT_CONFIGS.keys())}")
        
        event_config = self.EVENT_CONFIGS[event_type]
        char_data, char_id, session_key = self._get_character_data()
        
        # Get battle data
        parameters = [char_id, session_key]
        battle_data = send_amf_request(event_config.get_battle_data_method(), parameters)
        
        available_energy = battle_data.get('energy', 0)
        print(f"{available_energy} energy available for {event_config.name} fights.")
        
        if available_energy == 0:
            print(f"No energy left for {event_config.name}.")
            return
        
        # Determine number of battles to execute
        if num_loops is None:
            battles_to_execute = available_energy
        else:
            if num_loops <= 0:
                print(f"⚠️  WARNING: Number of loops must be positive. Requested: {num_loops}")
                return
            
            if num_loops > available_energy:
                print(f"⚠️  WARNING: Requested {num_loops} battles but only {available_energy} energy available.")
                print(f"Cannot proceed. Please reduce the number of loops or wait for energy to regenerate.")
                return
            
            battles_to_execute = num_loops
            print(f"Will execute {battles_to_execute} out of {available_energy} available battles.")
        
        # Handle fixed boss events (CD Event)
        if event_config.is_fixed_boss:
            enemy_id = event_config.boss_id
            enemy_data = {
                'hp': event_config.boss_hp,
                'agility': event_config.boss_agility
            }
        else:
            # Select enemy for regular events
            if enemy_id is None:
                enemy_id = self._prompt_enemy_selection(event_config, battle_data)
            
            if not enemy_id:
                print("Invalid enemy selection.")
                return
            
            enemy_data = get_data_by_id(enemy_id, self.enemy_list)
        
        # Execute battles
        successful_battles = 0
        for i in range(battles_to_execute):
            initial_tokens = config.all_char['tokens']
            print(f"\nStarting {event_config.name} Fight {i+1}/{battles_to_execute}")
            
            result = self._execute_battle(char_data, char_id, session_key, 
                                         enemy_id, enemy_data, event_config)
            
            if result.get('status') == 1:
                successful_battles += 1
                print(f"✓ Successfully defeated {event_config.name} enemy | "
                      f"XP: {result['result'][0]} | Gold: {result['result'][1]}")
                self._check_hack_detection(result, initial_tokens)
            else:
                print(f"✗ Battle failed with status: {result.get('status')}")
        
        remaining_energy = available_energy - battles_to_execute
        print(f"\n{'='*60}")
        print(f"Finished {event_config.name}:")
        print(f"  • Battles executed: {successful_battles}/{battles_to_execute}")
        print(f"  • Remaining energy: {remaining_energy}")
        print(f"{'='*60}")


# Convenience functions for backward compatibility
def fight_cd_event(num_loops: Optional[int] = None):
    """Fight Confronting Death Event."""
    system = EventBattleSystem()
    system.fight_event("cd", num_loops=num_loops)


def fight_pumpkin_event(enemy_id: Optional[str] = None, num_loops: Optional[int] = None):
    """Fight Pumpkin/Halloween Event."""
    system = EventBattleSystem()
    system.fight_event("pumpkin", enemy_id, num_loops)


def fight_yinyang_event(enemy_id: Optional[str] = None, num_loops: Optional[int] = None):
    """Fight Yin Yang Event."""
    system = EventBattleSystem()
    system.fight_event("yinyang", enemy_id, num_loops)


def fight_gi_event(enemy_id: Optional[str] = None, num_loops: Optional[int] = None):
    """Fight Independence Event."""
    system = EventBattleSystem()
    system.fight_event("independence", enemy_id, num_loops)

    "cd","pumpkin","yinyang","independence"