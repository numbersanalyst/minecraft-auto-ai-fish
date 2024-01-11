from multiprocessing import Process


class Bot:
    def __init__(self):
        self.detection = False
        self.reaction = False
        self.verification = False

    def toggle_detection(self):
        self.detection = not self.detection
        if self.detection:
            self.detection_process = Process(target=self.start_detection)
            self.detection_process.start()
        elif self.detection_process.is_alive():
            self.detection_process.terminate()

    def start_detection(self):
        pass
