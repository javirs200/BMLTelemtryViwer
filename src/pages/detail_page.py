import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.ui import StyledLabel, StyledButton, StyledFrame, Card, COLORS, FONTS, SPACING


class DetailPage(tk.Frame):
    """Detail page with landing data and charts - modern dark theme."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_dark"])
        self.controller = controller
        self._build_static_ui()
    
    def _build_static_ui(self):
        """Build the static UI structure."""
        # Header
        header_frame = StyledFrame(self, style="secondary")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_title = StyledLabel(header_frame, text="🛬 Landing Details", style="header")
        header_title.pack(side="left", padx=SPACING["lg"], pady=SPACING["lg"])
        
        back_btn = StyledButton(header_frame, text="← Back", style="secondary", command=self._go_back)
        back_btn.pack(side="right", padx=SPACING["md"], pady=SPACING["md"])
        
        # Content
        content_frame = StyledFrame(self, style="default")
        content_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Top row: Aircraft info + scores
        top_row = StyledFrame(content_frame, style="default")
        top_row.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Aircraft info card
        info_card = Card(top_row, title="✈ Aircraft Information")
        info_card.pack(side="left", fill="both", expand=True, padx=(0, SPACING["md"]))
        self.info_text = tk.Text(info_card.content_frame, height=10, width=30, bg=COLORS["bg_tertiary"], 
                                 fg=COLORS["text_primary"], font=FONTS["mono"], bd=0, relief="flat")
        self.info_text.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])
        
        # Scores card
        score_card = Card(top_row, title="📊 Landing Scores")
        score_card.pack(side="right", fill="both", expand=True, padx=(SPACING["md"], 0))
        self.score_text = tk.Text(score_card.content_frame, height=10, width=20, bg=COLORS["bg_tertiary"],
                                  fg=COLORS["text_primary"], font=FONTS["mono"], bd=0, relief="flat")
        self.score_text.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])
        
        # Chart card
        chart_card = Card(self, title="📈 Flight Profile")
        chart_card.pack(fill="both", expand=True, pady=(SPACING["lg"], 0))
        
        self.canvas_frame = StyledFrame(chart_card.content_frame, style="tertiary")
        self.canvas_frame.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])
    
    def _go_back(self):
        """Navigate back to main page."""
        from src.pages.main_page import MainPage
        self.controller.show_frame(MainPage)
    
    def refresh(self):
        """Refresh and display landing data."""
        if self.controller.current_landing:
            landing = self.controller.current_landing
            
            # Update aircraft info
            self.info_text.config(state="normal")
            self.info_text.delete(1.0, tk.END)
            
            info_str = f"""Aircraft: {landing.get('aircraft_title', 'N/A')}
Time: {landing.get('timestamp_zulu', 'N/A')}

Airport: {landing.get('airport_icao', 'N/A')}
Runway: {landing.get('runway_ident', 'N/A')}

Approach Altitude: {landing.get('position', {}).get('alt_ft_msl', 'N/A')} ft
Touchdown Speed: {landing.get('touchdown_ias_kt', 'N/A')} kt
Ground Speed: {landing.get('touchdown_groundspeed_kt', 'N/A')} kt
"""
            self.info_text.insert(1.0, info_str)
            self.info_text.config(state="disabled")
            
            # Update scores
            self.score_text.config(state="normal")
            self.score_text.delete(1.0, tk.END)
            
            max_g = landing.get('max_g', 0)
            g_color = "✓" if max_g < 2 else "⚠" if max_g < 3 else "✗"
            
            bounce = landing.get('bounce_count', 0)
            bounce_color = "✓" if bounce == 0 else "⚠" if bounce < 3 else "✗"
            
            score_str = f"""{g_color} Max G: {max_g}
{bounce_color} Bounces: {bounce}

Sideslip: {landing.get('touchdown_sideslip_deg', 'N/A')}°
Radio Alt: {landing.get('touchdown_radio_alt_ft', 'N/A')} ft
Descent Rate: {landing.get('touchdown_fpm', 'N/A')} fpm
"""
            self.score_text.insert(1.0, score_str)
            self.score_text.config(state="disabled")
            
            # Draw chart
            self._draw_chart(landing)
    
    def _draw_chart(self, landing):
        """Draw dual-axis chart with landing profile."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLORS["bg_tertiary"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS["bg_dark"])
        
        # Extract touchdown_profile data
        touchdown_profile = landing.get('touchdown_profile', [])
        if touchdown_profile:
            tp_time = [point.get('t_ms', 0) / 1000 for point in touchdown_profile]
            tp_vs = [point.get('vertical_speed_fpm', 0) for point in touchdown_profile]
            ax.plot(tp_time, tp_vs, color=COLORS["accent_blue"], linewidth=2.5, 
                   label="Vertical Speed", marker='o', markersize=2, alpha=0.8)
            ax.fill_between(tp_time, tp_vs, alpha=0.1, color=COLORS["accent_blue"])
        
        # Extract rollout_track data
        rollout_track = landing.get('rollout_track', [])
        if rollout_track:
            rt_time = [point.get('t_ms', 0) / 1000 for point in rollout_track]
            rt_gs = [point.get('groundspeed_kt', 0) for point in rollout_track]
            ax2 = ax.twinx()
            ax2.plot(rt_time, rt_gs, color=COLORS["accent_orange"], linewidth=2.5,
                    label="Ground Speed", marker='s', markersize=2, alpha=0.8)
            ax2.set_ylabel("Ground Speed (kt)", color=COLORS["accent_orange"], fontweight="bold", fontsize=10)
            ax2.tick_params(axis='y', labelcolor=COLORS["accent_orange"])
            ax2.spines['right'].set_color(COLORS["accent_orange"])
            ax2.spines['left'].set_color(COLORS["accent_blue"])
            ax2.spines['top'].set_visible(False)
            ax2.spines['bottom'].set_color(COLORS["text_muted"])
            ax2.grid(True, alpha=0.2, color=COLORS["text_muted"])
        
        ax.set_xlabel("Time (s)", color=COLORS["text_primary"], fontweight="bold", fontsize=10)
        ax.set_ylabel("Vertical Speed (fpm)", color=COLORS["accent_blue"], fontweight="bold", fontsize=10)
        ax.tick_params(axis='y', labelcolor=COLORS["accent_blue"])
        ax.tick_params(axis='x', labelcolor=COLORS["text_primary"])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS["accent_blue"])
        ax.spines['bottom'].set_color(COLORS["text_muted"])
        
        # Legend
        lines1, labels1 = ax.get_legend_handles_labels()
        if rollout_track:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9, 
                     facecolor=COLORS["bg_secondary"], edgecolor=COLORS["text_muted"])
        else:
            ax.legend(lines1, labels1, loc="upper left", fontsize=9,
                     facecolor=COLORS["bg_secondary"], edgecolor=COLORS["text_muted"])
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
