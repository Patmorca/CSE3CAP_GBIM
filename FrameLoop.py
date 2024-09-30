import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import customtkinter as CTk
from PIL import ImageTk, ImageEnhance, Image
import _tkinter as tk
import MPRecognition
import numpy as np
import math
from threading import Thread
import time


class GestureVision:
    
    def __init__(self,root,window,affirmation,model_data): ## Initialises all MP and CV variables and objects to be operated on
        
        self.activated = False

        self.frameCapture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpHandObject = self.mpHands.Hands()
        self.cursor_control_active = False
        self.doOverlay = False
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
        self.start_time = None
        self.end_time = None
        
        ## Editing ##
        self.opened = False # For making sure you cant open an image on an open image
        self.prevEdit = "none"
        self.cropMode = False
        self.editor = None
        self.history = None
        self.historyDoAdd = ["translate","crop","rotate","brightness","contrast","resize","undo","redo"]
        
    def updateFrame(self):

        success, frame = self.frameCapture.read()
        if success:

            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) ## OpenCV takes images in BGR format, this converts them into the proper RGB format for display and processing
            results = self.mpHandObject.process(frameRGB)
            
            gestureFrame = Image.fromarray(frameRGB)
            ppFrame = self.preProcess(gestureFrame) # Preprocessing to increase image sharpness, contrast

            if(results.multi_hand_landmarks):
                if(self.doOverlay):
                    for landmark in results.multi_hand_landmarks:
                        self.mpDrawing.draw_landmarks(frameRGB,landmark,self.mpHands.HAND_CONNECTIONS)              
                gestureFrame = Image.fromarray(frameRGB)

                if(self.runProcessing == 0):
                    gThread = Thread(target = self.recognizer.recognizeGesture,args = [ppFrame,results])
                    gThread.daemon = True
                    gThread.start()
                    self.runProcessing += 1
                    
                elif(self.runProcessing < 2):
                    self.runProcessing += 1
                    
                else:
                    self.runProcessing = 0
                    
            else:
                MPRecognition.gesture = "none"

            if(self.cropMode == False): ## Crop mode indicator
                self.affirmation.configure(text = MPRecognition.gesture)
            else:
                self.affirmation.configure(text = "crop")

            if(self.history):

                historyTop = self.history.check_top().cget("text")
                if(historyTop != self.prevEdit and MPRecognition.gesture in self.historyDoAdd and self.cropMode == False): ## adds the appropriate gestures to the history
                    if(self.prevEdit != "cropenter" and self.prevEdit != "cropexit"):
                        self.history.add_item(item = MPRecognition.gesture)              

            if(self.activated == False): ## this isolates pointer and open file as being able to be accessed whilst in the pre-import stage
                
                if(MPRecognition.gesture == "pointer"):
                    self.callFunction(MPRecognition.gesture,results)
                if(MPRecognition.gesture == "open file" and self.opened == False):
                    self.opened == True
                    MPRecognition.gesture = "none" # This forces the gesture out of recognition so that it doesnt repeatedly open windows
                    self.recognizer.clear_Buffer()
                    self.root.open_file()
            
            elif(self.activated == True):
                self.callFunction(MPRecognition.gesture,results)
                           
            resizedFrame = gestureFrame.resize((320,240),Image.Resampling.LANCZOS)
            displayFrame = CTk.CTkImage(resizedFrame, size= (320,240))
       
            ## return it to the tkinter widget in which we want to display it
       
            self.window.image = displayFrame
            self.window.configure(image=displayFrame)
            self.root.after(1,self.updateFrame)         
            
        else:
            return
       
    def preProcess(self,frame): # Preprocesses the frame for recognition - increases image sharpness and contrast
        contrastPreProcessor = ImageEnhance.Contrast(frame)
        cppFrame = contrastPreProcessor.enhance(1.3)
        sharpnessPreProcessor = ImageEnhance.Sharpness(cppFrame)
        scppFrame = sharpnessPreProcessor.enhance(1.75)
        return scppFrame
    
    def setActive(self):
        self.activated = True

    def setEditor(self,editor):
        self.editor = editor

    def setHistory(self,history):
        self.history = history
        
    def setOverlay(self):
        self.doOverlay = True
    
    def exitCrop(self):
        print("EXITING")
        self.cropMode = False
        self.editor.destroyCropBounds(True)
        self.editor.resetCropStage()

    def callFunction(self,gesture,results): ## This method will be called to check which function to call based on the contents of the buffer
        
        if(gesture == "resize"):
            if(self.cropMode == True):
                self.editor.crop(results)
                self.prevEdit = "cropsize"
            
            elif(self.cropMode == False):
                self.editor.resize(results)
                self.prevEdit = "resize"
        
        elif(gesture == "crop"):
            
            if(self.cropMode == False and self.prevEdit != "cropexit"): #If you didnt just exit crop
                self.cropMode = True
                self.editor.createCropBounds()
                self.prevEdit = "cropenter"
            
            elif(self.cropMode == True and self.prevEdit != "cropenter"): # You were in crop mode but you didnt just literally enter into it. Will need to change how this behaves when gestures other than resize are given
                print("EXITING")
                self.prevEdit = "cropexit"
                self.editor.destroyCropBounds(False)
                self.cropMode = False

        elif(gesture == "rotate"):
            if(self.cropMode == False):
                self.editor.rotate(results)
                self.prevEdit = "rotate"
            else:
                self.exitCrop()
        
        elif(gesture == "translate"):
            if(self.cropMode == False):
                self.editor.translate(results)
                self.prevEdit = "translate"
            else:
                self.exitCrop()
        
        elif(gesture == "brightness"):
            if(self.cropMode == False):
                self.editor.brightness(results)
                self.prevEdit = "brightness"
            else:
                self.exitCrop()

        elif(gesture == "contrast"):
            if(self.cropMode == False):
                self.editor.contrast(results)
                self.prevEdit = "contrast"
            else:
                self.exitCrop()
                                    
        elif(gesture == "undo"):
            if(self.cropMode == False):
                self.editor.undo()
                self.recognizer.clear_Buffer()
                self.prevEdit = "undo"
            else:
                self.exitCrop()
            
        elif(gesture == "redo"):
            if(self.cropMode == False):
                self.editor.redo()
                self.recognizer.clear_Buffer()
                self.prevEdit = "redo"
            else:
                self.exitCrop()
                
        elif(gesture == "pointer"):
            if(self.cropMode == False):
                self.editor.pointer(results)
                self.prevEdit = "pointer"
            else:
                self.exitCrop()
                
        elif(gesture == "brightness"):
            if(self.cropMode == False):
                self.editor.brightness(results)
                self.prevEdit = "brightness"
            else:
                self.exitCrop()
            
        elif(gesture == "save file"):
            self.recognizer.clear_Buffer()
            self.editor.save_file()
           
        elif(gesture == "help"): # Ditto as above
            self.root.open_help(self.history.check_top().cget("text"))
            MPRecognition.gesture = "none" # This forces the gesture out of recognition so that it doesnt repeatedly open windows
            self.recognizer.clear_Buffer()
                      
        elif(self.prevEdit != "none" and self.prevEdit != "undo" and self.prevEdit != "redo"):
            self.recognizer.clear_Buffer() ## Ensures we dont have hangover, adds a little bit of delay but the benefits outweight the cost here.
            self.editor.set_start(self.prevEdit)
            if(gesture == "none" or gesture == "open hand"):
                self.prevEdit = "none"
