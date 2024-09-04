## PUT OPENCV FRAME UPDATE LOGIC IN HERE ##

## Not too sure how python hands passing objects, whether they're copied and passed by value or passed by reference and can be edited from within the caller.
## Will need to investigate when things are up and running to see.

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
from PIL import ImageTk
import _tkinter as tk
import MPRecognition
import Functions
import numpy as np
import math
from threading import Thread

class GestureVision:
    
    def __init__(self,root,window,affirmation,model_data,editor): ## Initialises all MP and CV variables and objects to be operated on
        
        self.frameCapture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpHandObject = self.mpHands.Hands()
        
        ##MPRecognition REFERENCES
        
        self.model_data = model_data
        self.recognizer = MPRecognition.MPRecognizer(self.model_data)
        self.gesture = None

        ## UI REFERENCES ##
       
        self.root = root 
        self.window = window
        self.affirmation = affirmation
        
        ## Optimisations ##
        self.runProcessing = 0
        
        ## Editing ##
        self.editor = editor
        self.prevEdit = "none" # This is a variable that acts to inform the editing calls when an edit is finished in order to update the values contained within the Functions object so That the subsequent edit operates from those.
       
        self.cropMode = False
        self.boolBuffer = ["none"]*5
        
    def updateFrame(self):
        success, frame = self.frameCapture.read()
        if success:
            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) ## OpenCV takes images in BGR format, this converts them into the proper RGB format for display and processing
            results = self.mpHandObject.process(frameRGB)
            
            gestureFrame = Image.fromarray(frameRGB)
 
            ## MPObject will be a globally defined MPRecognizer object declared within the main ui loop


            ######################################OPTIMISATIONS#################################################
            ## Comment out the if else chain to make the recognizer process every single frame
            ## Comment out gThread and comment back in the commented out line to run the old version. NOTE: You must change self.affirmation.config(text=MPRecognition to =self.gesture).
            if(results.multi_hand_landmarks):
                if(self.runProcessing == 0):
                    gThread = Thread(target = self.recognizer.recognizeGesture,args = [gestureFrame,results])
                    gThread.daemon = True
                    gThread.start()
                    #self.gesture = self.recognizer.recognizeGesture(gestureFrame,results)
                    self.runProcessing += 1
                elif(self.runProcessing < 3):
                    self.runProcessing += 1
                else:
                    self.runProcessing = 0
            else:
                MPRecognition.gesture = "none"

            ##DEBUG##
            if(self.cropMode == False):
                self.affirmation.config(text=MPRecognition.gesture)
            else:
                self.affirmation.config(text = "crop") # Crop mode indicator
            ##DEBUG##

           #######################################OPTIMISATIONS####################################################
          

            self.callFunction(MPRecognition.gesture,results)
            
        
            
            resizedFrame = gestureFrame.resize((320,240),Image.Resampling.LANCZOS)
            displayFrame = ImageTk.PhotoImage(image = resizedFrame)
       
            ## return it to the tkinter widget in which we want to display it
       
            self.window.image = displayFrame
            self.window.config(image=displayFrame)
            self.root.after(1,self.updateFrame)
            
        else:
            return
        
      
    def drawLandmarks(self): ## Draws hand landmarks. Good debugging tool but unnecessary to do all the time. Could add as boolean option
        return
    
    def callFunction(self,gesture,results): ## This method will be called to check which function to call based on the contents of the buffer

        #print(MPRecognition.gesture)

        if(gesture == "resize"):
            if(self.cropMode == True):
                self.editor.crop(results)
                self.prevEdit = "cropsize"
            
            elif(self.cropMode == False):
                self.editor.resize(results)
                self.prevEdit = "resize"
        
        elif(gesture == "translate" and self.cropMode == False):
            self.editor.translate(results)
            self.prevEdit = "translate"
        
        elif(gesture == "crop"):
            
            if(self.cropMode == False and self.prevEdit != "cropexit"): #If you didnt just exit crop
                self.cropMode = True
                self.prevEdit = "cropenter"
            
            elif(self.cropMode == True and self.prevEdit != "cropenter"): # You were in crop mode but you didnt just literally enter into it. Will need to change how this behaves when gestures other than resize are given
                print("EXITING")
                self.cropMode = False
                self.prevEdit = "cropexit"

        elif(gesture == "rotate" and self.cropMode == False):
            self.editor.rotate(results)
            self.prevEdit = "rotate"
            
        
        elif(self.prevEdit != "none"):
            self.editor.setStart()
            #self.prevEdit = "none"
            


    def displayGesture(self): ## Method to display affirmative gesture feedback (Similar to what is currently under DEBUG)
        return
        
        