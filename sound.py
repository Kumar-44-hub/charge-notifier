import winsound
import time

def play_plugged_sound():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

def play_unplugged_sound():
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)


if __name__ == "__main__":
    print("Testing plugged sound...")
    play_plugged_sound()
    time.sleep(1)

    print("Testing unplugged sound...")
    play_unplugged_sound()
