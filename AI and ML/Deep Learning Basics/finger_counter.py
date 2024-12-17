import cv2
import numpy as np
import math
from hand_tracking_min import HandDetector

detector = HandDetector(detectionCon=0.7)
capture = cv2.VideoCapture(0)

fingertip_ids = [4, 8, 12, 16, 20]

while True:
    _, img = capture.read()
    img, lst = detector.find_hands(img)

    if len(lst) > 0:
        landmarks = lst[0]

        if len(landmarks) > 0:
            fingers = []
            if landmarks[fingertip_ids[0]][1] > landmarks[fingertip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for i in range(1, 5):
                if landmarks[fingertip_ids[i]][2] < landmarks[fingertip_ids[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            print(fingers)

    cv2.imshow("Image", img)
    cv2.waitKey(1)