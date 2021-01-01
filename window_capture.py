import numpy
import win32gui, win32ui, win32con


class Window_Capture:
    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    hwnd = None

    def __init__(self, window_name=None):

        if window_name is None:
            print("No window set to capture: Setting to active Window")
            self.hwnd = win32gui.GetDesktopWindow()
            print(win32gui.GetWindowText(win32gui.GetDesktopWindow()))


        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window could not be found [Window Name: {}]".format(window_name))
            print("Window Found: Setting to preferred Window")

        # define monitor height and width and hwnd

        window_size = win32gui.GetWindowRect(self.hwnd)
        self.w = window_size[2] - window_size[0]
        self.h = window_size[3] - window_size[1]

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_size[0] + self.cropped_x
        self.offset_y = window_size[1] + self.cropped_y

    def screenshare(self):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = numpy.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # dcObj.DeleteDC()
        # cDC.DeleteDC()
        # win32gui.ReleaseDC(self.hwnd, wDC)
        # win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = numpy.ascontiguousarray(img)

        return img

    # getting a list of all the windows
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y
