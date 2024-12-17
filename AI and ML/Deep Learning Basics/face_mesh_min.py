import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpMesh = mp.solutions.face_mesh
mesh = mpMesh.FaceMesh()
drawingSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

while True:
    _, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mesh.process(imgRGB)

    if results.multi_face_landmarks:
        for lm in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, lm, mpMesh.FACEMESH_CONTOURS, drawingSpec, drawingSpec)

    cv2.imshow("Image", img)
    cv2.waitKey(1)