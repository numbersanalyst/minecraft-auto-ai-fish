from multiprocessing import Process

class Bot:
    def __init__(self):
        self.detection = False
        self.reaction = False
        self.verification = False
    
    def toggle_detection(self):
        self.detection = not self.detection
        if self.detection:
            self.detection_process = Process(target=start_detection)
        elif self.detection.is_alive():
            self.detection_process.terminate()

    def toggle_reaction(self):
        self.reaction = not self.reaction
        if self.reaction:
            self.reaction_process = Process(target=start_reaction)
        elif self.reaction.is_alive():
            self.reaction_process.terminate()

    def toogle_verification(self):
        self.verification = not self.verification
        if self.verification:
            self.verification_process = Process(target=start_verification)
        elif self.verification.is_alive():
            self.verification_process.terminate()

    def start_detection(self):
        pass

    def start_reaction(self):
        pass
    
    def start_verification(self):
        pass
    