#import required library
import controller as cnt
import requests
from boltiot import Bolt 
from config import confi as co
import mediapipe as mp
import time
import threading
import cv2
import json
import numpy as np

time.sleep(2.0)

no = 0
mybolt = Bolt(co.bolt_api_key,co.device_id)
tipIds=[4,8,12,16,20]

#status checking for Boltiot
def statuschecking ():
	try :

		status = mybolt.isOnline()
		status = json.loads(status)

	except Exception as e :
		print ("error occured")
		print (e)

	if status['success']==1 :

		blank = np.zeros((500,700,3),dtype='uint8')

		cv2.putText(img= blank,text='STATUS : ONLINE',
		org=(10,50),fontFace = cv2.FONT_HERSHEY_PLAIN,
		fontScale=2,color=(255,255,255),thickness=2)

		cv2.putText(img= blank,text='PROCESSING...',
		org=(250,250),fontFace = cv2.FONT_HERSHEY_PLAIN,
		fontScale=2,color=(255,255,255),thickness=2)

		cv2.imshow('blank',blank)
		captures()
		cv2.waitKey(0)

	else :
            print(status)

            mybolt.restart()

            blank1 = np.zeros((500,700,3),dtype='uint8')

            cv2.putText(img= blank1,text='STATUS : OFFLINE',
            org=(10,50),fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale=2,color=(255,255,255),thickness=2)

            cv2.putText(img= blank1,text='RESTARTING...',
            org=(250,250),fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale=2,color=(255,255,255),thickness=2)

            cv2.imshow('blank',blank1)
            cv2.waitKey(0)

def welcome() :
    blank3 = np.zeros((500,700,3),dtype='uint8')

    cv2.putText(img= blank3,text='WELCOME TO EPULZ',
    org=(150,50),fontFace = cv2.FONT_HERSHEY_PLAIN,
    fontScale=2,color=(255,255,255),thickness=2)

    cv2.putText(img= blank3,text='DONT HAVE A GOOD DAY',
    org=(100,255),fontFace = cv2.FONT_HERSHEY_PLAIN,
    fontScale=2,color=(255,255,255),thickness=2)
    
    cv2.putText(img= blank3,text='HAVE A GREAT DAY!!',
    org=(100,300),fontFace = cv2.FONT_HERSHEY_PLAIN,
    fontScale=2,color=(255,255,255),thickness=2)


    cv2.imshow('blank',blank3)

#Alert when the value exceeds
def Alerting():
    time.sleep(5)
    if total == 5 :
        welcome()
        time.sleep(5)
        cnt.Alarm()
    else :
        print("changed")
      
#capture the hand
def captures() :

    mp_draw=mp.solutions.drawing_utils
    mp_hand=mp.solutions.hands

    video=cv2.VideoCapture(0)

    with mp_hand.Hands(min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
        while True:
            ret,image=video.read()
            image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable=False
            results=hands.process(image)
            image.flags.writeable=True
            image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            lmList=[]
            if results.multi_hand_landmarks:
                for hand_landmark in results.multi_hand_landmarks:
                    myHands=results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHands.landmark):
                        h,w,c=image.shape
                        cx,cy= int(lm.x*w), int(lm.y*h)
                        lmList.append([id,cx,cy])

                    mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS, 
                        landmark_drawing_spec=mp_draw.DrawingSpec(color = (255,0,0),
                        circle_radius=2, 
                        thickness=2),
                        connection_drawing_spec=mp_draw.DrawingSpec(thickness=2, 
                        color=(0,0,0)))

            fingers=[]
            if len(lmList)!=0:
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1,5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                global total
                total=fingers.count(1)

    
                t1 = threading.Thread(target=Alerting)
                cnt.led(total)
                
                if total == 5 :
                    if no == total :
                        pass
                    else :
                        t1.start()
                        no = total
                else:
                    no = total

                if total==0:
                    cv2.putText(image, "0", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 5)
                elif total==1:
                    cv2.putText(image, "1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 5)
                elif total==2:
                    cv2.putText(image, "2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 5)
                elif total==3:
                    cv2.putText(image, "3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 5)
                elif total==4:
                    cv2.putText(image, "4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 5)
                elif total==5:
                    cv2.putText(image, "5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 0, 0), 5)

            cv2.imshow("Frame",image)
            k=cv2.waitKey(1)
            if k==ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
statuschecking()
