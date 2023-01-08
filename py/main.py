import json
import cv2
from time import sleep
from HandRecognition import HandRecognition
from GestureActions import GestureActions
import sys
import signal

camera = cv2.VideoCapture(0)


def signal_handler(sig, frame):
    camera.release()
    exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    func_map = None
    actions = GestureActions()
    with open('..\\gesture_function_map.json', 'r') as func_conf:
        func_map = json.load(func_conf)

    gesture_detector = HandRecognition()

    while True:
        # getting a frame from the camera
        _, frame = camera.read()

        x, y, c = frame.shape
        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        gesture = gesture_detector.getGestureName(frame_rgb)

        if gesture == "":
            continue

        action_to_run = func_map[gesture]["function"]
        delay = func_map[gesture]["delay"]
        if action_to_run == "":
            continue

        gesture_func: function = getattr(actions, action_to_run)
        gesture_func()
        sleep(delay)


if __name__ == "__main__":
    main()
