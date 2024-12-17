import cv2
import numpy as np
import math
from hand_tracking_min import HandDetector
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

detector = HandDetector(maxHands=1, detectionCon=0.7)
capture = cv2.VideoCapture(0)

while True:
    _, img = capture.read()
    img, lst = detector.find_hands(img)

    if len(lst) > 0:
        landmarks = lst[0]

        if len(landmarks) > 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (mid_x, mid_y), 7, (255, 255, 0), cv2.FILLED)

            if length < 50:
                cv2.circle(img, (mid_x, mid_y), 7, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)