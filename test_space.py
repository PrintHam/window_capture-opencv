from window_capture import Window_Capture
import cv2 as cv
from image_positions import Image_Process
import pyautogui
import time
from hsvfilter import HsvFilter

# this file is used for testing hsv settings

window_path = r'Runescape'

# capturing the desired window
wincap = Window_Capture(window_path)

osr_rock = Image_Process('processed mob 1.JPG')
wincap.list_window_names()
# opens the hsv filter gui : window can be used to adjust hsv settings
osr_rock.init_control_gui()

pyautogui.FAILSAFE = False

loop_time = time.time()
hsvfilter = HsvFilter(21, 0, 0, 179, 255, 255, 0, 255, 255, 0)
while True:
    output_screenshot = wincap.screenshare()

    hsv_image = osr_rock.apply_hsv_filter(output_screenshot, hsv_filter=hsvfilter)

    # fetching positions of all needle image locations in the screenshot
    # 0.5 represents the threshold level that the confidence % must be above or at in order for it
    # to be considered a possible location
    rectangles = osr_rock.imagepositions(hsv_image, 0.34)

    # draws a rectangle for each image that is a possible match
    final_image = osr_rock.show_rectangles(hsv_image, rectangles)

    # displays the output image on an opencv window
    cv.imshow('Result', final_image)

    print("FPS: {}".format(round(1 / (time.time() - loop_time))))

    loop_time = time.time()

    if cv.waitKey(1) == ord('q'):
        print("Capture Ended")
        cv.destroyWindow(output_screenshot)
