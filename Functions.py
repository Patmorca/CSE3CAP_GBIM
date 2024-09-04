## PUT EDITING FUNCTIONS IN HERE ##
## Hey Harry. Thought I'd put some thoughts in here. I think the most logical way to go about this would be to have this as a class we can instantiate in Main
## Something like class editFunction(self):, that way we could store variables we need to keep track of i.e image start size, start position etc.
## within the properties of the class, and stop them from being changed everytime a function (The edit operations) from this class is called on each frame 
##
## For example - Resize. We have functions(self,image) (an object of this class) in Main. We pass the image into it and store all the important information
## Then when a gesture is done being detected from MPRecognition, we pass the gesture's name to the FrameLoop and FrameLoop.callFunction("Whatever gesture was detected")
## callFunction will go through if/else to find the right one, and then call the appropriate method of from the object of this class i.e editFunction.resize()
##
## then, the method has the results (hand landmarks) and the initial photo information that will be an unchanging reference point for the duration needed. Since it will be called every
## frame we have the realtime update as long as the image is placed back on the tkinter canvas at the end of each frame's call. Since we have the hand landmarks,
## we've got all the math we need.
##
##
## Feel free to experiment or do it in whatever way makes the most sense though - just thought I'd give you my idea as a starting point
##
##
##
##
from PIL import ImageTk
from PIL import Image
import math
import numpy as np
from cv2 import readOpticalFlow, resize

class editFunctions:
    def __init__(self, image:ImageTk,canvasImage,canvas):
       
        self.image: Image = ImageTk.getimage(image)
        self.canvas = canvas
        self.canvasImage = canvasImage

        self.startWidth = self.image.width
        self.startHeight = self.image.height
        self.startPos = canvas.coords(self.canvasImage)
        self.startRot = 0
        
        self.updateWidth = self.startWidth
        self.updateHeight = self.startHeight
        self.updateRot = self.startRot
        self.startResults = None
        

    def resize(self,results):
        if(self.startResults == None):
            self.startResults = results
        
        startPoint = self.startResults.multi_hand_landmarks[0].landmark[8]
        if(results.multi_hand_landmarks != None):
            h1Landmarks = results.multi_hand_landmarks[0]
            h1Point = h1Landmarks.landmark[8]
        
        
            distance = math.sqrt((startPoint.x - h1Point.x)**2 + (startPoint.y - h1Point.y)**2) ## Doesnt Like Crossing over the centrepoint - just scales positive again
            print(distance)
            scaler = distance + 1
            
            if((h1Point.x < startPoint.x and h1Point.y < startPoint.y) or (h1Point.x<startPoint.x and h1Point.y > startPoint.y)): # I.e if you are in the left hand quadrants when you divide from the point, you are shrinking
                scaler = 1/scaler
        
            resizeWidth = self.startWidth * scaler
            resizeHeight = self.startHeight * scaler
            
            self.updateWidth = resizeWidth
            self.updateHeight = resizeHeight
            
            
            resizedImage = self.image.resize((math.floor(resizeWidth),math.floor(resizeHeight)),Image.Resampling.LANCZOS)
            resizedOut = ImageTk.PhotoImage(resizedImage)
            self.canvas.itemconfig(self.canvasImage,image=resizedOut)
            self.canvas.imgref = resizedOut
           
    
    def translate(self,results):
        if(self.startResults == None):
            self.startResults = results
        
        startPoint = self.startResults.multi_hand_landmarks[0].landmark[8]
        if(results.multi_hand_landmarks != None):
            
            h1Landmarks = results.multi_hand_landmarks[0]
            h1Point1 = h1Landmarks.landmark[8]
            self.canvas.moveto(self.canvasImage,h1Point1.x*1280,h1Point1.y*720)
            
        return
    
    def crop(self,results):
        print("cropping")
        return
        


    def rotate(self,results):
        if(self.startResults == None):
            self.startResults = results        

        startPoint = self.startResults.multi_hand_landmarks[0].landmark[8]
        print(self.startRot)
        if(results.multi_hand_landmarks != None):
            
            h1Landmarks = results.multi_hand_landmarks[0]
            h1Point1 = h1Landmarks.landmark[5]
            h1Point2 = h1Landmarks.landmark[8]
            
            
            rotPoint = [h1Point1.x,h1Point1.y]
            pivPoint = [h1Point2.x,h1Point2.y]
            

            rotVec = np.subtract(rotPoint,pivPoint)
            rotation = math.atan2(rotVec[1],rotVec[0])
            print(-(math.degrees(rotation)-90))

            outRot = -(math.degrees(rotation)-90)
            self.updateRot = self.startRot + outRot
            


            rotatedImage = self.image.rotate(self.startRot + outRot)
            rotatedOut = ImageTk.PhotoImage(rotatedImage)
            self.canvas.itemconfig(self.canvasImage,image=rotatedOut)
            self.canvas.imgred = rotatedOut
        return
    
        

    def setStart(self):
        self.startResults = None # Resetting start position of gesture coordinates
        self.startWidth = self.updateWidth
        self.startHeight = self.updateHeight
        self.startRot = self.updateRot

        