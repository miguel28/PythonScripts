import numpy as np
import cv2

import os, pdb
from os import listdir
from os.path import isfile, join

import sys

def imageProcess(img,x,y,maxx,maxy):
    #for i in range(x):
    #    img = np.insert(img, 0, 0, axis=1)
         
    #height, width = img.shape[:2]   
    #for i in range(maxx - width):
    #    img = np.insert(img, width+i, 0, axis=1)    
                
    #for i in range(y):
    #    img = np.insert(img, 0, 0, axis=0)
        
    #height, width = img.shape[:2]    
    #for i in range(maxy - height):
    #    img= np.insert(img, height+i, 0, axis=0)       
     
    #return img
    height, width = img.shape[:2]  
    
    if x > 0:
        hmatrix1 = np.zeros((height,x,3), dtype=np.uint8)
        img = np.hstack((hmatrix1,img))
        
        print img.shape[:2]  
        print hmatrix1.shape[:2] 
        height, width = img.shape[:2]  
        
    if (maxx - width) > 0 :
        hmatrix2 = np.zeros((height,maxx - width,3), dtype=np.uint8)
        print img.shape
        print hmatrix2.shape
        #pdb.set_trace()
        img = np.hstack((img,hmatrix2))
        height, width = img.shape[:2]  
    
    if y > 0:
        vmatrix1 = np.zeros((y,maxx,3), dtype=np.uint8)
        print img.shape[:2]  
        print vmatrix1.shape[:2]
        img = np.vstack((vmatrix1,img))
        height, width = img.shape[:2]  
        
    if (maxy - height) > 0:
        vmatrix2 = np.zeros((maxy - height,maxx,3), dtype=np.uint8)
        print img.shape[:2]  
        print vmatrix2.shape[:2] 
        img = np.vstack((img,vmatrix2))
        
    #cv2.imshow("frame",img)
    #cv2.waitKey(0)
    return img

def test2rect(data, mheight, mwidth):
    left = int(data[1])
    botom = int(data[2])
    right = int(data[3])
    top = int(data[4])
        
    x = left
    y = mheight - top
    width = right - left
    height = top - botom
        
    return [x ,y ,width, height]
        
def rect2tess(data, mheight, mwidth):
    x = int(data[0])
    y = int(data[1])
    width = int(data[2])
    height = int(data[3])
        
    left = x
    botom = mheight - y - height
    right = x + width
    top = mheight - y
    return " " + str(left) + " " + str(botom) + " " + str(right) + " " + str(top) + " " 

class mergeImage:

    totalHeight = 1000;
    totalWidth = 1000;
    currentX = 0;
    currentY = 0;
    maxY = 0;
    finalName = "final"
    finalImage = np.zeros((totalHeight,totalWidth,3), np.uint8)
    finalBoxes = []    
    
    def process(self,files):
        self.finalBoxes = []
        for file in files: 
            if ".jpg" in file: 
                print "***************************************************************"
                print "Procesing Image" + file
                image = cv2.imread(file)
                height, width = image.shape[:2] 
                
                print "  Image W:", width, " H:",height
                
                if height > self.maxY:
                    print "found new Y", height
                    self.maxY = height
                
                if(self.currentX + width >= self.totalWidth):
                    self.currentX = 0
                    self.currentY = self.currentY + self.maxY
                    self.maxY = 0
                    print "New Line:", self.currentY , "Max:", self.maxY
                
                print "Place in X:", self.currentX, " Y:",self.currentY
                prosImage = imageProcess(image,self.currentX,self.currentY,self.totalHeight,self.totalWidth)
                self.finalImage = prosImage+self.finalImage
                
                boxfile = file[:-3] + "box"
                print "Processing Box file", boxfile 
                
                with open (boxfile, "r") as myfile:
                    boxes = myfile.read().split("\n")
                    for box in boxes:
                        data = box.split(" ")
                        if len(data)>=6:
                            x,y,w,h = test2rect(data, height, width)
                            
                            newData =[]
                            newData.append( x + self.currentX)
                            newData.append( y + self.currentY)
                            newData.append( w )
                            newData.append( h )
                            
                            newBox = data[0] + rect2tess(newData, self.totalHeight, self.totalWidth) + data[5]
                            self.finalBoxes.append(newBox)

                self.currentX = self.currentX + width

        with open(self.finalName + ".box", "w") as text_file:
            for line in self.finalBoxes:
                text_file.write(line + "\n")
            
        cv2.imwrite(self.finalName+".png", self.finalImage)


onlyfiles = [ f for f in listdir(".") if isfile(join(".",f)) ]

def processSTN(stn, tFiles):
    files = []
    for file in tFiles:
        if stn in file:
            files.append(file)

    processor = mergeImage();
    processor.finalName = "Finale OCR " + stn
    processor.process(files)  
    print "--------------------------------------------------"
    
if len(sys.argv) > 1:
    processSTN(sys.argv[1], onlyfiles)

else:
    cstn = ""
    stns = []
    for file in onlyfiles:
        names = file.split("_")
        if names[0] != cstn and ".jpg" in file:
            cstn = names[0]
            stns.append(cstn)
    print "Find STNS", stns   
    for pstn in stns:
        processSTN(pstn, onlyfiles)
    