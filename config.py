from configparser import ConfigParser
import os


class Settings:
    """Settings class for the bot."""

    def __init__(self):
        """Initialize the settings."""
        self.config = ConfigParser()
        self.data = self.config["DEFAULT"]  # alias

        self.load()

    def get_capture_size(self):
        """Convert data about capture_size from string to tuple."""
        self.capture_size = tuple(map(int, self.data["capture_size"].split(", ")))

    def load(self):
        """Load the settings from the config file or create a new one."""
        if not os.path.exists("config.ini"):
            self.create_default_config()
        self.config.read("config.ini")
        self.get_capture_size()

    def create_default_config(self):
        """Create a new config file with default settings."""
        self.config["DEFAULT"] = {
            "capture_size": "150, 150, 150, 150",
            "detection_threshold": 0.6,
            "detection_interval": 0.2,
            "reaction_time": 0.35,
            "reaction_speed": 1,
            "reaction_strength": 300,
        }
        self.save()

    def save(self):
        """Save the settings to the config file."""
        with open("config.ini", "w") as f:
            self.config.write(f)
        self.get_capture_size()
