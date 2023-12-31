import cv2 as cv
import numpy as np
from PIL import ImageGrab
import pydirectinput as pdi
from time import sleep, time
import keyboard
import os
from colorama import Fore, Style, just_fix_windows_console, init

# Settings
capture_size = 150
threshold = 0.6
interval = 0.25
detection = False
reaction = True
template = cv.imread("bobber_full.png")
detected_time = time()


def setup_colorama():
    just_fix_windows_console()
    init(autoreset=True)


def toggle_script():
    global detection
    detection = not detection
    # Mesage to user
    print(
        Style.DIM + "Script loop is now",
        Fore.GREEN + "active." if detection else Fore.RED + "inactive.",
    )


def takeFish():
    print("Taking fish!")  # Mesage to user
    pdi.rightClick()
    pdi.moveRel(None, 380, 0.25, relative=True, disable_mouse_acceleration=True)
    sleep(0.2)
    pdi.moveRel(None, -380, 0.25, relative=True, disable_mouse_acceleration=True)
    sleep(1)
    pdi.rightClick()
    sleep(3)


if __name__ == "__main__":
    setup_colorama()

    keyboard.add_hotkey("p", toggle_script)  # Press p to toggle the script
    keyboard.add_hotkey("o", lambda: os._exit(0))  # Press o to quit

    print(Style.BRIGHT + "Minecraft Auto Fishing AI Script for Mausaa")
    print(Style.DIM + "Press p to toggle the script.")
    print(Style.DIM + "Press o to quit program.")
    print()

    while True:
        if detection:
            x, y = pdi.position()
            img = cv.cvtColor(
                np.array(
                    ImageGrab.grab(
                        bbox=(
                            x - capture_size,
                            y - capture_size,
                            x + capture_size,
                            y + capture_size,
                        )
                    )
                ),
                cv.COLOR_RGB2BGR,
            )

            res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)

            # Detect
            if reaction:
                if np.sum(loc) != 0:
                    detected_time = time()
                else:
                    if time() - detected_time > 0.35:
                        takeFish()

            # Draw rectangles
            for pt in zip(*loc[::-1]):
                cv.rectangle(
                    img,
                    pt,
                    (pt[0] + template.shape[1], pt[1] + template.shape[0]),
                    (0, 255, 0),
                    1,
                )

            # Save image
            # cv.imwrite("res.png", img)

            # Show preview
            cv.imshow("Preview", img)
            cv.waitKey(1)

            sleep(interval)
