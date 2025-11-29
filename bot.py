import pyautogui
import time
import keyboard

# Настройки
CONF = 0.8
LOOP_DELAY = 0.5

def wait_and_hold_key(image, key, hold_time):
    """Ждём появления картинки, затем удерживаем клавишу."""
    while True:
        pos = pyautogui.locateOnScreen(image, confidence=CONF)
        if pos:
            print(f"[+] Найдено: {image} → удерживаю {key} {hold_time}с")
            pyautogui.keyDown(key)
            time.sleep(hold_time)
            pyautogui.keyUp(key)
            return
        time.sleep(LOOP_DELAY)

def wait_and_click(image):
    """Ждём появления картинки и кликаем один раз."""
    while True:
        pos = pyautogui.locateOnScreen(image, confidence=CONF)
        if pos:
            print(f"[+] Найдено: {image} → клик")
            pyautogui.click(pos)
            return
        time.sleep(LOOP_DELAY)

def wait_and_hold_lmb(image, hold_time):
    """Ждём появления картинки и удерживаем ЛКМ."""
    while True:
        pos = pyautogui.locateOnScreen(image, confidence=CONF)
        if pos:
            print(f"[+] Найдено: {image} → удерживаю ЛКМ {hold_time}с")
            pyautogui.mouseDown(button='left')
            time.sleep(hold_time)
            pyautogui.mouseUp(button='left')
            return
        time.sleep(LOOP_DELAY)

# === Основной цикл ===
print("Бот запущен. Нажми Ctrl+C для остановки.")
try:
    while True:
        wait_and_hold_key('images/1.png', 'e', 2)
        wait_and_click('images/2.png')
        wait_and_hold_lmb('images/5.png', 2)
        print("[+] Цикл завершён, повторяем...")
except KeyboardInterrupt:
    print("\n[!] Остановлено пользователем.")