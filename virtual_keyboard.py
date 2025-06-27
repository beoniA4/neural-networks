import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Controller

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8)

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
]
finalText=''

keyboard=Controller()

def drawAll(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cvzone.cornerRect(img,(button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img

class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size

buttonList=[]
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))

while True:
    success,img=cap.read()
    hands,img=detector.findHands(img)
    img=drawAll(img,buttonList)
    if hands:
        lmlist=hands[0]['lmList']
        for button in buttonList:
            x,y=button.pos
            w,h=button.size
            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+h:
                cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),(175,0,175),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                point1 = lmlist[8][:2]
                point2 = lmlist[12][:2]

                result = detector.findDistance(point1, point2, img)
                print("Result:", result)

                if isinstance(result, (tuple, list)):
                    if len(result) >= 3:
                        l, _, img = result[:3]
                    elif len(result) == 2:
                        l, img = result
                    else:
                        l = result[0]
                else:
                    l = result

                if l<30:
                    keyboard.press(button.text)
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    finalText += button.text
                    sleep(0.15)

    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60,430),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)

    cv2.imshow("Image",img)
    cv2.waitKey(1)