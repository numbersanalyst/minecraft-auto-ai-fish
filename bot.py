from multiprocessing import Process
from multiprocessing import freeze_support
from detection import Detector
from time import sleep


class Bot:
    def __init__(self, settings):
        """Initialize the bot values."""
        freeze_support()  # To prevent spawning multiple main processes

        self.detection = False
        self.reaction = False
        self.verification = False

        self.detection_ctrl = Detector(settings, self)

        self.settings = settings

    def toggle_detection(self):
        """Toggles the detection process."""
        self.detection = not self.detection
        if self.detection:
            # Start the detection process
            self.detection_process = Process(target=self.start_detection)
            self.detection_process.start()
        elif self.detection_process.is_alive():
            # Stop the detection process
            self.detection_ctrl.destroy_window()
            self.detection_process.terminate()

    def start_detection(self):
        """Detection process."""
        self.detection_ctrl.create_window()
        while True:
            self.detection_ctrl.detect_bobber()
            wait_time = float(self.settings.data["detection_interval"])
            sleep(wait_time)
