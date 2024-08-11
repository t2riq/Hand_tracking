#import libraries
import cv2
import mediapipe as mp
import time
import serial

# Adjust the serial port to match Pico
ser = serial.Serial('/dev/ttyACM0', 115200)
# Wait for the connection to establish
time.sleep(2.0)  

# Initialize Mediapipe Hands
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#asign the fingers IDs
tip_IDs = [4, 8, 12, 16, 20]

#start capturing
cap = cv2.VideoCapture(0)
#################################
#functions:

#function to set camera setting 
def set_camera(imge):
    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
    imge.flags.writeable = False
    results = hands.process(imge)
    imge.flags.writeable = True
    imge = cv2.cvtColor(imge, cv2.COLOR_RGB2BGR)
    return results
    
#function to track the hand marks
def track_marks(imge,lmlist,mp_hands):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = imge.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            mp_draw.draw_landmarks(imge, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return lmlist

#####################################
previous_state = None

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, imge = cap.read()
        imge = cv2.flip(imge, 1)
        
        #call the set camera setting function    
        results=set_camera(imge)

        #call track the land marks function
        lmlist = []
        lmlist=track_marks(imge,lmlist,mp_hands)

        if len(lmlist) != 0:
            fingers = []
            # Reverse the logic for the thumb
            if lmlist[tip_IDs[0]][1] < lmlist[tip_IDs[0] - 1][1]:
                fingers.append('1')
            else:
                fingers.append('0')
            # Index to Pinky
            for id in range(1, 5):
                if lmlist[tip_IDs[id]][2] < lmlist[tip_IDs[id] - 2][2]:
                    fingers.append('1')  
                else:
                    fingers.append('0')
            #send action to the pico
            current_state = ''.join(fingers) + '\n'
            if current_state != previous_state:
                print(f'Sending data to Pico: {current_state.strip()}')
                ser.write(current_state.encode())
                previous_state = current_state

            # Display the LED count on the screen
            cv2.rectangle(imge, (20, 300), (340,400), (125, 125, 125), 3)
            cv2.putText(imge, f'LEDS: {" ".join(fingers)}', (45, 357), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)

        #show and quit
        cv2.imshow('Hand Tracking LED', imge)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
ser.close()
