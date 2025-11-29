import pyautogui
import time
import keyboard
import sys, os
import cv2
import numpy as np

# ----------------- настройки -----------------
CONF        = 0.5
LOOP_DELAY  = 1.0

BASE = getattr(sys, '_MEIPASS', os.path.abspath('.'))
def img(path):
    return os.path.join(BASE, path)

# ----------------- старые функции -----------------
def wait_and_hold_key(image, key, hold_time):
    while True:
        try:
            pos = pyautogui.locateOnScreen(img(image), confidence=CONF)
            if pos:
                print(f"[+] Найдено: {image} → удерживаю {key} {hold_time}с")
                pyautogui.keyDown(key)
                time.sleep(hold_time)
                pyautogui.keyUp(key)
                return
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(LOOP_DELAY)

def wait_and_click(image):
    while True:
        try:
            pos = pyautogui.locateOnScreen(img(image), confidence=CONF)
            if pos:
                print(f"[+] Найдено: {image} → клик")
                pyautogui.click(pos)
                return
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(LOOP_DELAY)

def wait_and_hold_lmb(image, hold_time):
    while True:
        try:
            pos = pyautogui.locateOnScreen(img(image), confidence=CONF)
            if pos:
                print(f"[+] Найдено: {image} → удерживаю ЛКМ {hold_time}с")
                pyautogui.mouseDown(button='left')
                time.sleep(hold_time)
                pyautogui.mouseUp(button='left')
                return
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(LOOP_DELAY)

# ----------------- основной цикл (ЧИСТЫЙ ЛИСТ) -----------------
print("Бот запущен. Нажми Ctrl+C для остановки.")
try:
    while True:
        # 1. начало боя (без изменений)
        wait_and_hold_key('images/1.png', 'e', 2)
        wait_and_click('images/2.png')
        wait_and_hold_lmb('images/5.png', 2)

        # 2. ПОСЛЕ 5.png – ПУСТО, ждём твоей команды
                # 2. после начала боя: ждём 5 сек, затем E-Q-F с интервалом 1 сек
        print("[+] Ждём 5 сек после начала боя...")
        time.sleep(5.0)
        print("[+] Нажимаем E-Q-F с интервалом 1 сек")
        keyboard.send('e'); time.sleep(1.0)
        keyboard.send('q'); time.sleep(1.0)
        keyboard.send('f'); time.sleep(1.0)
                # 3. ещё 5 сек перерыв, затем E-W-F-Space-Space
        print("[+] Перерыв 5 сек...")
        time.sleep(5.0)
        print("[+] Нажимаем E-W-F-Space-Space")
        keyboard.send('e'); time.sleep(1.0)
        keyboard.send('w'); time.sleep(1.0)
        keyboard.send('f'); time.sleep(0.8)
        keyboard.send('space'); time.sleep(0.05)
        keyboard.send('space'); time.sleep(1.0)

        print("[+] Цикл завершён, повторяем...")
        time.sleep(1)          # просто ждём, пока ты не скажешь, что делать

except KeyboardInterrupt:
    print("\n[!] Остановлено пользователем.")
