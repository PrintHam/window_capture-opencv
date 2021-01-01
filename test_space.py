from window_capture import Window_Capture
import cv2 as cv
import time

# path to window that will be captured
window_path = r'Runescape'
wincap = Window_Capture(window_path)
loop_time = time.time()

# capturing the desired window
while True:
    output_screenshot = wincap.screenshare()
    
    # displays the output image on an opencv window
    cv.imshow('Result', output_screenshot)

    print("FPS: {}".format(round(1 / (time.time() - loop_time))))
    loop_time = time.time()

    if cv.waitKey(1) == ord('q'):
        print("Capture Ended")
        cv.destroyWindow(output_screenshot)
