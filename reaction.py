import pydirectinput as pdi
from time import sleep


class Reaction:
    def __init__(self, settings):
        self.verification_time = settings.data["reaction_speed"]
        self.reaction_time = settings.data["reaction_time"]
        self.reaction_strength = settings.data["reaction_strength"]

        self.eq_width = 300
        self.eq_height = 300

    def take_fish(self):
        pdi.rightClick()
        pdi.moveRel(
            None,
            self.reaction_strength,
            self.reaction_time,
            relative=True,
            attempt_pixel_perfect=True,
            disable_mouse_acceleration=True,
        )
        sleep(0.2)
        pdi.moveRel(
            None,
            -self.reaction_strength,
            self.reaction_time,
            relative=True,
            attempt_pixel_perfect=True,
            disable_mouse_acceleration=True,
        )
        sleep(1)
        pdi.rightClick()

    def calculate_skull_position(self, loc):
        # to do
        x, y = loc
        return x, y

    def bypass_verification(self, x, y):
        pdi.press("e")
        sleep(0.2)
        pdi.moveRel(
            x,
            y,
            relative=True,
            attempt_pixel_perfect=True,
            disable_mouse_acceleration=True,
        )
