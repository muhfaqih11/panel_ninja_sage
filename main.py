import os
import json
import time
import keyboard
from typing import Dict, Any, Optional, List

import config
import amf_req
from leveling import start_leveling
from resources import download_all_resources
from utils import save_to_json, open_json_to_dict
from eudemon import fight_eudemon_boss
from cd_event import fight_cd_event, fight_pumpkin_event, fight_yinyang_event, fight_gi_event
from event_finisher import event_finisher


class NinjaSageApp:
    def __init__(self):
        self.QUICK_LOGIN_FILE = 'quick_login.json'
        self.running = True
    
    def check_game_version(self) -> bool:
        """Check if game version is compatible"""
        config.game_data = amf_req.check_version()
        if config.game_data.get("status") != 1:
            print("Game version not matched, wait for the panel update")
            return False
        return True
    
    def display_welcome(self):
        """Display welcome message"""
        print("==== Panel Ninja Sage by robot0011 ===")
        print("")
    
    def quick_login_exists(self) -> bool:
        """Check if quick login data exists"""
        return os.path.exists(self.QUICK_LOGIN_FILE)
    
    def load_quick_login(self) -> Optional[Dict[str, str]]:
        """Load quick login data from file"""
        try:
            with open(self.QUICK_LOGIN_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def save_quick_login(self, username: str, password: str):
        """Save login credentials for quick login"""
        login_data = {"username": username, "password": password}
        save_to_json(login_data, "quick_login")
    
    def perform_login(self, username: str, password: str) -> bool:
        """Perform login and validate credentials"""
        config.login_data = amf_req.login(
            username, 
            password, 
            config.game_data["__"], 
            str(int(config.game_data["_"]))
        )
        return config.login_data.get('status') == 1
    
    def handle_login(self) -> bool:
        """Handle the login process"""
        print("Login Page")
        print("1: Quick login")
        print("2: Login")
        
        while True:
            try:
                login_method = int(input("Enter your login method: "))
            except ValueError:
                print("Please enter a valid number (1 or 2)")
                continue
            
            if login_method == 1:
                login_data = self.load_quick_login()
                if login_data:
                    username = login_data["username"]
                    password = login_data["password"]
                    if self.perform_login(username, password):
                        return True
                    else:
                        print("Quick login failed. Please try manual login.")
                else:
                    print("No quick login data found. Please use login method 2 to login first.")
            
            elif login_method == 2:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                
                if self.perform_login(username, password):
                    self.save_quick_login(username, password)
                    return True
                else:
                    print("Invalid username or password. Please try again.")
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    def select_character(self):
        """Handle character selection"""
        print("")
        print("List of your characters:")
        config.all_char = amf_req.get_all_characters()
        
        if not config.all_char:
            print("No characters found!")
            return False
        
        
        while True:
            try:
                chosen_character = int(input("Choose your character: "))
                if 1 <= chosen_character <= len(config.all_char):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(config.all_char)}")
            except ValueError:
                print("Please enter a valid number")
        
        # Get the selected character data
        selected_char = config.all_char[chosen_character-1]
        config.char_data = amf_req.get_character_data(selected_char)
        
        if not config.char_data:
            print("Failed to load character data!")
            return False
            
        self.display_character_info()
        return True
    
    def display_character_info(self):
        """Display current character information"""
        if not config.char_data or "character_data" not in config.char_data:
            print("No character data available!")
            return
            
        char_data = config.char_data["character_data"]
        print("")
        print("Ninja Character Data:")
        print(f"Name: {char_data.get('character_name', 'Unknown')} || "
              f"Exp: {char_data.get('character_xp', 0)} || "
              f"Gold: {char_data.get('character_gold', 0)} || "
              f"Token: Lu miskin")
        print("")
    
    def show_main_menu(self):
        """Display the main menu options"""
        print("What do you want to do?")
        print("")
        print("1. Start Leveling")
        print("2. Fight Eudemon Boss")
        print("3. Fight CD Event Boss")
        print("4. Fight Pumpkin Event Boss")
        print("5. Fight Yin Yang Event Boss")
        print("6. Fight Independence Event Boss")
        print("7. Event Finisher")
        print("8. See character details")
        print("9. Exit")

    def handle_user_action(self, action: int):
        """Handle user menu selection"""
        action_handlers = {
            1: (start_leveling, "Starting Leveling... press q to stop levelling"),
            2: (fight_eudemon_boss, "Starting Eudemon Boss Fight... press q to stop fighting"),
            3: (fight_cd_event, "Starting CD Event Boss Fight... press q to stop fighting"),
            4: (fight_pumpkin_event, "Starting Pumpkin Event Fight... press q to stop fighting"),
            5: (fight_yinyang_event, "Starting Yin Yang event Fight... press q to stop fighting"),
            6: (fight_gi_event, "Starting Independence event Fight... press q to stop fighting"),
            7: (event_finisher, "Starting Event Finisher... press q to stop fighting"),
            8: (self.display_character_info, ""),
            9: (self.exit_app, "Exiting...")
        }
        
        if action in action_handlers:
            handler, message = action_handlers[action]
            
            if message:
                print("")
                print(message)
            
            if action == 8:
                handler()
            else:
                handler()
        else:
            print("Invalid choice. Please try again.")
        
        print("\n")
    
    def exit_app(self):
        """Exit the application"""
        self.running = False
    
    def run(self):
        """Main application loop"""
        if not self.check_game_version():
            return
        
        self.display_welcome()
        
        # Download resources if needed
        # download_all_resources()
        
        if not self.handle_login():
            return
        
        if not self.select_character():
            return
        
        while self.running:
            self.show_main_menu()
            
            try:
                action = int(input("Enter your choice: "))
                self.handle_user_action(action)
            except ValueError:
                print("Please enter a valid number")
                print("\n")
            except KeyboardInterrupt:
                print("\n\nApplication interrupted by user. Exiting...")
                self.exit_app()


def main():
    app = NinjaSageApp()
    app.run()


if __name__ == "__main__":
    main()