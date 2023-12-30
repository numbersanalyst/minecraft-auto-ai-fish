from PIL import ImageGrab
import numpy as np
import cv2

from time import sleep
import pyautogui
import keyboard

script_active = False

def getData(capture_size: int) -> np.ndarray:
    """Takes a screenshot of the game and returns it as a numpy array."""
    x, y = pyautogui.position()
    img = ImageGrab.grab(bbox=(x, y, x + capture_size, y + capture_size))
    data = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    return data


def toggleScript() -> None:
    """Toggles the script loop."""
    global script_active
    script_active = not script_active
    print('Script loop is now', 'active.' if script_active else 'inactive.')



def autoFish(capture_size: int, threshold: int, interval: float) -> None:
    """Automatically casts the rod and catches something."""
    pyautogui.rightClick()
    print('Casting the rod.')
    sleep(5)
    print('Waiting for something...')

    data = getData(capture_size)
    while np.sum(data == 0) > threshold:
        data = getData(capture_size)
        sleep(interval)
        # PREVIEW DATA
        # cv2.imshow('Preview', data)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break

    pyautogui.rightClick()
    print('Catch!')
    sleep(1)


def main():
    print('Minecraft Auto Fishing Script for Mausaa')
    print('Press ctrl to toggle the script.')
    print('Press q to quit program.')
    print()

    keyboard.add_hotkey('ctrl', toggleScript)

    while True:
        while script_active:
            autoFish(15, 10, 0.2)

        if keyboard.is_pressed('q'):
            break

    keyboard.remove_hotkey('ctrl')


if __name__ == '__main__':
    main()