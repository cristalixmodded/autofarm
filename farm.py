import time
import pyautogui
import configparser

config = configparser.ConfigParser()
config.read_file(open(r'config.ini'))
ores_warp = config.get('Config', 'ores_warp')
ores_slot = config.get('Config', 'ores_slot')
mobs_warp = config.get('Config', 'mobs_warp')
mobs_slot = config.get('Config', 'mobs_slot')
delay = config.get('Config', 'delay')
delay = int(delay) * 60

def farm(warp, slot, click_range, time_sleep):
    for _ in range(2):
        pyautogui.press('t')
        pyautogui.typewrite(warp, interval=0.25)
        pyautogui.press('enter')
   
    pyautogui.press(slot)
    for _ in range(click_range):
        pyautogui.leftClick()
        time.sleep(time_sleep)
        
def start_farm():
    while True:
        time.sleep(10)
        
        farm('/warp ' + ores_warp, ores_slot, 6, 5)
        farm('/warp ' + mobs_warp, mobs_slot, 12, 10)
        farm('/home', '5', 1, 1)
        
        time.sleep(delay)
