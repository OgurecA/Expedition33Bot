import pyautogui
import time
import keyboard
import sys, os
import pytesseract
import cv2
import numpy as np
from PIL import Image

# ----------------- настройки -----------------
CONF        = 0.6
LOOP_DELAY  = 0.5

BASE = getattr(sys, '_MEIPASS', os.path.abspath('.'))
def img(path):
    return os.path.join(BASE, path)

# ----------------- OCR: читаем метр -----------------
def read_meter():
    """Перебираем 10 шаблонов 0a.png ... 9a.png и берём ЛУЧШЕЕ совпадение (даже 0.1)."""
    while True:
        best_digit = None
        best_conf  = -1.0
        screen     = np.array(pyautogui.screenshot())

        for d in range(10):
            try:
                template = cv2.imread(img(f'images/{d}a.png'), cv2.IMREAD_COLOR)
                if template is None:
                    continue
                res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > best_conf:
                    best_conf  = max_val
                    best_digit = d
            except Exception as e:
                print(f"[!] Ошибка при поиске {d}a: {e}")
                continue

        # ВСЕГДА возвращаем лучшую цифру (даже если conf 0.01)
        if best_digit is not None:
            print(f"[+] Метр = {best_digit} (лучшее совпадение {best_conf:.3f})")
            return best_digit

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

        # 2. цикл: метр + действия, пока не появится 12
        while True:
            try:                       # ← общий страховочный блок
                time.sleep(2.0)
                meter = read_meter()
                if meter >= 7:
                    # вставляем ПЕРЕД первым keyboard.send внутри цикла метра
                    try:
                        game_window = pyautogui.getWindowsWithTitle('Expedition 33')[0]   # заголовок окна
                        game_window.activate()
                    except Exception as e:
                    print(f"[!] Не удалось активировать окно игры: {e}")
                    keyboard.send('e')
                    time.sleep(1.0)
                    keyboard.send('w')
                    time.sleep(1.0)
                    keyboard.send('f')
                    time.sleep(3.0)
                    keyboard.send('space')
                    time.sleep(0.1)
                    keyboard.send('space')
                    time.sleep(4.0)
                else:
                    keyboard.send('f'); time.sleep(0.5)
                    keyboard.send('f')
                    time.sleep(4.0)

                if (pyautogui.locateOnScreen(img('images/12.png'), confidence=CONF) or
                    pyautogui.locateOnScreen(img('images/13.png'), confidence=CONF)):
                    print("[+] Бой закончен → выход из цикла метра")
                    break
            except Exception as e:
                print(f"[!] Ошибка в цикле метра: {type(e).__name__}: {e.args}")
                # дебаг-скрин
                try:
                    debug_shot = pyautogui.screenshot()
                    debug_shot.save(r'D:\a\Expedition33Bot\Expedition33Bot\debug_screen.png')
                    print("[debug] Скрин сохранён как debug_screen.png")
                except:
                    pass
                time.sleep(LOOP_DELAY)

        print("[+] Цикл завершён, повторяем...")
except KeyboardInterrupt:
    print("\n[!] Остановлено пользователем.")
