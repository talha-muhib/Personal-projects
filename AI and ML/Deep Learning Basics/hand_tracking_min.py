import cv2
import mediapipe as mp

#Hand Detector class
class HandDetector:
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5):
        """
        Read the following for more info on the parameters
        https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
        """

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon #Detection confidence
        self.complexity = complexity
        self.trackCon = trackCon #Tracking confidence

        #Extract the hand detection function from Mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.complexity,
                                        self.detectionCon,
                                        self.trackCon)

        #Mediapipe's drawing utilities
        self.mpDraw = mp.solutions.drawing_utils
    
    #Find the hands in our image
    def find_hands(self, img, draw=True, id_list=[4, 8]):
        #Process the image using OpenCV and get the results using Mediapipe
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        #Collect landmarks for every hand in this list
        hand_list = []

        #Check if we have the hand landmarks
        if results.multi_hand_landmarks:
            #Go through every hand
            for hand in results.multi_hand_landmarks:
                #Extract landmarks for every hand
                hand_list.append(self.__find_pos(img, hand, draw, id_list))

                #Draw the hands with its landmarks and the connections between them
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
        
        #Return list
        return img, hand_list
    
    #Find positions of landmarks for every hand and return as a list
    def __find_pos(self, img, hand, draw=True, id_list=[4, 8]):
        #List to collect all landmarks
        landmark_list = []

        for id, lm in enumerate(hand.landmark):
            #Get the shape of the image
            h, w, c = img.shape

            #Determine position of each landmark using height & width of the image
            cx, cy = int(w * lm.x), int(h * lm.y)

            #Append ID and positions of each landmark to our list
            landmark_list.append([id, cx, cy])
            
            #For every 5th landmark ID, display a purple circle underneath it
            if id in id_list and draw:
                cv2.circle(img, (cx, cy), 12, (255, 255, 0), cv2.FILLED)
        
        #Return list
        return landmark_list

#Main function
def main():
    #Default video camera of laptop
    capture = cv2.VideoCapture(0)

    #Instantiate our hand detector class
    detector = HandDetector()

    #Run the loop forever
    while True:
        #Read the image captured on camera
        _, img = capture.read()

        #Find hands using our detector
        img, hand_list = detector.find_hands(img)

        #Print list
        print(hand_list)

        #Display image on screen
        cv2.imshow("Image", img)

        #Wait a millisecond for key input
        cv2.waitKey(1)

if __name__ == "__main__":
    main()