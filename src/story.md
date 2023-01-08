## Inspiration
Our initial inspiration for this project came from one of the members of our team not wanting to pause a video due to them having been eating and their hands being greasy.
## What it does
BeyondControl introduces rudimentary gesture control system for a Windows computer. A user can manipulate volume, media playback, and window focus without having to touch their computer.
## How we built it
This application was build in python and heavily utilizes tensorflow, mediapipe, and a dataset from [haGRID](https://github.com/hukenovs/hagrid). Our team wrote a sequential convocational deep neural net to determine hand gestures. The training was done on landmarks, meaning it would be simple to extend the app for custom gestures processed through mediapipe rather than having to do custom labeling on the images. The font-end was written as an electron application with some javascript to help interface with python.

## Challenges we ran into
One of the largest challenges with this task was learning about how to adapt and train a model based on an arbitrary dataset.

## Accomplishments that we're proud of
Since the dawn of time, man kind has sought to control their surroundings with a wave of a hand. Today, we are proud to say we have accomplished this. Close your eyes and imagine the following, you are working on a secret coding project and your dad walks in on you when you least expect it. You can quickly minimize by showing a fist and he will be none the wise. This is but one example of the limitless potential our app facilitates. 

## What we learned
Making your own deep learning network not only does not produce great results, but is also extremely time consuming and makes you go slightly insane when you realize the best application of the software is to hide...... content.


## What's next for BeyondControl
We are hoping to add a way for the user to add their own gestures, and add an api to allow any gesture to be used for the users own custom functions.
