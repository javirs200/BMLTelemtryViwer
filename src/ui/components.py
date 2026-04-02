import tkinter as tk
from .theme import COLORS, FONTS, SPACING


class StyledButton(tk.Button):
    """Custom styled button."""
    def __init__(self, parent, text="", style="primary", **kwargs):
        style_config = {
            "primary": {
                "bg": COLORS["accent_blue"],
                "fg": COLORS["bg_dark"],
                "activebackground": COLORS["accent_cyan"],
                "activeforeground": COLORS["bg_dark"],
                "font": FONTS["body"],
                "bd": 0,
                "padx": SPACING["md"],
                "pady": SPACING["sm"],
                "cursor": "hand2",
                "relief": "flat",
            },
            "secondary": {
                "bg": COLORS["bg_tertiary"],
                "fg": COLORS["text_primary"],
                "activebackground": COLORS["accent_blue"],
                "activeforeground": COLORS["bg_dark"],
                "font": FONTS["body"],
                "bd": 1,
                "borderwidth": 1,
                "padx": SPACING["md"],
                "pady": SPACING["sm"],
                "cursor": "hand2",
                "relief": "solid",
            },
            "danger": {
                "bg": COLORS["accent_red"],
                "fg": COLORS["text_primary"],
                "activebackground": COLORS["danger"],
                "activeforeground": COLORS["text_primary"],
                "font": FONTS["body"],
                "bd": 0,
                "padx": SPACING["md"],
                "pady": SPACING["sm"],
                "cursor": "hand2",
                "relief": "flat",
            },
        }
        config = style_config.get(style, style_config["primary"])
        config.update(kwargs)
        super().__init__(parent, text=text, **config)


class StyledLabel(tk.Label):
    """Custom styled label."""
    def __init__(self, parent, text="", style="body", **kwargs):
        style_config = {
            "header": {
                "font": FONTS["header"],
                "fg": COLORS["accent_cyan"],
                "bg": COLORS["bg_dark"],
            },
            "title": {
                "font": FONTS["title"],
                "fg": COLORS["accent_blue"],
                "bg": COLORS["bg_dark"],
            },
            "subtitle": {
                "font": FONTS["subtitle"],
                "fg": COLORS["text_primary"],
                "bg": COLORS["bg_dark"],
            },
            "body": {
                "font": FONTS["body"],
                "fg": COLORS["text_primary"],
                "bg": COLORS["bg_dark"],
            },
            "muted": {
                "font": FONTS["small"],
                "fg": COLORS["text_muted"],
                "bg": COLORS["bg_dark"],
            },
        }
        config = style_config.get(style, style_config["body"])
        config.update(kwargs)
        super().__init__(parent, text=text, **config)


class StyledFrame(tk.Frame):
    """Custom styled frame."""
    def __init__(self, parent, style="default", **kwargs):
        style_config = {
            "default": {"bg": COLORS["bg_dark"]},
            "secondary": {"bg": COLORS["bg_secondary"]},
            "tertiary": {"bg": COLORS["bg_tertiary"]},
            "card": {
                "bg": COLORS["bg_tertiary"],
                "relief": "flat",
                "bd": 1,
                "highlightbackground": COLORS["accent_blue"],
                "highlightthickness": 1,
            },
        }
        config = style_config.get(style, style_config["default"])
        config.update(kwargs)
        super().__init__(parent, **config)


class Card(StyledFrame):
    """Reusable card component."""
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, style="card", **kwargs)
        
        if title:
            title_label = StyledLabel(self, text=title, style="subtitle")
            title_label.pack(padx=SPACING["md"], pady=(SPACING["md"], SPACING["sm"]), anchor="w")
        
        self.content_frame = StyledFrame(self, style="tertiary")
        self.content_frame.pack(fill="both", expand=True, padx=SPACING["sm"], pady=SPACING["sm"])
    
    def add_content(self, widget):
        """Add widget to card content."""
        widget.pack(in_=self.content_frame, fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])
        return widget
