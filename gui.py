import tkinter as tk
import pyautogui, threading, win32api
import sys, os, time, queue, configparser
from tkinter import ttk
from engine import healing, spellrotation as sr
from lib import windowTitles, utilities, hk



class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carnufex@Github")
        self.root.geometry('600x500')
        self.root.resizable(width=False, height=False)

        self.config_file_path = self.set_file_path()
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)

        self.checkButton_hk_bools = {}

        self.hotkey_checkButton_dict = {}
        self.all_spells_dict = {'attack': {}, 'heal': {}, 'utility': {}}
        self.all_bools = {}
        self.all_text_fields = {}




        self.hotkeys = []
        #loading all hk's into an array
        for item in self.config.items('HOTKEYS'):
            self.hotkeys.append(item[0])

        names = ['Hotkeys', 'Spell rotation', 'Healing', 'Config', 'Instructions']
        self.nb = self.create_notebook(self.root, names)
        self.menu = self.create_menus(self.root)


        self.title = None
        self.set_title()

    '''
    Finds filepath after compiling.
    '''
    def set_file_path(self):
        if getattr(sys, 'frozen', False): # we are running in a bundle
            bundle_dir = sys._MEIPASS # This is where the files are unpacked to
        else: # normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
        return bundle_dir + '\\config.ini'

    def update_config(self):
            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)


    '''
    finds all titles of visible windows, filters for "Tibia -" and returns full string.
    '''
    def set_title(self):
        try:
            self.title = windowTitles.find_tibia_title()
        except IndexError as e:
            print("You need to login before starting bot.")
            self.root.destroy()

    def thread_handler(self, button):
        button_name = button["text"]
        button_status = button.config('relief')[-1]
        if button_name == "Hotkeys":
            hk_thread = None
            if button_status == 'raised':
                #button pressed
                hk_thread = threading.Thread(target=hk_run)
                try:
                    print("Hotkeys enabled")
                    hk_thread.start()
                except:
                    print("Error: unable to start thread")
            else:
                print("Hotkeys disabled")
                #stop thread
                hk.stop()
                if hk_thread is not None:
                    hk_thread.join()
        elif button_name == "spell rotation":
            #print(self.checkButton_bools)
            spellrotation_thread = None
            if self.checkButton_hk_bools['spell_rotation'].get() is True:
                #button pressed
                # coords is loaded from file as strings, parsing back to tuple type.
                start_coords = utilities.string2tuple(self.config['GAMEWINDOW']['game_start_coords'])
                end_coords = utilities.string2tuple(self.config['GAMEWINDOW']['game_end_coords'])
                #spellrotation_thread = threading.Thread(target=spellrotation_run, args=(300, 'avalanche', 2, hotkey, start_coords, end_coords, config))
                spellrotation_thread = threading.Thread(target=spellrotation_run, args=(start_coords, end_coords, gui))
                try:
                    print("starting spell rotation")
                    spellrotation_thread.start()
                except:
                    print("Error: unable to start thread")
            else:
                #stop thread
                print("Stopping spell rotation")
                if spellrotation_thread is not None:
                    spellrotation_thread.join()
        elif button_name == "healing":
            healing_thread = None
            if self.checkButton_hk_bools['healing'].get() is True:
                healing_thread = threading.Thread(target=healing_run)
                try:
                    print("Starting healing")
                    healing_thread.start()
                except:
                    print("Error: unable to start healing thread.")
            else:
                print("Stopping healing")
                if healing_thread is not None:
                    healing_thread.join()



    def button_thread(self, button):
        if button.config('relief')[-1] == 'raised':
            self.thread_handler(button)
            if button.winfo_class() == 'Button':
                button["bg"] = "green"
                button.config(relief = 'sunken')
                print('raised')
        else:
            self.thread_handler(button)
            if button.winfo_class() == 'Button':
                print('sunken')
                button["bg"] = "red"
                button.config(relief = 'raised')

    def update_text(self, text_field, new_text):
        text_field.configure(state='normal')
        text_field.delete('1.0', 'end')
        text_field.insert('end', str(new_text))
        text_field.configure(state='disabled')

    '''
    Using Q to return something from a Thread instead of using multithreading; keeping old code

    Input:
    item : tuple containing var and value loaded from .ini
    text_field : tk.Text object

    Action:
    updated .ini file and value in GUI

    '''
    def update_click(self, item, text_field, section):
        print("updating: ", item, text_field)
        que = queue.Queue()
        mouse_thread = threading.Thread(target=lambda q, arg1: q.put(utilities.detect_mouse_click(arg1)), args=(que, 'test'))
        mouse_thread.start()
        result = que.get()
        mouse_thread.join()
        self.config.set(section, item[0], str(result))
        self.update_config()
        self.update_text(text_field, result)

    def update_anchors(self, item, text_field, section):
        start_coords_dict, end_coords_dict = healing.find_anchors()
        if item[0][7:] == 'end':
            self.config.set(section, item[0], str(end_coords_dict[item[0][:2]]))
            self.update_text(text_field, str(end_coords_dict[item[0][:2]]))
        else:
            self.config.set(section, item[0], str(start_coords_dict[item[0][:2]]))
            self.update_text(text_field, str(start_coords_dict[item[0][:2]]))

        self.update_config()

    def update_textField(self, stringVar, section, item):
        self.config.set(section, item, stringVar.get())
        # self.hotkey_checkButton_dict['healing'].invoke()
        self.update_config()
        stringVar.set(self.config[section][item])
        # self.hotkey_checkButton_dict['healing'].invoke()
        return True


    def update_hotkeys(self, category, item, amountObj=None):
        new_val = amountObj.get()
        #print('gui: {0}  category: {1}   item: {2}  new val: {3}'.format(GUI_obj, category, item, new_val))
        self.config.set(category, item, new_val)
        self.update_config()




    def create_notebook(self, root, names):
        nb = ttk.Notebook(root, width=590, height=450)
        nb.pack()

        # Create tabs & save them by name in a dictionary
        nb.tabs = {}
        for name in names:
            nb.tabs[name] = tab = ttk.Frame(root)
            nb.add(tab, text=name)

        def add_label(parent, text, row, column, columnspan=1, rowspan=1):
            label = tk.Label(parent, text=text)
            label.grid(row=row, column=column, sticky=tk.N, pady=10, columnspan=columnspan, rowspan=rowspan)
            return label

        def add_button_thread(parent, button_text, command, row, column, columnspan=1):
            button = tk.Button(parent, text=button_text, command=lambda: command(button), bg="red", relief="raised", width=14)
            button.grid(row=row, column=column, sticky=tk.N, pady=10, padx=10, columnspan=columnspan)
            return button

        def add_button_config(parent, button_text, command, item, text_field, section, row, column):
            button = tk.Button(parent, text=button_text, command=lambda: command(item, text_field, section), bg="grey", width=10)
            button.grid(row=row, column=column, sticky=tk.N, pady=10, padx=10)
            return button

        def add_checkButton_hk(parent, text, variable, command, row, column):
            try:
                variable = self.checkButton_hk_bools[text]
            except:
                print("Didn\'t find the bool connected to checkbox")
            check_button = tk.Checkbutton(parent, text=text.replace("_", " "), variable=variable, command=lambda: command(check_button), onvalue=True, offvalue=False)
            check_button.grid(row=row, column=column, sticky=tk.N, pady=10, padx=10)
            self.hotkey_checkButton_dict[text] = check_button
            return check_button

        def add_checkButton_spell(parent, spell, school, variable, row, column):
            check_button = tk.Checkbutton(parent, text=spell.replace("_", " "), variable=variable, onvalue=True, offvalue=False)
            check_button.grid(row=row, column=column, sticky=tk.N, pady=10, padx=10)
            spell_dict = self.all_spells_dict[school]
            spell_dict[spell] = check_button
            return check_button

        def add_text(parent, text, width, height, row, col, state='normal'):
            text_field = tk.Text(parent, width=width, height=height)
            text_field.insert('end', text)
            text_field.configure(state=state)
            text_field.grid(row=row, column=col, sticky=tk.N, pady=10, padx=10)
            parent.focus_set()
            return text_field

        def add_text_command(parent, stringVar, width, height, row, col, command, section, item, columnspan=1):
            e = tk.Entry(parent, textvariable=stringVar, validate="focusout", validatecommand=lambda: command(stringVar, section, item), width=width)
            e.grid(row=row, column=col, sticky=tk.N, pady=10, padx=10, columnspan=columnspan)
            return e


        def add_optionMenu(parent, variable, option_list, command, category, item, row, col):
            option = tk.OptionMenu(parent, variable, *option_list, command=lambda var: command(category, item, variable))
            option.grid(row=row, column=col, sticky=tk.N, pady=10, padx=10)



        def cooldown_window():
            window = tk.Toplevel(self.root)
            window.grid()
            window.title("Cooldowns")
            window.geometry('400x500')
            window.resizable(width=False, height=False)
            load_cooldowns(window)



        def load_cooldowns(parent):
            i = 0
            info = 'Press the top left corner of the cooldown.'
            add_label(parent, info, i, 0, 3)
            i += 1
            info = 'Attack CD\'s'
            add_label(parent, info, i, 0, 3)
            for item in self.config.items('ATTACK_COOLDOWNS'):
                i += 1
                name = item[0].replace("_", " ")
                name = name.lower()
                add_label(parent, name, i, 0)
                text_field = add_text(parent, item[1], 12, 1, i, 1, 'disabled')
                add_button_config(parent, 'update', self.update_click, item, text_field, 'ATTACK_COOLDOWNS', i ,2)
            i += 1
            info = 'Healing CD\'s'
            add_label(parent, info, i, 0, 3)
            i += 1
            for item in self.config.items('HEALING_COOLDOWNS'):
                name = item[0].replace("_", " ")
                name = name.lower()
                add_label(parent, name, i, 0)
                text_field = add_text(parent, item[1], 12, 1, i, 1, 'disabled')
                add_button_config(parent, 'update', self.update_click, item, text_field, 'HEALING_COOLDOWNS', i ,2)
                i += 1

        def load_config(parent):
            i = 0
            for item in self.config.items('GAMEWINDOW'):
                label = item[0].replace("_", " ")
                label = label.lower()
                add_label(parent, label, i, 0)
                text_field = add_text(parent, item[1], 12, 1, i, 1, 'disabled')
                add_button_config(parent, 'update', self.update_click, item, text_field, 'GAMEWINDOW', i, 2)
                i += 1
            for item in self.config.items('HP_AND_MANA_BAR'):
                label = item[0].replace("_", " ")
                label = label.lower()
                add_label(parent, label, i, 0)
                text_field = add_text(parent, item[1], 12, 1, i, 1, 'disabled')
                self.all_text_fields[item] = text_field
                add_button_config(parent, 'update', self.update_anchors, item, text_field, 'HP_AND_MANA_BAR', i, 2)
                i += 1
            #add_button_config(parent, 'update', self.update_anchors, item, text_field, 'HP_AND_MANA_BAR', i-2, 2)
            cooldown_button = tk.Button(parent, text="Cooldowns", command=cooldown_window)
            cooldown_button.grid(row=i, column=1, sticky=tk.N, pady=10, padx=10)

        def load_spell_settings(name):
            hotkey = tk.StringVar()
            amount = tk.StringVar()
            priority = tk.StringVar()
            range = tk.StringVar()
            for save in self.config.items('SAVED_HOTKEYS'):
                if name == save[0]:
                    hotkey.set(save[1])
                    break
                else:
                    hotkey.set('None')
            for save in self.config.items('AMOUNT'):
                if name == save[0]:
                    amount.set(save[1])
                    break
                else:
                    amount.set('None')
            for save in self.config.items('PRIORITY'):
                if name == save[0]:
                    priority.set(save[1])
                    break
                else:
                    priority.set('None')
            for save in self.config.items('RANGE'):
                if name == save[0]:
                    priority.set(save[1])
                    break
                else:
                    priority.set('None')
            return (hotkey, amount, priority, range)

        def load_hotkeys(parent):
            add_label(parent, 'Enable all hotkeys: ', 0, 0)
            add_button_thread(parent, "Hotkeys", self.button_thread, 0, 1, columnspan=3)
            hotkey = load_spell_settings('spell_rotation')[0]
            #spell rotation
            add_optionMenu(parent, hotkey, self.hotkeys, self.update_hotkeys, 'SAVED_HOTKEYS', 'spell_rotation', 1, 0)
            bool = tk.BooleanVar()
            self.checkButton_hk_bools['spell_rotation'] = bool
            add_checkButton_hk(parent, 'spell_rotation', self.checkButton_hk_bools['spell_rotation'], self.button_thread, 1, 1)
            #healing
            hotkey = load_spell_settings('healing')[0]
            add_optionMenu(parent, hotkey, self.hotkeys, self.update_hotkeys, 'SAVED_HOTKEYS', 'healing', 2, 0)
            bool = tk.BooleanVar()
            self.checkButton_hk_bools['healing'] = bool
            add_checkButton_hk(parent, 'healing', self.checkButton_hk_bools['healing'], self.button_thread, 2, 1)
            # heal friend
            hotkey = load_spell_settings('heal_friend')[0]
            add_optionMenu(parent, hotkey, self.hotkeys, self.update_hotkeys, 'SAVED_HOTKEYS', 'heal_friend', 3, 0)
            bool = tk.BooleanVar()
            self.checkButton_hk_bools['heal_friend'] = bool
            add_checkButton_hk(parent, 'heal_friend', self.checkButton_hk_bools['heal_friend'], self.button_thread, 3, 1)
            text = tk.StringVar()
            text.set(self.config.get('HEAL_FRIEND', 'names'))
            add_text_command(parent, text, 12, 1, 3, 2, self.update_textField, 'HEAL_FRIEND', 'names')




        def load_spell_rotation(parent):
            i = 1
            add_label(parent, 'Spell', i, 0)
            add_label(parent, 'Hotkey', i, 1)
            add_label(parent, 'Active', i, 2)
            add_label(parent, 'Min monsters', i, 3)
            add_label(parent, 'Priority', i, 4)
            add_label(parent, 'Range', i, 5)

            #iterating through every offensive attack
            for item in self.config.items('ATTACK_COOLDOWNS'):
                i += 1
                #saving checkBox variables
                bool = tk.BooleanVar()
                self.all_bools[item[0]] = bool
                # mapping saved hotkeys to hotkeys
                tk_hotkey, tk_amount, tk_priority, tk_range = load_spell_settings(item[0])
                #adding buttons
                text = tk.StringVar()
                text.set(self.config.get('SPELL_NAME', item[0]))
                add_text_command(parent, text, 12, 1, i, 0, self.update_textField, 'SPELL_NAME', item[0])
                add_optionMenu(parent, tk_hotkey, self.hotkeys, self.update_hotkeys, 'SAVED_HOTKEYS', item[0], i, 1)
                # item[0] is the key for tuple
                add_checkButton_spell(parent, item[0], 'attack' ,self.all_bools[item[0]], i, 2)
                add_optionMenu(parent, tk_amount, [str(i) for i in range(10)], self.update_hotkeys, 'AMOUNT', item[0], i, 3)
                add_optionMenu(parent, tk_priority, [str(i) for i in range(10)], self.update_hotkeys, 'PRIORITY', item[0], i, 4)
                add_optionMenu(parent, tk_range, [str(i) for i in range(10)], self.update_hotkeys, 'RANGE', item[0], i, 5)
            i += 1
            add_label(parent, 'Monsters: ', i, 0)
            text = tk.StringVar()
            text.set(self.config.get('MONSTERS', 'list'))
            add_text_command(parent, text, 60, 1, i, 1, self.update_textField, 'MONSTERS', 'list', 5)


        def load_healing(parent):
            i = 1
            add_label(parent, 'Hotkey', i, 0)
            add_label(parent, '%', i, 1)
            add_label(parent, 'Active', i, 2)

            for item in self.config.items('HEALING_COOLDOWNS'):
                i += 1
                bool = tk.BooleanVar()
                self.all_bools[item[0]] = bool

                tk_hotkey = tk.StringVar()
                for save in self.config.items('SAVED_HOTKEYS'):
                    if item[0] == save[0]:
                        tk_hotkey.set(save[1])
                        break
                    else:
                        tk_hotkey.set('None')
                for save in self.config.items('SAVED_VALUES'):
                    text = tk.StringVar()
                    if item[0] == save[0]:
                        text.set(save[1])
                        tf = save[1]
                        break
                    else:
                        text.set(0)
                        tf = 0
                add_optionMenu(parent, tk_hotkey, self.hotkeys, self.update_hotkeys, 'SAVED_HOTKEYS', item[0], i, 0)
                add_text_command(parent, text, 4, 1, i, 1, self.update_textField, 'SAVED_VALUES', item[0])
                #add_text(parent, tf, 12, 1, i, 1)
                add_checkButton_spell(parent, item[0], 'heal', self.all_bools[item[0]], i, 2)





        # hotkeys tab
        tab = nb.tabs['Hotkeys']
        load_hotkeys(tab)

        #spell rotation tabs
        tab = nb.tabs['Spell rotation']
        load_spell_rotation(tab)



        # healing tab
        tab = nb.tabs['Healing']
        load_healing(tab)

        # config tab
        tab = nb.tabs['Config']
        load_config(tab)




        # for i in range(3):
        #     add_label(tab, 'm' + str(i), i, i)

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

#def spellrotation_run(radius, rune, min_monsters, hotkey, start_coords, end_coords, config):
def spellrotation_run(start_coords, end_coords, gui):
    utilities.find_cds(gui)
    targets = utilities.get_monster_list(gui)
    print(targets)
    pressed = gui.checkButton_hk_bools['spell_rotation'].get()
    while pressed:
        sr.spellrotation(start_coords, end_coords, gui, targets)
        pressed = gui.checkButton_hk_bools['spell_rotation'].get()


def healing_run():
    healing.find_anchors()
    for item in gui.config.items('HP_AND_MANA_BAR'):
        if item[1] == '[]':
            print("GO CONFIG AND UPDATE YOUR HP/MANA SETTINGS")
            gui.hotkey_checkButton_dict['healing'].invoke()
            break
    pressed = gui.checkButton_hk_bools['healing'].get()
    while pressed:
        healing.run(gui)
        pressed = gui.checkButton_hk_bools['healing'].get()


gui = GUI()
utilities.find_cds(gui)
gui.root.mainloop()
