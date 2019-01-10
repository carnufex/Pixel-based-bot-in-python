import win32gui
import win32ui
from ctypes import windll
from PIL import Image

hwnd = win32gui.FindWindow(None, 'Archlight (NA) - Flippad Mage')
win32gui.SetForegroundWindow(hwnd)
win32gui.ShowWindow(hwnd, 9)

# Change the line below depending on whether you want the whole window
# or just the client area.
#left, top, right, bot = win32gui.GetClientRect(hwnd)
left, top, right, bot = win32gui.GetWindowRect(hwnd)
print(left, top, right, bot)
w = right - left
h = bot - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

# Change the line below depending on whether you want the whole window
# or just the client area.
#result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
print(result)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

if result == 1:
    #PrintWindow Succeeded
    im.save("testpic.png")


# from pywinauto import Application
# #app = application.Application().start("notepad.exe")
# app = Application().connect(process=16684)
# dlg = app.top_window()
# app.dlg.print_control_identifiers()
# #app.dlg.capture_as_image().save('window.png')
