import numpy as np
import cv2

class Draw:
    dark = (35,34,39)
    img = cv2.imread('friends.jpg')

    def __init__(self,result):
        self.result = result

    def movePoint(self,x,y):
        return (x[0] + y[0],x[1] + y[1])

    def drawFace(self):
        main = (123,1,233)
        for face in self.result["faces"]:
            #Highlight face
            pt1 = (face["faceRectangle"]["left"] , face["faceRectangle"]["top"])
            pt2 = (face["faceRectangle"]["left"] + face["faceRectangle"]["width"] , face["faceRectangle"]["top"] + face["faceRectangle"]["height"])
            cv2.rectangle(self.img,pt1,pt2,main,2)
            #Top info
            ptt = self.movePoint(pt1,(-1,-2))
            ptl = cv2.getTextSize(face["gender"],1,1.1,1)
            cv2.rectangle(self.img, self.movePoint(ptt,(0,ptl[1]-5)),self.movePoint(ptt,(ptl[0][0]+1,-2-ptl[0][1])),main,-1);
            cv2.putText(self.img,face["gender"],self.movePoint(ptt,(2,0)),1,1.1,self.dark)
            #Bottom Info
            ptb = self.movePoint(pt1,(-1,face["faceRectangle"]["height"]+14))
            ptl = cv2.getTextSize("Age:" + str(face["age"]),1,1.1,1)
            cv2.rectangle(self.img, self.movePoint(ptb,(0,ptl[1]-3)),self.movePoint(ptb,(ptl[0][0]+1,-2-ptl[0][1])),main,-1);
            cv2.putText(self.img,"Age:"+str(face["age"]),self.movePoint(ptb,(2,0)),1,1.1,self.dark)

    def drawObject(self):
        main = (2,252,220)
        for object in self.result["objects"]:
            #Highlight object
            pt1 = (object["rectangle"]["x"] , object["rectangle"]["y"])
            pt2 = (object["rectangle"]["x"] + object["rectangle"]["w"] , object["rectangle"]["y"] + object["rectangle"]["h"])
            cv2.rectangle(self.img,pt1,pt2,main,2)
            #Top info
            ptt = self.movePoint(pt1,(-1,-2))
            ptl = cv2.getTextSize(object["object"],1,1.1,1)
            cv2.rectangle(self.img, self.movePoint(ptt,(0,ptl[1]-5)),self.movePoint(ptt,(ptl[0][0]+1,-2-ptl[0][1])),main,-1);
            cv2.putText(self.img,object["object"],self.movePoint(ptt,(2,0)),1,1.1,self.dark)
            #Bottom Info
            ptb = self.movePoint(pt1,(-1,object["rectangle"]["h"]+14))
            ptl = cv2.getTextSize(str(object["confidence"]*100)+"%",1,1.1,1)
            cv2.rectangle(self.img, self.movePoint(ptb,(0,ptl[1]-3)),self.movePoint(ptb,(ptl[0][0]+1,-2-ptl[0][1])),main,-1);
            cv2.putText(self.img,str(object["confidence"]*100)+"%",self.movePoint(ptb,(2,0)),1,1.1,self.dark)

    def additionalInfo(self):
        main = (255,255,255)
        ptl = cv2.getTextSize("Captions: "+self.result["description"]["captions"][0]["text"],1,1.3,1)
        cv2.rectangle(self.img, (0,0),self.movePoint(ptl[0],(1,5)),self.dark,-1);
        cv2.putText(self.img,"Captions: "+self.result["description"]["captions"][0]["text"],(0,15),1,1.3,main)
        if len(self.result["description"]["tags"]) > 8:
            temp = [self.result["description"]["tags"][:7],self.result["description"]["tags"][7:]]
            cv2.rectangle(self.img, (0,19),self.movePoint(ptl[0],(1,26)),self.dark,-1)
            cv2.putText(self.img,"Tags: #"+" #".join(temp[0]),(0,35),1,1.3,main)
            temp2 = [temp[1][:7],temp[1][7:]]
            cv2.rectangle(self.img, (0,38),self.movePoint(ptl[0],(1,45)),self.dark,-1)
            cv2.putText(self.img,"#"+" #".join(temp2[0]),(0,54),1,1.3,main)
            if len(temp2[1]) != 0:
                cv2.rectangle(self.img, (0,58),self.movePoint(ptl[0],(1,67)),self.dark,-1)
                cv2.putText(self.img,"#"+" #".join(temp2[1]),(0,74),1,1.3,main)
        else:
            cv2.rectangle(self.img, (0,19),self.movePoint(ptl[0],(1,26)),self.dark,-1);
            cv2.putText(self.img,"Tags: "+" ".join(self.result["description"]["tags"]),(0,35),1,1.3,main)

    def displyImg(self):
        cv2.imshow('Analyzed Image', self.img)
        cv2.waitKey(0)
