from PIL import ImageGrab
import numpy as np
import cv2

from time import sleep
import pydirectinput
import keyboard

from colorama import Fore, Style, just_fix_windows_console, init


def getData(capture_size: int) -> np.ndarray:
    """Takes a screenshot of the game and returns it as a numpy array."""
    x, y = pydirectinput.position()
    img = ImageGrab.grab(bbox=(x, y, x + capture_size, y + capture_size))
    data = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    return data


def toggleScript() -> None:
    """Toggles the script loop."""
    global script_active
    script_active = not script_active
    print(Style.DIM + 'Script loop is now', Fore.GREEN + 'active.' if script_active else Fore.RED + 'inactive.')


def moveAndBack(length: int=380) -> None:
    pydirectinput.moveRel(None, length, duration=0.2, relative=True)
    sleep(0.2)
    pydirectinput.moveRel(None, -length, duration=1, relative=True)


def autoFish(capture_size: int, threshold: int, interval: float) -> None:
    """Automatically casts the rod and catches something."""
    pydirectinput.rightClick()
    print('Casting the rod.')
    sleep(5)
    print('Waiting for something...')

    data = getData(capture_size)
    while np.sum(data == 0) > threshold:
        data = getData(capture_size)
        sleep(interval)
        # PREVIEW DATA
        cv2.imshow('Preview', data)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


    pydirectinput.rightClick()
    print('Catch!')
    sleep(0.15)
    moveAndBack()



def main():
    just_fix_windows_console()
    init(autoreset=True)

    global script_active
    script_active = False

    print(Style.BRIGHT +'Minecraft Auto Fishing Script for Mausaa')
    print(Style.DIM + 'Press ctrl to toggle the script.')
    print(Style.DIM + 'Press q to quit program.')
    print()

    keyboard.add_hotkey('ctrl', toggleScript)

    while True:
        while script_active:
            autoFish(25, 15, 0.2)

        if keyboard.is_pressed('q'):
            break

    keyboard.remove_hotkey('ctrl')


if __name__ == '__main__':
    main()
    