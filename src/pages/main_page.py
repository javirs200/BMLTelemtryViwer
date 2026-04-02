import tkinter as tk
from src.ui import StyledLabel, StyledButton, StyledFrame, COLORS, FONTS, SPACING


class MainPage(tk.Frame):
    """Main landing list page with modern dark theme."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_dark"])
        self.controller = controller
        self.scrollable_frame = None
        self._build_ui()
    
    def _build_ui(self):
        """Build the main page UI."""
        # Header bar
        header_frame = StyledFrame(self, style="secondary")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_title = StyledLabel(header_frame, text="✈ BML Telemetry Viewer", style="header")
        header_title.pack(side="left", padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Button frame on the right
        button_frame = StyledFrame(header_frame, style="secondary")
        button_frame.pack(side="right", padx=SPACING["lg"], pady=SPACING["md"])
        
        refresh_btn = StyledButton(button_frame, text="🔄 Refresh", style="secondary", command=self._refresh_landings)
        refresh_btn.pack(side="left", padx=SPACING["sm"])
        
        close_btn = StyledButton(button_frame, text="✕", style="danger", command=self.controller.root.quit, width=3)
        close_btn.pack(side="left", padx=SPACING["sm"])
        
        # Subtitle
        subtitle = StyledLabel(self, text="Flight Plans & Landings Dashboard", style="muted")
        subtitle.pack(padx=SPACING["lg"], pady=(SPACING["md"], 0), anchor="w")
        
        # Main content
        content_frame = StyledFrame(self, style="default")
        content_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Scrollable landing list
        canvas = tk.Canvas(content_frame, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview, bg=COLORS["bg_secondary"])
        self.scrollable_frame = StyledFrame(canvas, style="default")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        self.canvas = canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate initial landings
        self._populate_landings()
    
    def _populate_landings(self):
        """Populate the landings list with responsive wrapping layout."""
        # Group landings by date
        landings_by_date = {}
        for landing in self.controller.landings:
            ts = landing.get('timestamp_zulu', '')
            date_key = ts[:10] if ts else 'Unknown'
            if date_key not in landings_by_date:
                landings_by_date[date_key] = []
            landings_by_date[date_key].append(landing)
        
        # Display date groups
        for date_key in sorted(landings_by_date.keys(), reverse=True):
            date_label = StyledLabel(self.scrollable_frame, text=f"📅 {date_key}", style="subtitle")
            date_label.pack(padx=SPACING["md"], pady=(SPACING["lg"], SPACING["sm"]), anchor="w")
            
            landings_list = landings_by_date[date_key]
            card_width = 180  # Fixed card width
            max_cards_per_row = 4  # Maximum cards per row
            
            # Create rows of cards
            for row_idx in range(0, len(landings_list), max_cards_per_row):
                row_frame = StyledFrame(self.scrollable_frame, style="default")
                row_frame.pack(padx=SPACING["md"], pady=(0, SPACING["lg"]), fill="x")
                
                row_landings = landings_list[row_idx:row_idx + max_cards_per_row]
                
                for landing in row_landings:
                    time_str = landing.get('timestamp_zulu', 'N/A')[11:19]
                    vs_fpm = int(landing.get('touchdown_fpm', 0))
                    aircraft = landing.get('aircraft_title', 'Unknown').split()[0]
                    
                    card_frame = StyledFrame(row_frame, style="card")
                    card_frame.pack(side="left", fill="both", expand=True, padx=SPACING["sm"], pady=SPACING["sm"])
                    
                    # Limit card width and height
                    card_frame.config(width=card_width, height=90)
                    card_frame.pack_propagate(False)
                    
                    # Card content
                    time_label = StyledLabel(card_frame, text=time_str, style="title")
                    time_label.pack(padx=SPACING["md"], pady=(SPACING["md"], 0))
                    
                    vs_label = StyledLabel(card_frame, text=f"{vs_fpm} fpm", style="muted")
                    vs_label.pack(padx=SPACING["md"], pady=(0, SPACING["sm"]))
                    
                    aircraft_label = StyledLabel(card_frame, text=aircraft, style="small")
                    aircraft_label.pack(padx=SPACING["md"], pady=(0, SPACING["md"]))
                    
                    # Make card clickable
                    for widget in [card_frame, time_label, vs_label, aircraft_label]:
                        widget.bind("<Button-1>", lambda e, l=landing: self.controller.select_landing(l))
                        widget.config(cursor="hand2")
    
    def _refresh_landings(self):
        """Reload landings from disk."""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Reload from disk
        self.controller._load_landings()
        
        # Repopulate the list
        self._populate_landings()
    
    def refresh(self):
        """Refresh page when navigating back."""
        pass
