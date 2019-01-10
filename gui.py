from tkinter import *
import archlight_me as arc
import threading
import time
import hk
import gfb


class Gui:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button_width = 14

        self.lf1 = LabelFrame(frame, text="Hotkeys")
        self.lf1.pack(fill="x", expand="yes")

        self.printButton = Button(frame, text="print message", command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.essence_toggle = Button(frame, text="Start essence bot", command=self.start_essence, bg="red", relief="raised", width=self.button_width)
        self.essence_toggle.pack(side=LEFT)

        self.hk_mode_toggle = Button(self.lf1, text="Enable Hotkeys", command=self.hk_mode, bg="red", relief="raised", width=self.button_width)
        self.hk_mode_toggle.pack()

        self.gfb_bool = BooleanVar()
        self.gfb_checkbutton = Checkbutton(self.lf1, text="gfb", variable=self.gfb_bool, command=self.gfb_hk, onvalue=True, offvalue=False)
        self.gfb_checkbutton.pack()

        self.ss_mode = Checkbutton(self.lf1, text="screenshot")
        self.ss_mode.select()
        self.ss_mode.pack()




    def printMessage(self):
        print("var= ", self.gfb_bool.get())

    def start_essence(self):
        essence_bot_thread = None
        if self.essence_toggle.config('relief')[-1] == 'raised':
            #start thread
            essence_bot_thread = threading.Thread(target=eb_run, args=(5,))
            try:
                print("starting essence bot")
                essence_bot_thread.start()
            except:
                print("Error: unable to start thread")
            #update button
            self.essence_toggle.config(relief = 'sunken')
            self.essence_toggle["text"] = "Stop essence bot"
            self.essence_toggle["bg"] = "green"
        else:
            #stop thread
            if essence_bot_thread is not None:
                essence_bot_thread.join()
            print("Stopped essence bot")
            #update button
            self.essence_toggle.config(relief = 'raised')
            self.essence_toggle["text"] = "Start essence bot"
            self.essence_toggle["bg"] = "red"

    def hk_mode(self):
        hk_thread = None
        if self.hk_mode_toggle.config('relief')[-1] == 'raised':
            #button pressed
            hk_thread = threading.Thread(target=hk_run)
            try:
                print("starting hk's")
                hk_thread.start()
            except:
                print("Error: unable to start thread")
            #update button
            self.hk_mode_toggle.config(relief = 'sunken')
            self.hk_mode_toggle["text"] = "Disable Hotkeys"
            self.hk_mode_toggle["bg"] = "green"
        else:
            #stop thread
            hk.stop()
            if hk_thread is not None:
                hk_thread.join()
            #update button
            self.hk_mode_toggle.config(relief = 'raised')
            self.hk_mode_toggle["text"] = "Enable Hotkeys"
            self.hk_mode_toggle["bg"] = "red"

    def gfb_hk(self):
        gfb_hk_thread = None
        if self.gfb_bool.get() is True:
            #button pressed
            gfb_hk_thread = threading.Thread(target=gfb_run, args=(400, 2))
            try:
                print("starting gfb hk")
                gfb_hk_thread.start()
            except:
                print("Error: unable to start thread")
        else:
            #stop thread
            if gfb_hk_thread is not None:
                gfb_hk_thread.join()

def eb_run(loop_delay):
    pressed = b.essence_toggle.config('relief')[-1] == 'sunken'
    while pressed:
        arc.eb(loop_delay)

def gfb_run(radius, min_monsters):
    pressed = b.gfb_bool.get()
    print("pressed: ", pressed)
    while pressed:
        gfb.run(radius, min_monsters)
        pressed = b.gfb_bool.get()

def hk_run():
    hk.start(b)

root = Tk()
b = Gui(root)
root.mainloop()
