import numpy as np
import mediapipe as mp
import tensorflow as tf
from time import sleep
from keras.models import load_model
from GuestureActions import GuestureActions


class HandRecognition:
    def __init__(self) -> None:
        self._mpHands = mp.solutions.hands
        self._hands = self._mpHands.Hands(
            max_num_hands=1, min_detection_confidence=0.7)
        self._mpDraw = mp.solutions.drawing_utils
        self._model = load_model('..\\model.h5')
        with open('..\\gesture.names', 'r') as gesture_name_file:
            self._gesture_names: list[str] = gesture_name_file.read().split(
                '\n')

    def getGestureName(self, frame_rgb):
        gesture_name = ""
        result = self._hands.process(frame_rgb)
        if result.multi_hand_landmarks:
            landmarks = []
            for landmark_point in result.multi_hand_landmarks:
                input = np.array(
                    [[res.x, res.y] for res in landmark_point.landmark]).astype('float32')
                input = tf.expand_dims(input, axis=-1)
                input = np.reshape(input, (1, 21, 2))
                prediction = self._model.predict(input, verbose=0)
                classID = np.argmax(prediction)
                gesture_name = self._gesture_names[classID]
        return gesture_name
