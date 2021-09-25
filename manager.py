import cv2
import time
import numpy

class CaptureManager:
    def __init__(self, capture, window, isMirrored):
        self.channel = 0
        self.window = window
        self.isMirrored = isMirrored

        self.frame = None
        self.enteredFrame = False
        
        self.imageFilename = None
        
        self.videoFilename = None
        self.videoCapture = capture
        self.videoWriter = None
        self.videoEncoder = cv2.VideoWriter_fourcc('I', '4', '2', '0')

        self.frameElapsed = 0
        self.fpsEstimated = 0.0
        self.frameStartTime = 0
        
        return
    
    def currentFrame(self):
        if self.enteredFrame and self.frame is None:
            _, self.frame = self.videoCapture.read()
        return self.frame

    def enterFrame(self):
        assert not self.enteredFrame, "enter failed"
        if self.videoCapture is not None:
            self.enteredFrame = True
        return

    def exitFrame(self):
        if self.frame is None:
            self.enteredFrame = False
            return

        if self.frameElapsed == 0:
            self.frameStartTime = time.time()  
        else:
            timeElapsed = time.time() - self.frameStartTime
            self.fpsEstimated = self.frameElapsed / timeElapsed
        self.frameElapsed += 1

        if self.window is not None:
            if self.isMirrored:
                mirroredFrame = numpy.fliplr(self.frame).copy()
                self.window.show(mirroredFrame)
            else:
                self.window.show(self.frame)

        if self.imageFilename is not None:
            cv2.imwrite(self.imageFilename, self.frame)
            self.imageFilename = None
        if self.videoFilename is not None:
            if self.videoWriter is None:
                fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
                if fps == 0.0:
                    if self.frameElapsed < 20:
                        return
                    else:
                        fps = self.fpsEstimated
                size = (int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                self.videoWriter = cv2.VideoWriter(self.videoFilename, self.videoEncoder, self.fpsEstimated, size)
            self.videoWriter.write(self.frame)

        self.frame = None
        self.enteredFrame = False
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
        return self.windowCreated
    
    def destroyWindow(self):
        cv2.destroyWindow(self.windowName)
        self.windowCreated = False
        return
    
    def show(self, frame):
        cv2.imshow(self.windowName, frame)
        return
    
    def registerEvent(self):
        keycode = cv2.waitKey(1)
        if self.callback is not None and keycode != -1:
            keycode &= 0xFF
            self.callback(keycode)
        return