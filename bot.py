import pyautogui
import time
import keyboard
import sys, os
import pytesseract
from PIL import Image

# ----------------- настройки -----------------
CONF        = 0.7
LOOP_DELAY  = 0.5

BASE = getattr(sys, '_MEIPASS', os.path.abspath('.'))
def img(path):
    return os.path.join(BASE, path)

# ----------------- OCR: читаем метр -----------------
def read_meter():
    """Сравниваем 10 шаблонов цифр и возвращаем текущее значение метра (0-9)."""
    while True:
        for digit in range(10):
            try:
                if pyautogui.locateOnScreen(img(f'images/meter{digit}.png'), confidence=CONF):
                    print(f"[+] Метр = {digit}")
                    return digit
            except pyautogui.ImageNotFoundException:
                pass
        time.sleep(LOOP_DELAY)

# ----------------- старые функции (без изменений) -----------------
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

# ----------------- основной цикл -----------------
print("Бот запущен. Нажми Ctrl+C для остановки.")
try:
    while True:
        # 1. начало боя (без изменений)
        wait_and_hold_key('images/1.png', 'e', 2)
        wait_and_click('images/2.png')
        wait_and_hold_lmb('images/5.png', 2)

        # 2. OCR-ветвление по метру
        meter = read_meter()
        if meter >= 7:
            print("[+] Метр ≥ 7 → жмём E дважды")
            pyautogui.press('e')
            time.sleep(0.1)
            pyautogui.press('e')
            pyautogui.press('space')
            time.sleep(0.1)
            pyautogui.press('space')
        else:
            print("[+] Метр < 7 → дважды F")
            pyautogui.press('f')
            time.sleep(0.1)
            pyautogui.press('f')

        print("[+] Цикл завершён, повторяем...")
except KeyboardInterrupt:
    print("\n[!] Остановлено пользователем.")
