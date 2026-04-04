import os
import json
import tkinter as tk
from tkinter import messagebox

from src.pages.main_page import MainPage
from src.pages.detail_page import DetailPage


class PageManager:
    """Manages page switching and landing data loading."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BML Telemetry Viewer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Load configuration
        self.config = self._load_config()
        
        # Configure grid
        self.container = tk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.current_landing = None
        self.landings = []
        
        self._load_landings()
        self._create_frames()
        self.show_frame(MainPage)
    
    def _load_config(self):
        """Load configuration from config.cfg."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.cfg')
        try:
            with open(config_path, 'r') as f:
                # Remove comments from JSON
                content = f.read()
                lines = [line.split('#')[0].rstrip() for line in content.split('\n')]
                clean_content = '\n'.join(lines)
                config = json.loads(clean_content)
                return config
        except Exception as e:
            messagebox.showwarning("Config Warning", f"Failed to load config.cfg , Using default settings.")
            return {}
    
    def _load_landings(self):
        """Load all landing JSON files from config location."""
        location = self.config.get('landingslocation')
        
        if not location:
            messagebox.showwarning("Warning", "Landings location not specified in config.cfg using default path.")

            # get base path ( documents folder )
            base_path = os.path.expanduser("~/Documents")

            # default path
            location = os.path.join(base_path, "BeatMyLanding", "Landings")

            return
        else:
            # check if relative path
            if not os.path.isabs(location):
                base_path = os.path.dirname(os.path.dirname(__file__))
                location = os.path.join(base_path, location)
            else:
                location = os.path.normpath(location)
            
        
        self.landings = []
        try:
            if not os.path.exists(location):
                messagebox.showwarning("Warning", f"Landing data path not found: {location}")
                return
                
            for root, dirs, files in os.walk(location):
                for file in sorted(files):
                    if file.endswith('.json'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r') as f:
                                data = json.load(f)
                                self.landings.append(data)
                        except Exception as e:
                            print(f"Error loading {filepath}: {e}")
            self.landings.sort(key=lambda x: x.get('timestamp_zulu', ''), reverse=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load landings: {e}")
    
    def _create_frames(self):
        """Create all page frames."""
        for F in (MainPage, DetailPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, cont):
        """Display a frame."""
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()
    
    def select_landing(self, landing):
        """Select a landing and navigate to detail."""
        self.current_landing = landing
        self.show_frame(DetailPage)
