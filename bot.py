import pyautogui
import time
import keyboard
import sys, os
import cv2
import numpy as np

# ----------------- настройки -----------------
CONF        = 0.7
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

# ----------------- основной цикл (НОВОЕ) -----------------
print("Бот запущен. Нажми Ctrl+C для остановки.")
try:
    while True:
        # 1. начало боя (без изменений)
        wait_and_hold_key('images/1.png', 'e', 2)
        wait_and_click('images/2.png')
        wait_and_hold_lmb('images/5.png', 2)

        # 2. ждём 14.png, затем запускаем серию до 12/13
        print("[+] Жду появления 14.png...")
        while True:
            try:
                if pyautogui.locateOnScreen(img('images/14.png'), confidence=CONF):
                    print("[+] Найдено 14 → запускаем серию E-W-F-Space-Space")
                    break
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(1.0)

        # 3. серия нажатий до появления 12 или 13
        print("[+] Запускаем серию E-W-F-Space-Space до 12/13")
        while True:
            # фоновая проверка 12/13 каждую секунду
            try:
                if (pyautogui.locateOnScreen(img('images/12.png'), confidence=CONF) or
                    pyautogui.locateOnScreen(img('images/13.png'), confidence=CONF)):
                    print("[+] Найдено 12 или 13 → выход из серии")
                    break
            except pyautogui.ImageNotFoundException:
                pass

            # нажатия (проверка происходит ПАРАЛЛЕЛЬНО)
            time.sleep(2.0)
            keyboard.send('e')
            time.sleep(2.0)
            keyboard.send('w')
            time.sleep(2.0)
            keyboard.send('f')
            time.sleep(3.0)
            keyboard.send('space')
            time.sleep(0.1)
            keyboard.send('space')
            time.sleep(2.0)          # пауза перед следующим циклом

        print("[+] Серия завершена, повторяем главный цикл...")
except KeyboardInterrupt:
    print("\n[!] Остановлено пользователем.")
