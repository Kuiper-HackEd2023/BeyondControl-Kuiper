from torchvision import models
from torchvision import transforms
from PIL import Image
import mediapipe as mp
import cv2
import torch
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input, Conv1D, MaxPooling1D, Flatten
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from transformers import AutoModel


# roughly inspired from https://github.com/nicknochnack/ActionDetectionforSignLanguage/blob/main/Action%20Detection%20Tutorial.ipynb

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

gesture_map = {
    "none": 0,
    "like": 1,
    "call": 2,
    "dislike": 3,
    "fist": 4,
    "four": 5,
    "mute": 6,
    "ok": 7,
    "one": 8,
    "palm": 9,
    "peace": 10,
    "peace_inverted": 11,
    "rock": 12,
    "stop": 13,
    "stop_inverted": 14,
    "three": 15,
    "three2": 16,
    "two_up": 17,
    "two_up_inverted": 18
}

def save_from_ann(ann, action):
    for image, desc in ann.items():
        for label in range(len(desc['labels'])):
            if len(desc['landmarks'][label]) == 0: continue
            if desc['labels'][label] == action:
                hand = np.array([[land[0], land[1]] for land in desc['landmarks'][label]])
                path = os.path.join('data\\subsample\\keypoints', action, image)
                np.save(path, hand)
            else:
                none = np.array([[land[0], land[1]] for land in desc['landmarks'][label]])
                path = os.path.join('data\\subsample\\keypoints\\none', image)
                np.save(path, none)

def load_from_np(path):
    gestures, labels = [], []
    for dir in os.listdir(path):
        for file in os.listdir(os.path.join(path, dir)):

            gesture = np.load(os.path.join(path, dir, file))
            
            if len(gesture) > 0 and gesture.shape == (21,2):
                gestures.append(gesture)
                labels.append(gesture_map[dir])
    return np.array(gestures), np.array(labels)

def myModel():
    model = Sequential()
    model.add(Conv1D(32, 3, input_shape=(21, 2)))
    model.add(MaxPooling1D())
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(19, activation='softmax'))
    return model

model = myModel()


# json_path = "data\\subsample\\ann_subsample\\ann_subsample"
# for file in os.listdir(json_path):
#     with open(os.path.join(json_path, file)) as jfile:
#         data = json.loads(jfile.read())
#         save_from_ann(data, os.path.splitext(file)[0])

# X, Y = load_from_np('data\\subsample\\keypoints')
# Y = tf.keras.utils.to_categorical(Y).astype(int)
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.05)


    
# model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.BinaryCrossentropy(), metrics=['categorical_accuracy'])
# model.fit(X_train.astype('float32'), y_train.astype('float32'), epochs=1500)
# model.save('modelgood.h5')


# https://google.github.io/mediapipe/getting_started/python.html
with mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        gest = 0
        model = tf.keras.models.load_model('modelgood.h5')

        if (results.left_hand_landmarks):
            input = np.array([[res.x, res.y] for res in results.left_hand_landmarks.landmark]).astype('float32')
            input = tf.expand_dims(input, axis=-1)
            input = np.reshape(input, (1, 21, 2))
            res = model.predict(input)
            gest = np.argmax(res)

        if (results.right_hand_landmarks):
            input = np.array([[res.x, res.y] for res in results.right_hand_landmarks.landmark]).astype('float32')
            input = tf.expand_dims(input, axis=-1)
            input = np.reshape(input, (1, 21, 2))
            res = model.predict(input)
            gest = np.argmax(res)

        print(list(gesture_map.keys())[gest])

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS)

        cv2.imshow('hand gesture', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()