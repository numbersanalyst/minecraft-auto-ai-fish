import pydirectinput as pdi
from time import sleep


class Reaction:
    def __init__(self, settings):
        self.verification_time = settings.data["reaction_speed"]
        self.reaction_time = settings.data["reaction_time"]
        self.reaction_strength = settings.data["reaction_strength"]

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

    def calculate_skull_position(self, loc, eq_half_w):
        x, y = loc

        mid = eq_half_w - 20
        x = x - mid
        y = y + 20

        return x, y

    def open_inventory(self):
        pdi.press("e")
        sleep(0.2)
        pdi.moveRel(None, -5, relative=True)

    def bypass_verification(self, x, y):
        pdi.moveRel(
            x,
            y,
            relative=True,
            attempt_pixel_perfect=True,
        )
        pdi.click()
