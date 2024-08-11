#import libraries
import cv2
import mediapipe as mp
import time
import numpy as np
import math
import alsaaudio
################
#creat class for hand tracking 
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackcon=trackcon
       
        self.mphands = mp.solutions.hands
        self.hands =self.mphands.Hands(static_image_mode=self.mode, 
                                      max_num_hands=self.maxHands, 
                                      min_detection_confidence=self.detectionCon, 
                                      min_tracking_confidence=self.trackcon)
        self.mp_draw = mp.solutions.drawing_utils
        

    def findhand(self,frame,draw=True):
        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb) 

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
               if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mphands.HAND_CONNECTIONS)
        return frame
    
    def findposition(self,frame,handno=0,drow=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                #print(id,lm)   
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                if drow:
                    cv2.circle(frame,(cx,cy),12,(0,0,255),cv2.FILLED) 
        
        return lmlist
###################

#asign constant values
wcam,hcam=640,480
pt=0
ct=0
minvol=0
maxvol=100
volbar=400
volper=0

#call the class
detector=handDetector(detectionCon=0.7)
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

#call volume library 
mixer =alsaaudio.Mixer(control='Master')

def set_volume(volume_percentage):
    volume = int(volume_percentage * 100 / 100) 
    mixer.setvolume(volume)
   
#capturing loop
while True:
    su,imge=cap.read()
    #call findhand from class 
    imge=detector.findhand(imge)
    #call findposition from class
    lm_list=detector.findposition(imge,drow=False)
    
    #check if there is a hand
    if len(lm_list)!=0:
        print(lm_list[4],lm_list[8])
        #find the centers
        x1,y1=lm_list[4][1],lm_list[4][2]
        x2,y2=lm_list[8][1],lm_list[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(imge,(x1,y1),12,(0,0,255),cv2.FILLED) 
        cv2.circle(imge,(x2,y2),12,(0,0,255),cv2.FILLED) 
        cv2.line(imge,(x1,y1),(x2,y2),(255,255,255),3)    
        cv2.circle(imge,(cx,cy),10,(0,0,255),cv2.FILLED) 
                
        #calc the length between the fingers
        lth=math.hypot(x2-x1,y2-y1)
        
        #control the volume 
        vol=np.interp(lth,[50,200],[minvol,maxvol])
        volbar=np.interp(lth,[50,200],[400,150])
        volper=np.interp(lth,[50,200],[0,100])
        set_volume(vol)
        
        #drow green circle when lenght less than 50
        if lth<50:
            cv2.circle(imge,(cx,cy),10,(0,255,0),cv2.FILLED) 
                 
    #volume and % show      
    cv2.rectangle(imge,(50,150),(85,400),(125,125,125),3)
    cv2.rectangle(imge,(50,int(volbar)),(85,400),(125,125,125),cv2.FILLED)
    cv2.putText(imge,f'{int(volper)}%',(40,450)
                ,cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3) 
    
    #control fps speed
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct 
    cv2.putText(imge,f'VOLUME CONTROL',(10,70)
                 ,cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),3)
    
    #show and quit button
    cv2.imshow('Hand Tracking volume', imge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
