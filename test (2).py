import win32api
import win32con

def send_input_hax(hwnd, msg):
    for c in msg:
        if c == "\n":
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)

send_input_hax(658650, "hej")

#hwnd = win32gui.GetForegroundWindow()
