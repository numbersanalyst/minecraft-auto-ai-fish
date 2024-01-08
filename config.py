from configparser import ConfigParser
import os


class Settings:
    """Settings class for the bot."""

    def __init__(self):
        """Initialize the settings."""
        self.config = ConfigParser()
        self.data = self.config["DEFAULT"] # alias
        self.load()

    def load(self):
        """Load the settings from the config file or create a new one."""
        if not os.path.exists("config.ini"):
            self.create_default_config()
        self.config.read("config.ini")

    def create_default_config(self):
        """Create a new config file with default settings."""
        self.config["DEFAULT"] = {
            "capture_size": (150, 150, 150, 150),
            "detection_threshold": 0.6,
            "detection_interval": 0.25,
            "reaction_time": 0.35,
            "reaction_speed": 0.5,
            "reaction_strength": 0.5,
        }
        self.save()

    def save(self):
        """Save the settings to the config file."""
        with open("config.ini", "w") as f:
            self.config.write(f)


if __name__ == "__main__":
    settings = Settings()
