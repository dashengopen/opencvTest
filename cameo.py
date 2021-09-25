import cv2
from manager import CaptureManager, WindowManager

class Cameo:
    def __init__(self):
        self.window = WindowManager("test", self.onKeypress)
        self.capture = CaptureManager(cv2.VideoCapture("/home/dasheng/Videos/01.rmvb"), self.window, False)
        return

    def run(self):
        self.window.createWindow()
        while self.window.windowCreated:
            self.capture.enterFrame()
            frame = self.capture.currentFrame()
            self.capture.exitFrame()
            self.window.registerEvent()
        return

    def onKeypress(self, keycode):
        if keycode == 9:
            if self.capture.videoFilename is None:
                self.capture.videoFilename = "capture.avi"
                print("record start...")
            else:
                self.capture.videoFilename = None
                self.capture.videoWriter = None
                print("record end")
        elif keycode == 32:
            self.capture.imageFilename = "screen.png"
            print("sceen successfully")
        elif keycode == 27:
            self.window.destroyWindow()


if __name__ == "__main__":
    Cameo().run()