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
w, h = template.shape[1], template.shape[0]


def setup_colorama():
    just_fix_windows_console()
    init(autoreset=True)


def toggle_detection():
    global detection
    detection = not detection
    # Message to user
    print(
        Style.DIM + "Detection loop is now",
        Fore.GREEN + "active." if detection else Fore.RED + "inactive.",
    )


def toggle_reaction():
    global reaction
    reaction = not reaction
    # Message to user
    print(
        Style.DIM + "Reaction loop is now",
        Fore.GREEN + "active." if reaction else Fore.RED + "inactive.",
    )


def take_fish():
    print("Taking fish!")  # Message to user
    pdi.rightClick()
    pdi.moveRel(None, 380, 0.2, relative=True, disable_mouse_acceleration=True)
    sleep(0.2)
    pdi.moveRel(None, -380, 0.2, relative=True, disable_mouse_acceleration=True)
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
    _, max_val, _, max_loc = cv.minMaxLoc(res)

    # Consider a match only if it exceeds the threshold
    if max_val >= THRESHOLD:
        global detected_time
        detected_time = time()

        top_left = max_loc
        bottom_right = (
            top_left[0] + w,
            top_left[1] + h,
        )

        # Draw rectangle around the detected fish
        cv.rectangle(img, top_left, bottom_right, (0, 255, 0), 1)

    elif time() - detected_time > REACTION_TIME_THRESHOLD and reaction:
        take_fish()

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

    keyboard.add_hotkey("i", toggle_detection)  # Press i to toggle the script
    keyboard.add_hotkey("o", toggle_reaction)  # Press o to toggle the reaction
    keyboard.add_hotkey("p", lambda: os._exit(0))  # Press p to quit

    print(Style.BRIGHT + "Minecraft Auto Fishing AI Script for Mausaa")
    print(Style.DIM + "Press i to toggle the detect.")
    print(Style.DIM + "Press o to toggle the reaction.")
    print(Style.DIM + "Press p to quit program.")
    print()

    main_loop()
