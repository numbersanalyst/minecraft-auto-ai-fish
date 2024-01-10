import tkinter as tk
from tkinter import ttk
import sv_ttk


class App(tk.Tk):
    """GUI class for the bot."""

    def __init__(self, settings, bot):
        """Create the app."""
        super().__init__()
        self.settings = settings
        self.get_status(bot)

        self._base_set_up()
        self._get_values()
        self._create_gui()

    def get_status(self, bot):
        """Get the status of the bot."""
        self.detection = bot.detection

        self.reaction_var = tk.BooleanVar(value=bot.reaction)
        self.verification_var = tk.BooleanVar(value=bot.verification)

    def _base_set_up(self):
        """Set up the base settings for the GUI."""
        sv_ttk.set_theme("dark")
        self.title("Auto Fishing AI")
        self.geometry("350x430")
        self.resizable(False, False)

        self.grid_columnconfigure((0, 1), weight=1)

        self.style = ttk.Style()
        self.style.configure("active.TButton", foreground="red")

    def _get_values(self):
        """Get the values from the settings."""
        self.tk_capture_size = tk.StringVar(
            self, value=self.settings.data["capture_size"]
        )
        self.tk_detection_threshold = tk.StringVar(
            self, value=self.settings.data["detection_threshold"]
        )
        self.tk_detection_interval = tk.StringVar(
            self, value=self.settings.data["detection_interval"]
        )
        self.tk_reaction_time = tk.StringVar(
            self, value=self.settings.data["reaction_time"]
        )
        self.tk_reaction_speed = tk.StringVar(
            self, value=self.settings.data["reaction_speed"]
        )
        self.tk_reaction_strenght = tk.StringVar(
            self, value=self.settings.data["reaction_strength"]
        )

    def update_values(self):
        """Update the values in the settings."""
        self.settings.data["capture_size"] = self.tk_capture_size.get()
        self.settings.data["detection_threshold"] = self.tk_detection_threshold.get()
        self.settings.data["detection_interval"] = self.tk_detection_interval.get()
        self.settings.data["reaction_time"] = self.tk_reaction_time.get()
        self.settings.data["reaction_speed"] = self.tk_reaction_speed.get()
        self.settings.data["reaction_strength"] = self.tk_reaction_strenght.get()
        self.settings.save()

    def update_btn_text(self):
        """Update the text and style in the button."""
        self.detection_btn["text"] = (
            "Start script (i)" if not self.detection else "Stop script (i)"
        )
        self.detection_btn["style"] = "active.TButton" if self.detection else ""

    def _create_gui(self):
        """Create the GUI."""

        # STATUS BUTTONS
        status_frame = ttk.LabelFrame(self, text="Buttons, but use keyboard instead.")
        status_frame.grid(
            row=0, column=0, padx=10, pady=(10, 0), ipady=3, columnspan=2, sticky="nsew"
        )

        status_frame.grid_columnconfigure((0, 1), weight=1)

        # self for change the style while button is pressed
        self.detection_btn = ttk.Button(status_frame, command=bot.toggle_detection)
        self.reaction_btn = ttk.Checkbutton(
            status_frame, text="Reaction (o)", variable=self.reaction_var
        )
        self.verification_btn = ttk.Checkbutton(
            status_frame, text="Verification (v)", variable=self.verification_var
        )

        self.update_btn_text()

        self.detection_btn.grid(
            row=0, column=0, columnspan=2, padx=10, pady=(5, 5), sticky="ew"
        )
        self.reaction_btn.grid(row=1, column=0)
        self.verification_btn.grid(row=1, column=1)

        # SETTINGS
        settings_frame = ttk.Frame(self)
        settings_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=(10, 10),
            columnspan=2,
            sticky="nsew",
            ipady=30,
        )

        settings_frame.grid_columnconfigure((0, 1), weight=1)
        settings_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Labels for settings
        capture_label = ttk.Label(settings_frame, text="Capture size:")
        threshold_label = ttk.Label(settings_frame, text="Detection threshold:")
        interval_label = ttk.Label(settings_frame, text="Detection interval:")
        reaction_threshold_label = ttk.Label(settings_frame, text="Reaction time:")
        reaction_speed_label = ttk.Label(settings_frame, text="Reaction speed:")
        reaction_strength_label = ttk.Label(settings_frame, text="Reaction strength:")

        # Input fields for settings
        capture_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_capture_size
        )
        threshold_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_detection_threshold
        )
        interval_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_detection_interval
        )
        reaction_threshold_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_reaction_time
        )
        reaction_speed_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_reaction_speed
        )
        reaction_strength_input = ttk.Entry(
            settings_frame, justify="center", textvariable=self.tk_reaction_strenght
        )

        # Layout with grid
        capture_label.grid(row=0, column=0)
        threshold_label.grid(row=1, column=0)
        interval_label.grid(row=2, column=0)
        reaction_threshold_label.grid(row=4, column=0)
        reaction_speed_label.grid(row=5, column=0)
        reaction_strength_label.grid(row=6, column=0)

        separator = ttk.Separator(settings_frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        capture_input.grid(row=0, column=1)
        threshold_input.grid(row=1, column=1)
        interval_input.grid(row=2, column=1)
        reaction_threshold_input.grid(row=4, column=1)
        reaction_speed_input.grid(row=5, column=1)
        reaction_strength_input.grid(row=6, column=1)

        # Button to apply settings changes
        apply_button = ttk.Button(
            self, text="Apply Settings", command=self.update_values
        )
        apply_button.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew"
        )


if __name__ == "__main__":
    # Create settings
    from config import Settings

    settings = Settings()

    from bot import Bot

    bot = Bot()

    # Create the app
    app = App(settings, bot)
    app.mainloop()
