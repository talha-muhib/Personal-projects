import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpFace = mp.solutions.face_detection
face = mpFace.FaceDetection()

capture = cv2.VideoCapture(0)

while True:
    _, img = capture.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face.process(imgRGB)

    if results.detections:
        for detection in results.detections:
            mpDraw.draw_detection(img, detection)

    cv2.imshow("Image", img)
    cv2.waitKey(1)