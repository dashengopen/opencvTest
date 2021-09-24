import cv2

class CaptureManager:
    def __init__(self):
        return

    def enterFrame(self):
        return

    def exitFrame(self):
        return

class WindowManager:
    def __init__(self, windowName, myCallback):
        self.windowCreated = False
        self.windowName = windowName
        self.callback = myCallback
        return

    def createWindow(self):
        cv2.namedWindow(self.windowName)
        self.windowCreated = True
        return
    
    def destroyWindow(self):
        cv2.destroyWindow(self.windowName)
        self.windowCreated = False
        return
    
    def show(self):
        return
    
    def registerEvent(self):
        return