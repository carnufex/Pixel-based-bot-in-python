import win32api, win32con, win32gui, win32ui, win32service, os, time

def send_click_input(pycwnd, x ,y):
    lParam = int(y) <<16 | int(x)
    pycwnd.SendMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam);
    pycwnd.SendMessage(win32con.WM_LBUTTONUP, 0, lParam);

def get_whndl(title):
    whndl = win32gui.FindWindowEx(0, 0, None, title)
    return whndl

def make_pycwnd(hwnd):
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

hotkey_dict = { 'f1': win32con.VK_F1,
                'f2': win32con.VK_F2,
                'f3': win32con.VK_F3,
                'f4': win32con.VK_F4,
                'f5': win32con.VK_F5,
                'f6': win32con.VK_F6,
                'f7': win32con.VK_F7,
                'f8': win32con.VK_F8,
                'f9': win32con.VK_F9,
                'f10': win32con.VK_F10,
                'f11': win32con.VK_F11,
                'f12': win32con.VK_F12
                }

def send_keyboard_input(pycwnd, hotkey=None, msg=None):
    #send_click_input(pycwnd, 15, 15)
    if hotkey.lower() in hotkey_dict:
        pycwnd.SendMessage(win32con.WM_KEYDOWN, hotkey_dict[hotkey.lower()], 0)
        pycwnd.SendMessage(win32con.WM_KEYUP, hotkey_dict[hotkey.lower()], 0)
    elif msg is not None:
        for c in msg:
            if c == "\n":
                pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)
        pycwnd.UpdateWindow()

# whndl = get_whndl('Tibia - George sadfrog')
# print("whndl: ", whndl)

### NEEDED IF WINDOW HAS CHILDS ###
# def callback(hwnd, hwnds):
#     if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
#         hwnds[win32gui.GetClassName(hwnd)] = hwnd
#     return True
#

# hwnds = {}
# win32gui.EnumChildWindows(whndl, callback, hwnds)
# print("hwnds: ", hwnds)
# whndl = hwnds['Edit']

# pycwnd = make_pycwnd(whndl)
# msg = "It works !\n"
# msg = "f11"
# send_keyboard_input(pycwnd,msg)
# send_click_input(pycwnd, 1170, 550)




def send_key(hotkey, msg=None, title=None):
    whndl = get_whndl(title)
    pycwnd = make_pycwnd(whndl)
    send_keyboard_input(pycwnd, hotkey, msg)

def send_click(x, y, title):
    whndl = get_whndl(title)
    pycwnd = make_pycwnd(whndl)
    send_click_input(pycwnd, x, y)

# https://docs.microsoft.com/sv-se/windows/desktop/inputdev/virtual-key-codes
#send_input('Tibia -', 'f11')
