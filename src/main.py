import cv2
from HandRecognition import HandRecognition
# import HandRecognition


def main():
    camera = cv2.VideoCapture(0)
    gesture_detector = HandRecognition()
    while True:
        # getting a frame from the camera
        _, frame = camera.read()

        x, y, c = frame.shape
        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        gesture = gesture_detector.getGestureName(frame_rgb)

        if gesture != "":
            print(gesture)


if __name__ == "__main__":
    main()
