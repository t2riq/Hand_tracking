# Import libraries
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

# Assign the fingers IDs
tip_IDs = [4, 8, 12, 16, 20]

# Start capturing
cap = cv2.VideoCapture(0)

#################################
# Functions:

# Function to set camera setting 
def set_camera(imge):
    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
    imge.flags.writeable = False
    results = hands.process(imge)
    imge.flags.writeable = True
    imge = cv2.cvtColor(imge, cv2.COLOR_RGB2BGR)
    return results

# Function to track the hand marks
def track_marks(imge, lmlist, mp_hands):
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
led_st=''

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, imge = cap.read()
        imge = cv2.flip(imge, 1)
        
        # Call the set camera setting function    
        results = set_camera(imge)

        # Call track the land marks function
        lmlist = []
        lmlist = track_marks(imge, lmlist, mp_hands)

        if len(lmlist) != 0:
            fingers = []
            # Check if all fingers are up or down
            for id in range(0, 5):
                if lmlist[tip_IDs[id]][2] < lmlist[tip_IDs[id] - 2][2]:
                    fingers.append('1')  
                else:
                    fingers.append('0')
            if all(finger == '1' for finger in fingers):
                led_state = '0\n'
                led_st='ON'
            else:
                led_state = '1\n'
                led_st='OFF'
            # Send action to the Pico
            current_state = led_state
            if current_state != previous_state:
                print(f'Sending data to Pico: {current_state.strip()}')
                ser.write(current_state.encode())
                previous_state = current_state

            # Display the LED state on the screen
            cv2.rectangle(imge, (20, 300), (220,400), (125, 125, 125), 3)
            cv2.putText(imge, f'LED: {led_st}', (45, 357), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

        # Show and quit
        cv2.imshow('Hand Tracking LED', imge)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
ser.close()