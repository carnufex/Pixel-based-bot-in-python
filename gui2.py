import tkinter as tk
from tkinter import ttk
import threading
import gfb
import hk

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SC")
        self.root.geometry('400x500')
        self.root.resizable(width=False, height=False)

        self.gfb_bool = tk.BooleanVar()
        self.hotkey_arr = []

        names = ['Hotkeys', 'Healing', 'Config', 'Instructions']
        self.nb = self.create_notebook(self.root, names)
        self.menu = self.create_menus(self.root)




        # We can also add items to the Notebook here
        # tab = self.nb.tabs['Instructions']
        # tk.Label(tab, text='You should\nread these\ninstructions').pack()

        # btn = tk.Button(root, text='Click', command=self.button_command)
        # btn.pack()

        #root.mainloop()

    def thread_handler(self, button):
        button_name = button["text"]
        button_status = button.config('relief')[-1]
        if button_name == "Hotkeys":
            if button_status == 'raised':
                #button pressed
                hk_thread = threading.Thread(target=hk_run)
                try:
                    print("starting hk's")
                    hk_thread.start()
                except:
                    print("Error: unable to start thread")
            else:
                #stop thread
                hk.stop()
        elif button_name == "GFB":
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



    def button_command(self, button):
        if button.config('relief')[-1] == 'raised':
            self.thread_handler(button)
            button["bg"] = "green"
            button.config(relief = 'sunken')
            print('raised')
        else:
            self.thread_handler(button)
            print('sunken')
            button["bg"] = "red"
            button.config(relief = 'raised')



    def create_notebook(self, root, names):
        nb = ttk.Notebook(root, width=390, height=450)
        nb.pack()

        # Create tabs & save them by name in a dictionary
        nb.tabs = {}
        for name in names:
            nb.tabs[name] = tab = ttk.Frame(root)
            nb.add(tab, text=name)

        def add_label(parent, text, row, column):
            label = tk.Label(parent, text=text)
            label.grid(row=row, column=column, sticky=tk.N, pady=10)
            return label

        def add_button(parent, button_text, command, row, column):
            button = tk.Button(parent, text=button_text, command=lambda: command(button), bg="red", relief="raised", width=14)
            button.grid(row=row, column=column, sticky=tk.N, pady=10)
            return button

        def add_checkButton(parent, text, variable, command, row, column):
            check_button = tk.Checkbutton(parent, text=text, variable=variable, command=lambda: command(check_button), onvalue=True, offvalue=False)
            check_button.grid(row=row, column=column, sticky=tk.N, pady=10)
            self.hotkey_arr.append((check_button["text"], check_button))
            return check_button

        # Add some labels to each tab
        tab = nb.tabs['Hotkeys']
        for i in range(2):
            add_label(tab, 't' + str(i), i, 0)
        add_label(tab, 'HOTKEYS:    ', 3, 1)
        add_button(tab, "Hotkeys", self.button_command, 3, 2)
        add_checkButton(tab, 'GFB', self.gfb_bool, self.button_command, 4, 1)

        tab = nb.tabs['Healing']
        for i in range(3):
            add_label(tab, 'g' + str(i), 0, i)

        tab = nb.tabs['Config']
        for i in range(3):
            add_label(tab, 'm' + str(i), i, i)

        return nb

    def create_menus(self, root):
        menu = tk.Menu(root, tearoff=False)
        root.config(menu=menu)
        subMenu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_separator()
        subMenu.add_command(label='Exit', command=root.destroy)
        return menu


def hk_run():
    hk.start(gui)

def gfb_run(radius, min_monsters):
    pressed = gui.gfb_bool.get()
    print("pressed: ", pressed)
    while pressed:
        gfb.run(radius, min_monsters)
        pressed = gui.gfb_bool.get()

gui = GUI()
gui.root.mainloop()
