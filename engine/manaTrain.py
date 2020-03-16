from engine import healing
from lib import sendInput, utilities
import random
import time
import pyautogui

NEXT_RUNE = time.time()

def use(hotkey, gui):
    sendInput.send_key(hotkey, title=gui.title)
    time.sleep(random.uniform(1.0, 2.0))

def check_mana():
    mp = healing.get_curr('mp_empty', 10)
    if mp is None:
        mp = 100
    return mp

def use_cask(gui):
    location = utilities.string2tuple(gui.config.get('MANA_TRAIN', 'cask'))
    utilities.setFocusWindow(gui)
    pyautogui.click(x=location[0], y=location[1], button='right')
    # sendInput.send_click(location[0], location[1], button="right", title=gui.title)

def get_mana(gui):
    mppc = check_mana()
    hk = gui.config.get('MANA_TRAIN', 'mana_hotkey')
    value = int(gui.config.get('MANA_TRAIN', 'pot_mppc'))
    count = 0
    while mppc < value:
        count += 1
        use(hk, gui)
        mppc = check_mana()
        if count > 20: #probably no more manas, use casks
            use_cask(gui)

def make_rune(gui):
    mppc = check_mana()
    hk = gui.config.get('MANA_TRAIN', 'rune_hotkey')
    use(hk, gui)


def mana_train(gui):
    amount = random.randint(1, 12)
    print("Making {0} runes.".format(amount))
    soul_cost = int(gui.config.get('MANA_TRAIN', 'soul_cost'))
    start = time.time()
    for i in range(amount):
        get_mana(gui)
        make_rune(gui)
    end = time.time()
    # 15 seconds per soul point - the time consumed to create the runes
    return time.time() + (amount * soul_cost * 14) - (end-start)

def waste_mana(gui):
    '''mana train'''
    amount = random.randint(1,5)
    print("wasting mana {} times.".format(amount))
    for i in range(amount):
        spam_one = gui.config.get('SAVED_HOTKEYS', 'spam_one')
        spam_two = gui.config.get('SAVED_HOTKEYS', 'spam_two')
        use(spam_one, gui)
        use(spam_two, gui)
    get_mana(gui)

def eat_food(gui):
    '''eats food'''
    amount = random.randint(3, 8)
    food_hk = gui.config.get('SAVED_HOTKEYS', 'food_hotkey')
    for i in range(amount):
        use(food_hk, gui)


def run(gui):
    '''runs thread'''
    global NEXT_RUNE
    now = time.time()
    if now > NEXT_RUNE:
        NEXT_RUNE = mana_train(gui)
        eat_food(gui)
    elif gui.all_bools['mana_train_spam'].get():
        waste_mana(gui)
    time.sleep(1)




# 1 check mana

# looping
# check mana
#

# 2 use hk X-Y times

# 3 wait 15s * soul req

# 4 eat food?

# 5 click cask
