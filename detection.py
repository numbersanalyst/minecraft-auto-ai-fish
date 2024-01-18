from PIL import ImageGrab
import pydirectinput as pdi
import numpy as np
import cv2 as cv
from time import time

from reaction import Reaction


class Detector:
    def __init__(self, settings, bot):
        """Initialize the basic variables."""
        self.settings = settings
        self.bot = bot

        self.reaction = Reaction(settings)

        self.detected_time = time()

        self.eq_hsv = np.array([0, 0, 139])
        self.verification_hsv_main = np.array([110, 130, 150])
        self.verification_hsv_second = np.array([180, 255, 255])

        self.bobber_template = cv.imread("assets/bobber.png")
        self.skull_template = cv.imread("assets/skull_human.png")
        self.skull_template = self.proccess_image_with_hsv(
            self.skull_template, self.eq_hsv
        )
        self.skull_template = cv.blur(self.skull_template, (2, 2))
        self.verification_template = cv.imread("assets/verification.png")
        self.verification_template = self.proccess_image_with_hsv(
            self.verification_template,
            self.verification_hsv_main,
            self.verification_hsv_second,
        )

        self.verification_half_w = 150
        self.verification_h = 100

        self.eq_half_w = 170
        self.eq_h = 120

    def get_screen(self, x1=None, y1=None, x2=None, y2=None):
        """Captures the screen and returns it as an image."""
        x, y = pdi.position()
        if x1:  # Use custom coordinates
            bbox = (x - x1, y - y1, x + x2, y + y2)
        else:  # Use coordinates from settings
            bbox = (
                x - self.settings.capture_size[0],
                y - self.settings.capture_size[1],
                x + self.settings.capture_size[2],
                y + self.settings.capture_size[3],
            )
        img = cv.cvtColor(
            np.array(ImageGrab.grab(bbox)),
            cv.COLOR_RGB2BGR,
        )
        return img

    def detect(
        self, img, template, threshold=0.8, hsv=False, hsv_max=False, blur=False
    ):
        """Finds and draws a rectangle around the template in the image. Returns image and position of the target."""
        org_img = img  # Original image for preview

        if isinstance(hsv, np.ndarray):
            if isinstance(hsv_max, np.ndarray):
                img = self.proccess_image_with_hsv(img, hsv, hsv_max)
            else:
                img = self.proccess_image_with_hsv(img, hsv)
        if blur:
            img = cv.blur(img, (2, 2))

        detection_result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(detection_result)

        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (
                top_left[0] + template.shape[1],
                top_left[1] + template.shape[0],
            )
            cv.rectangle(org_img, top_left, bottom_right, (250, 0, 0), 2)

            return org_img, top_left

        # If no match was found
        return org_img, None

    def proccess_image_with_hsv(self, img, hsv, hsv_max=None):
        """Process image with hsv filter"""
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        if isinstance(hsv_max, np.ndarray):
            img = cv.inRange(img, hsv, hsv_max)
        else:
            img = cv.inRange(img, hsv, hsv)

        return img

    def detect_bobber(self):
        """Detects a bobber and returns the image with a rectangle around it. Invokes reaction if necessary."""
        img = self.get_screen()
        res, top_left = self.detect(
            img, self.bobber_template, float(self.settings.data["detection_threshold"])
        )
        self.update_window(res)
        if top_left != None:
            self.detected_time = time()
        elif time() - self.detected_time > float(self.settings.data["reaction_time"]):
            if self.bot.reaction:
                self.reaction.take_fish()
                pdi.rightClick()
            if self.bot.verification:
                self.detect_verification()

    def detect_verification(self):
        """Detects a verification and returns the image with a rectangle around it. Invokes reaction if necessary."""
        img = self.get_screen(
            self.verification_half_w, self.verification_h, self.verification_half_w, 0
        )
        res, top_left = self.detect(
            img,
            self.verification_template,
            hsv=self.verification_hsv_main,
            hsv_max=self.verification_hsv_second,
        )
        self.update_window(res)
        if top_left != None:
            self.reaction.open_inventory()
            self.detect_skull()

    def detect_skull(self):
        """Detects a skull and returns the image with a rectangle around it. Invokes reaction if necessary."""
        img = self.get_screen(self.eq_half_w, 0, self.eq_half_w, self.eq_h)
        res, top_left = self.detect(
            img, self.skull_template, hsv=self.eq_hsv, blur=True
        )
        self.update_window(res)
        if top_left != None:
            x, y = self.reaction.calculate_skull_position(top_left, self.eq_half_w)
            self.reaction.bypass_verification(x, y)

    def create_window(self):
        """Creates the preview window."""
        cv.namedWindow("Preview", cv.WINDOW_NORMAL)

    def update_window(self, img):
        """Updates the window with the given image."""
        cv.imshow("Preview", img)
        cv.waitKey(1)

    def destroy_window(self):
        """Destroys the window."""
        cv.destroyAllWindows()
