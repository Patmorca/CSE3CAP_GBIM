from enum import Enum

class Gesture(Enum):
        ROTATE = "Rotate"
        CROP = "Crop"
        RESIZE = "Resize"
        TRANSLATE = "Translate"
        CONTRAST = "Contrast"
        BRIGHTNESS = "Brightness"
        POINTER = "Pointer"
        PEN = "Pen"
        CLOSE = "Close"
        SAVEFILE = "Save File"
        OPENFILE = "Open File"
        OPENHAND = "Open Hand"
        CLOSEDHAND = "Closed Hand"
        HELP = "Help"
        def gesture_help(cls):
            gestureHelp = {
                    Gesture.ROTATE: "This is the help text for rotate",
                    Gesture.CROP: "This is the help text for Crop, Crop crop crop",
                    Gesture.RESIZE: "This is the help text for RESIZE",
                    Gesture.TRANSLATE :"Translate Help text",
                    Gesture.CONTRAST :"Contrast Help text contrast",
                    Gesture.BRIGHTNESS: "This is the help text for brightness, blah blah brightness",
                    Gesture.POINTER: "This is the help text for POINTER, blah blah POINTER",
                    Gesture.PEN: "This is the help text for PEN, blah blah PEN",
                    Gesture.CLOSE: "Close",
                    Gesture.SAVEFILE: "Save File",
                    Gesture.OPENFILE: "This is the help text for openfile, blah blah openfiles",
                    Gesture.OPENHAND: "This is the help text for OPENHANDs, blah blah OPENHANDess",
                    Gesture.CLOSEDHAND: "This is the help text for CLOSEDHAND, blah blah CLOSEDHAND",
                    Gesture.HELP: "This is the help text for briHELP, blah blah HELP"
            }
            return gestureHelp[cls]
        def gesture_image(cls):
            gestureImage = {
                    Gesture.ROTATE: "Resources\RotateStatic.png",
                    Gesture.CROP: "Resources\CropStatic.png",
                    Gesture.RESIZE: "Resources\ResizeStatic.png",
                    Gesture.TRANSLATE :"Resources\TranslateStatic.png",
                    Gesture.CONTRAST :"Resources\ContrastStatic.png",
                    Gesture.BRIGHTNESS: "Resources\BrightnessStatic.png",
                    Gesture.POINTER: "Resources\PointerStatic.png",
                    Gesture.PEN: "Resources\PenStatic.png",
                    Gesture.CLOSE: "Resources\BrightnessStatic.png",
                    Gesture.SAVEFILE: "Resources\SaveStatic.png",
                    Gesture.OPENFILE: "Resources\OpenStatic.png",
                    Gesture.OPENHAND: "Resources\BrightnessStatic.png",
                    Gesture.CLOSEDHAND: "Resources\BrightnessStatic.png",
                    Gesture.HELP: "Resources\HelpStatic.png"
            }
            return gestureImage[cls]
        def gesture_gif(cls):
            gestureGif = {
                    Gesture.ROTATE: "Resources\Rotate.gif",
                    Gesture.CROP: "Resources\Crop.gif",
                    Gesture.RESIZE: "Resources\Resize.gif",
                    Gesture.TRANSLATE :"Resources\Translate.gif",
                    Gesture.CONTRAST :"Resources\Contrast.gif",
                    Gesture.BRIGHTNESS: "Resources\Brightness.gif",
                    Gesture.POINTER: "Resources\Pointer.gif",
                    Gesture.PEN: "Resources\Pen.gif",
                    Gesture.CLOSE: "Resources\Brightness.gif",
                    Gesture.SAVEFILE: "Resources\Save.gif",
                    Gesture.OPENFILE: "Resources\Open.gif",
                    Gesture.OPENHAND: "Resources\Brightness.gif",
                    Gesture.CLOSEDHAND: "Resources\Brightness.gif",
                    Gesture.HELP: "Resources\Help.gif"
            }
            return gestureGif[cls]
        def string_to_enum(string):
            string = string.replace(" ", "")
            string = string.upper()
            return Gesture.__members__.get(string)

#print(Gesture.BRIGHTNESS.value + " = " +Gesture.gesture_help(Gesture.BRIGHTNESS))

#print(Gesture.string_to_enum("Help"))

#print(Gesture.gesture_image(Gesture.HELP))