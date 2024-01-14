from PIL import ImageGrab
from time import sleep, time
import pydirectinput as pdi
import numpy as np
import cv2 as cv

from reaction import Reaction


class Detect:
    def __init__(self, settings, bot):
        """Initialize the basic variables."""
        self.settings = settings
        self.bot = bot

        self.reaction = Reaction(settings)

        self.detected_time = time()

        self.eq_hsv = np.array([0, 0, 139])
        self.verification_hsv_main = np.array([180, 100, 66.7])
        self.verification_hsv_second = np.array([180, 100, 16.5])

        self.bobber_template = cv.imread("assets/bobber.png")
        self.skull_template = cv.imread("skull_human.png")
        self.skull_template = cv.cvtColor(self.skull_template, cv.COLOR_BGR2HSV)
        self.skull_template = cv.inRange(self.skull_template, self.eq_hsv, self.eq_hsv)
        self.skull_template = cv.blur(self.skull_template, (2, 2))

        self.bobber_w, self.bobber_h = (
            self.bobber_template.shape[1],
            self.bobber_template.shape[0],
        )
        self.skull_w, self.skull_h = (
            self.skull_template.shape[1],
            self.skull_template.shape[0],
        )

    def get_screen(self):
        """Captures the screen and returns it as an image."""
        x, y = pdi.position()
        img = cv.cvtColor(
            np.array(
                ImageGrab.grab(
                    bbox=(
                        x - self.settings.capture_size[0],
                        y - self.settings.capture_size[1],
                        x + self.settings.capture_size[2],
                        y + self.settings.capture_size[3],
                    )
                )
            ),
            cv.COLOR_RGB2BGR,
        )
        return img

    def detect(self, img):
        """Detect a bobber and return the image with a rectangle around the detected bobber."""
        res = cv.matchTemplate(img, self.bobber_template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)

        # Consider a match only if it exceeds the threshold
        if max_val >= float(self.settings.data["detection_threshold"]):
            self.detected_time = time()

            top_left = max_loc
            bottom_right = (
                top_left[0] + self.bobber_w,
                top_left[1] + self.bobber_h,
            )

            # Draw rectangle around the detected fish
            cv.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

        elif (
            time() - self.detected_time > float(self.settings.data["reaction_time"])
            and self.bot.reaction
        ):
            self.reaction.take_fish()

        return img

    def detect_skull(self, img):
        """Finds and draws a rectangle around the skull in the image. Returns image and the coordinates of the target."""
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_img, self.eq_hsv, self.eq_hsv)
        mask = cv.blur(mask, (2, 2))

        detection_result = cv.matchTemplate(
            mask, self.skull_template, cv.TM_CCOEFF_NORMED
        )
        _, max_val, _, max_loc = cv.minMaxLoc(detection_result)

        threshold = 0.8
        if max_val > threshold:
            top_left = max_loc
            bottom_right = (
                top_left[0] + self.skull_w,
                top_left[1] + self.skull_h,
            )
            cv.rectangle(img, top_left, bottom_right, (250, 0, 0), 2)

            return img, top_left

        return hsv_img, None

    def show_img(self, img):
        """Shows the image."""
        cv.imshow("image", img)
        cv.waitKey(5000)


if __name__ == "__main__":
    from config import Settings
    from bot import Bot

    settings = Settings()
    bot = Bot(settings)

    detection = Detect(settings, bot)

    img = detection.get_screen()

    res, top_left = detection.detect_skull(img)

    detection.show_img(res)
