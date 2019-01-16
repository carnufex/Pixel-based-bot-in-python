import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        root = tk.Tk()
        root.title("SC")
        root.geometry('400x500')
        root.resizable(width=False, height=False)

        names = ['Title', 'Graphs', 'Messages', 'Instructions']
        self.nb = self.create_notebook(root, names)
        self.menu = self.create_menus(root)

        # We can also add items to the Notebook here
        tab = self.nb.tabs['Instructions']
        tk.Label(tab, text='You should\nread these\ninstructions').pack()

        btn = tk.Button(root, text='Click', command=self.button_command)
        btn.pack()
        test(GUI.names)

        root.mainloop()

    def button_command(self):
        print('The button was clicked')

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

        # Add some labels to each tab
        tab = nb.tabs['Title']
        for i in range(3):
            add_label(tab, 't' + str(i), i, 0)

        tab = nb.tabs['Graphs']
        for i in range(3):
            add_label(tab, 'g' + str(i), 0, i)

        tab = nb.tabs['Messages']
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

def test(gui):
    print(gui)


GUI()
