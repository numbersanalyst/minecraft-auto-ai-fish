import cv2 as cv
import numpy as np
from PIL import ImageGrab
import pydirectinput as pdi
from time import sleep, time
import keyboard
import os
from colorama import Fore, Style, just_fix_windows_console, init

# Settings
CAPTURE_SIZE = 150
THRESHOLD = 0.6
INTERVAL = 0.25
REACTION_TIME_THRESHOLD = 0.35

detection = False
reaction = False
detected_time = time()
template = cv.imread("bobber_full.png")


def setup_colorama():
    just_fix_windows_console()
    init(autoreset=True)


def toggle_script():
    global detection
    detection = not detection
    # Message to user
    print(
        Style.DIM + "Script loop is now",
        Fore.GREEN + "active." if detection else Fore.RED + "inactive.",
    )


def take_fish():
    print("Taking fish!")  # Message to user
    pdi.rightClick()
    pdi.moveRel(None, 380, 0.25, relative=True, disable_mouse_acceleration=True)
    sleep(0.2)
    pdi.moveRel(None, -380, 0.25, relative=True, disable_mouse_acceleration=True)
    sleep(1)
    pdi.rightClick()
    sleep(3)


def process_image():
    x, y = pdi.position()
    img = cv.cvtColor(
        np.array(
            ImageGrab.grab(
                bbox=(
                    x - CAPTURE_SIZE,
                    y - CAPTURE_SIZE,
                    x + CAPTURE_SIZE,
                    y + CAPTURE_SIZE,
                )
            )
        ),
        cv.COLOR_RGB2BGR,
    )
    return img


def detect_fish(img):
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)

    # Reaction
    if reaction:
        global detected_time
        if np.sum(loc) != 0:
            detected_time = time()
        elif time() - detected_time > REACTION_TIME_THRESHOLD:
            take_fish()

    # Draw rectangles
    for pt in zip(*loc[::-1]):
        cv.rectangle(
            img,
            pt,
            (pt[0] + template.shape[1], pt[1] + template.shape[0]),
            (0, 255, 0),
            1,
        )

    return img


def show_preview(img):
    cv.imshow("Preview", img)
    cv.waitKey(1)


def main_loop():
    while True:
        if detection:
            screen = process_image()
            img_with_detection = detect_fish(screen)
            show_preview(img_with_detection)
            sleep(INTERVAL)


if __name__ == "__main__":
    setup_colorama()

    keyboard.add_hotkey("p", toggle_script)  # Press p to toggle the script
    keyboard.add_hotkey("o", lambda: os._exit(0))  # Press o to quit

    print(Style.BRIGHT + "Minecraft Auto Fishing AI Script for Mausaa")
    print(Style.DIM + "Press p to toggle the script.")
    print(Style.DIM + "Press o to quit program.")
    print()

    main_loop()
