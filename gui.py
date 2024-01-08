import tkinter as tk
from tkinter import ttk
import sv_ttk

# Example data
detection = 0
reaction = 0
verification = 1

def create_gui(root):
    root.title("Auto Fishing AI")
    root.geometry("350x430")
    root.resizable(False, False)
    root.grid_columnconfigure((0, 1), weight=1)

    sv_ttk.set_theme("dark")

    status_frame = ttk.LabelFrame(root, text="Buttons, but use keyboard instead.")
    status_frame.grid(
        row=0, column=0, padx=10, pady=(10, 0), ipady=3, columnspan=2, sticky="nsew"
    )

    status_frame.grid_columnconfigure((0, 1), weight=1)

    detection_btn = ttk.Button(
        status_frame,
        text="Detection (i): " + ("Active" if detection else "Inactive"),
    )

    reaction_btn = ttk.Button(
        status_frame,
        text="Reaction (o): " + ("Active" if reaction else "Inactive"),
    )

    style = ttk.Style()
    style.configure('active.TButton', 
                foreground = 'lightblue')

    verification_btn = ttk.Button(
        status_frame,
        text="Verification (p): "
        + ("Active" if verification else "Inactive"),
        style=("active.TButton" if verification else "active.TButton"),
    )

    detection_btn.grid(row=0, column=0, columnspan=2, padx=4, pady=(0, 5), sticky="ew")
    reaction_btn.grid(row=1, column=0)
    verification_btn.grid(row=1, column=1)

    settings_frame = ttk.Frame(root)
    settings_frame.grid(
        row=1, column=0, padx=10, pady=(10, 10), columnspan=2, sticky="nsew", ipady=30
    )

    settings_frame.grid_columnconfigure((0, 1), weight=1)
    settings_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    # Labels for settings
    capture_label = ttk.Label(settings_frame, text="Capture Size:")
    threshold_label = ttk.Label(settings_frame, text="Detection threshold:")
    interval_label = ttk.Label(settings_frame, text="Detection interval:")
    reaction_threshold_label = ttk.Label(settings_frame, text="Reaction threshold:")
    reaction_speed_label = ttk.Label(settings_frame, text="Reaction speed:")
    reaction_strength_label = ttk.Label(settings_frame, text="Reaction strength:")

    # Input fields for settings
    capture_input = ttk.Entry(
        settings_frame, justify="center", textvariable=CAPTURE_SIZE
    )
    threshold_input = ttk.Entry(
        settings_frame, justify="center", textvariable=THRESHOLD
    )
    interval_input = ttk.Entry(settings_frame, justify="center", textvariable=INTERVAL)
    reaction_threshold_input = ttk.Entry(
        settings_frame, justify="center", textvariable=REACTION_TIME_THRESHOLD
    )
    reaction_speed_input = ttk.Entry(
        settings_frame, justify="center", textvariable=REACTION_SPEED
    )
    reaction_strength_input = ttk.Entry(
        settings_frame, justify="center", textvariable=REACTION_STRENGTH
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

    def update_settings():
        pass

    # Button to apply settings changes
    apply_button = ttk.Button(root, text="Apply Settings", command=update_settings)
    apply_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")


if __name__ == "__main__":
    root = tk.Tk()

    # Example data
    CAPTURE_SIZE = tk.StringVar(root, value="150, 150, 150, 150")
    THRESHOLD = tk.DoubleVar(root, value="0.6")
    INTERVAL = tk.DoubleVar(root, value="0.25")
    REACTION_TIME_THRESHOLD = tk.DoubleVar(root, value="0.35")
    REACTION_SPEED = tk.DoubleVar(root, value="0.5")
    REACTION_STRENGTH = tk.DoubleVar(root, value="0.5")

    create_gui(root)
    root.mainloop()
