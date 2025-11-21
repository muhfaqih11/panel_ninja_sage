from event import fight_cd_event, fight_pumpkin_event, fight_yinyang_event, fight_gi_event, EventBattleSystem
from leveling import start_leveling
import time
from shadow_war import shadow_war_event
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import config


class EventFinisherConfigDialog:
    """Popup dialog to configure event finisher targets"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Event Finisher Configuration")
        self.dialog.geometry("600x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (700 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.create_widgets()
        # self.independence_targets = {
        #     "ene_2104": 0,
        #     "ene_2105": 0,
        #     "ene_2106": 0,
        #     "ene_2103": 0,
        #     "ene_2102": 0
        # }
    
    def create_widgets(self):
        """Create the configuration form widgets"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Event Finisher Configuration", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(main_frame, 
                               text="Set the number of kills for each enemy. Events will run until all targets are completed.",
                               font=('Arial', 10), wraplength=550, justify=tk.LEFT)
        instructions.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # CD Event Tab
        cd_frame = ttk.Frame(notebook, padding=10)
        notebook.add(cd_frame, text="CD Event")
        self.create_cd_tab(cd_frame)
        
        # Pumpkin Event Tab
        pumpkin_frame = ttk.Frame(notebook, padding=10)
        notebook.add(pumpkin_frame, text="Pumpkin Event")
        self.create_pumpkin_tab(pumpkin_frame)
        
        # Yin Yang Event Tab
        yinyang_frame = ttk.Frame(notebook, padding=10)
        notebook.add(yinyang_frame, text="Yin Yang Event")
        self.create_yinyang_tab(yinyang_frame)
        
        # # Independence Event Tab
        # independence_frame = ttk.Frame(notebook, padding=10)
        # notebook.add(independence_frame, text="Independence Event")
        # self.create_independence_tab(independence_frame)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        start_btn = ttk.Button(button_frame, text="Start Event Finisher", 
                              command=self.start_event_finisher)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", 
                               command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Load default values
        self.load_defaults()
    
    def create_cd_tab(self, parent):
        """Create CD Event configuration"""
        tk.Label(parent, text="Confronting Death Event", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        # CD event has only one boss
        cd_frame = ttk.Frame(parent)
        cd_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(cd_frame, text="CD Boss Kills:").pack(side=tk.LEFT)
        self.cd_target = tk.IntVar(value=0)
        cd_spinbox = ttk.Spinbox(cd_frame, from_=0, to=10000, textvariable=self.cd_target, width=10)
        cd_spinbox.pack(side=tk.LEFT, padx=10)
    
    def create_pumpkin_tab(self, parent):
        """Create Pumpkin Event configuration"""
        tk.Label(parent, text="Pumpkin Event Enemies", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        # Pumpkin enemies with descriptions
        pumpkin_enemies = [
            ("ene_2104", "Pumpkin Minion"),
            ("ene_2105", "Skeleton Ninja"), 
            ("ene_2106", "Zombie Samurai"),
            ("ene_2103", "Headless Pumpkin Horseman"),
            ("ene_2102", "Cursed Pumpkin King")
        ]
        
        self.pumpkin_targets = {}
        
        for enemy_id, enemy_name in pumpkin_enemies:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=3)
            
            tk.Label(frame, text=f"{enemy_name} ({enemy_id}):", width=30, anchor=tk.W).pack(side=tk.LEFT)
            var = tk.IntVar(value=0 if enemy_id == "ene_2104" else 
                          0 if enemy_id in ["ene_2105", "ene_2106"] else 0)
            spinbox = ttk.Spinbox(frame, from_=0, to=10000, textvariable=var, width=10)
            spinbox.pack(side=tk.LEFT, padx=10)
            
            self.pumpkin_targets[enemy_id] = var
    
    def create_yinyang_tab(self, parent):
        """Create Yin Yang Event configuration"""
        tk.Label(parent, text="Yin Yang Event Enemies", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        yinyang_enemies = [
            ("ene_2100", "Yin Tiger"),
            ("ene_2101", "Yang Dragon")
        ]
        
        self.yinyang_targets = {}
        
        for enemy_id, enemy_name in yinyang_enemies:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=3)
            
            tk.Label(frame, text=f"{enemy_name} ({enemy_id}):", width=30, anchor=tk.W).pack(side=tk.LEFT)
            var = tk.IntVar(value=0)
            spinbox = ttk.Spinbox(frame, from_=0, to=10000, textvariable=var, width=10)
            spinbox.pack(side=tk.LEFT, padx=10)
            
            self.yinyang_targets[enemy_id] = var
    
    def create_independence_tab(self, parent):
        """Create Independence Event configuration"""
        tk.Label(parent, text="Independence Event Enemies", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        independence_enemies = [
            ("ene_2095", "Lembuswana"),
            ("ene_2096", "Besukih"),
            ("ene_2097", "Leak"),
            ("ene_2098", "Ahool"),
            ("ene_2099", "Sembrani")
        ]
        
        self.independence_targets = {}
        
        for enemy_id, enemy_name in independence_enemies:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=3)
            
            tk.Label(frame, text=f"{enemy_name} ({enemy_id}):", width=30, anchor=tk.W).pack(side=tk.LEFT)
            var = tk.IntVar(value=140)
            spinbox = ttk.Spinbox(frame, from_=0, to=10000, textvariable=var, width=10)
            spinbox.pack(side=tk.LEFT, padx=10)
            
            self.independence_targets[enemy_id] = var
    
    def load_defaults(self):
        """Load default values"""
        # Default values are already set in the variable initialization
    
    def start_event_finisher(self):
        """Start event finisher with configured targets"""
        # Validate that at least one target is set
        total_targets = (self.cd_target.get() + 
                        sum(var.get() for var in self.pumpkin_targets.values()) +
                        sum(var.get() for var in self.yinyang_targets.values())
                        # sum(var.get() for var in self.independence_targets.values())
                        )
        
        if total_targets == 0:
            messagebox.showwarning("No Targets", "Please set at least one target kill count.")
            return
        
        # Prepare the targets dictionary
        pumpkin_target = {enemy_id: var.get() for enemy_id, var in self.pumpkin_targets.items() if var.get() > 0}
        yinyang_target = {enemy_id: var.get() for enemy_id, var in self.yinyang_targets.items() if var.get() > 0}
        # independence_target = {enemy_id: var.get() for enemy_id, var in self.independence_targets.items() if var.get() > 0}
        cd_target = self.cd_target.get()
        
        # Close dialog
        self.dialog.destroy()
        
        # Start event finisher in a separate thread
        threading.Thread(target=run_event_finisher, 
                        args=(pumpkin_target, yinyang_target, cd_target),
                        daemon=True).start()


def run_event_finisher(pumpkin_target, yinyang_target ,cd_target):
    """Run the event finisher with the given targets"""
    system = EventBattleSystem()
    
    # Create working copies of targets (so we can track progress)
    pumpkin_remaining = pumpkin_target.copy()
    yinyang_remaining = yinyang_target.copy()
    # independence_remaining = independence_target.copy()
    cd_remaining = cd_target
    
    # Main event loop
    print("\n" + "="*50)
    print("Starting event battles with configured targets...")
    print("="*50)
    
    while True:
        # Check stop event
        if hasattr(config, 'stop_event') and config.stop_event.is_set():
            print("Event finisher stopped by user")
            break
            
        # Check if all targets are completed
        all_completed = (
            cd_remaining <= 0 and
            not pumpkin_remaining and 
            not yinyang_remaining
            # not independence_remaining
        )
        
        if all_completed:
            print("\n✓ All configured enemies have been defeated!")
            break
        
        # CD Event
        if cd_remaining > 0:
            energy = system.check_energy("cd")
            print(f"\nCD Event Energy: {energy}")
            while energy > 0 and cd_remaining > 0:
                # Check stop event
                if hasattr(config, 'stop_event') and config.stop_event.is_set():
                    break
                    
                print(f"Fighting CD boss ({cd_remaining} kills remaining)")
                fight_cd_event(num_loops=1)
                cd_remaining -= 1
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
                # Check stop event
                if hasattr(config, 'stop_event') and config.stop_event.is_set():
                    break
                    
                # Get first enemy from remaining targets
                enemy_id = next(iter(pumpkin_remaining))
                kills_left = pumpkin_remaining[enemy_id]
                print(f"Fighting Pumpkin enemy {enemy_id} ({kills_left} kills remaining)")
                fight_pumpkin_event(enemy_id=enemy_id, num_loops=1)
                pumpkin_remaining[enemy_id] -= 1
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
                # Check stop event
                if hasattr(config, 'stop_event') and config.stop_event.is_set():
                    break
                    
                enemy_id = next(iter(yinyang_remaining))
                kills_left = yinyang_remaining[enemy_id]
                print(f"Fighting Yin-Yang enemy {enemy_id} ({kills_left} kills remaining)")
                fight_yinyang_event(enemy_id=enemy_id, num_loops=1)
                yinyang_remaining[enemy_id] -= 1
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
        # if independence_remaining:
        #     energy = system.check_energy("independence")
        #     print(f"\nIndependence Event Energy: {energy}")
        #     while energy > 0 and independence_remaining:
        #         # Check stop event
        #         if hasattr(config, 'stop_event') and config.stop_event.is_set():
        #             break
                    
        #         enemy_id = next(iter(independence_remaining))
        #         kills_left = independence_remaining[enemy_id]
        #         print(f"Fighting Independence enemy {enemy_id} ({kills_left} kills remaining)")
        #         fight_gi_event(enemy_id=enemy_id, num_loops=1)
        #         independence_remaining[enemy_id] -= 1
        #         if independence_remaining[enemy_id] <= 0:
        #             del independence_remaining[enemy_id]
        #             print(f"✓ Enemy {enemy_id} target completed!")
        #         if not independence_remaining:
        #             print("✓ All Independence targets completed!")
        #             break
        #         # Re-check energy for next iteration
        #         energy = system.check_energy("independence")
        #     if energy <= 0 and independence_remaining:
        #         print("⚠ No energy left for Independence event")
        
        # Check if all targets are completed before leveling
        all_completed_check = (
            cd_remaining <= 0 and
            not pumpkin_remaining and 
            not yinyang_remaining
            # not independence_remaining
        )
        
        # Check stop event before starting leveling
        if hasattr(config, 'stop_event') and config.stop_event.is_set():
            break
            
        if not all_completed_check:
            print("\nStarting leveling session...")
            # shadow_war_event()
            # start_leveling(20)  # Reduced from 1920 for testing
            start_leveling(1200)
        else:
            print("\nAll targets completed! Skipping leveling.")
    
    # Clear stop event when finished
    if hasattr(config, 'stop_event'):
        config.stop_event.clear()


def event_finisher():
    """Main event finisher function that shows configuration popup"""
    # Get the main window from config if available, or create a temporary one
    try:
        parent_window = config.main_window
    except AttributeError:
        # If no main window in config, create a temporary root
        parent_window = tk.Tk()
        parent_window.withdraw()  # Hide the temporary window
    
    # Show configuration dialog
    dialog = EventFinisherConfigDialog(parent_window)
    
    # If we created a temporary window, destroy it after dialog closes
    if not hasattr(config, 'main_window'):
        parent_window.destroy()