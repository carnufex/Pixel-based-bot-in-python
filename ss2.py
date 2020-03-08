from gi.repository import Gdk

win = Gdk.get_default_root_window()
h = win.get_height()
w = win.get_width()

print ("The size of the window is %d x %d" % (w, h))

pb = Gdk.pixbuf_get_from_window(win, 0, 0, w, h)

if (pb != None):
    pb.savev("screenshot.png","png", (), ())
    print("Screenshot saved to screenshot.png.")
else:
    print("Unable to get the screenshot.")