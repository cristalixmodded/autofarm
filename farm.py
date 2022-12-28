import time
import pyautogui
import configparser

config = configparser.ConfigParser()
config.read_file(open(r'config.ini'))
ores_warp = config.get('Config', 'ores_warp')
ores_slot = config.get('Config', 'ores_slot')
mobs_warp = config.get('Config', 'mobs_warp')
mobs_slot = config.get('Config', 'mobs_slot')
delay = config.get('Config', 'delay') * 60

def farm(warp, slot, click_range, time_sleep):
    for _ in range(2):
        pyautogui.press('t')
        pyautogui.typewrite("/warp " + warp, interval=0.25)
        pyautogui.press('enter')
   
    pyautogui.press(slot)
    for _ in range(click_range):
        pyautogui.leftClick()
        time.sleep(time_sleep)
        
def start_farm():
    time.sleep(10)
    
    farm(ores_warp, ores_slot, 6, 5)
    farm(mobs_warp, mobs_slot, 12, 10)
    time.sleep(delay)