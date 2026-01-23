# Location: /autoclicker/fast_autoclicker.py
# File: fast_autoclicker.py

import ctypes
import threading
import time
import tkinter as tk
from tkinter import ttk
import keyboard
import json
import os

SendInput = ctypes.windll.user32.SendInput
SETTINGS_FILE = "settings.json"

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("mi", MOUSEINPUT)]

def click():
    extra = ctypes.c_ulong(0)
    i = INPUT()
    i.type = 0
    i.mi = MOUSEINPUT(0, 0, 0, 2, 0, ctypes.pointer(extra))
    SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))
    i.mi.dwFlags = 4
    SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))

running = False
click_interval = 0.1
burst = 1
target_mode = "Human"
hotkey = "F6"

modes = {
    "Human": 5,
    "Normal": 20,
    "Above Normal": 50,
    "Fast": 200,
    "Ultra Fast": 500,
    "SONIC": 1000
}

def clicker_loop():
    global running, click_interval, burst
    next_click = time.perf_counter()
    while True:
        if running:
            now = time.perf_counter()
            if now >= next_click:
                for _ in range(burst):
                    click()
                next_click = now + click_interval
            time.sleep(0.0005)
        else:
            time.sleep(0.01)

threading.Thread(target=clicker_loop, daemon=True).start()

root = tk.Tk()
root.title("Ultra Fast Autoclicker")
root.geometry("380x450")
root.resizable(False, False)
root.attributes("-topmost", True)

status_var = tk.StringVar(value="OFF")
mode_var = tk.StringVar(value="Human")
warning_var = tk.StringVar(value="")
hotkey_var = tk.StringVar(value=f"Current Hotkey: {hotkey}")

def start():
    global running
    running = True
    status_var.set("ON")

def stop():
    global running
    running = False
    status_var.set("OFF")

def toggle_running():
    if running:
        stop()
    else:
        start()

def set_mode(mode):
    global click_interval, burst, target_mode
    target_mode = mode
    cps = modes[mode]
    if mode == "SONIC":
        burst = 20
        click_interval = 1 / cps
        warning_var.set("⚠️ MAY CAUSE DAMAGE OR FREEZE COMPUTER ⚠️")
        warning_frame.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
    else:
        burst = 1
        click_interval = 1 / cps
        warning_var.set("")
        warning_frame.config(highlightthickness=0)
    mode_var.set(mode)

def set_hotkey():
    warning_var.set("Press a key or mouse button...")
    warning_label.config(fg="orange")
    root.update()

    event = keyboard.read_event(suppress=True)
    key_name = event.name
    if event.event_type in ["down", "down_mouse"] or event.event_type == keyboard.MOUSE_BUTTON:
        global hotkey
        hotkey = key_name
        hotkey_var.set(f"Current Hotkey: {hotkey}")
        save_settings()
        warning_var.set("")
        warning_label.config(fg="red")
        keyboard.add_hotkey(hotkey, toggle_running)

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"hotkey": hotkey}, f)

def load_settings():
    global hotkey
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            hotkey = data.get("hotkey", "F6")
            hotkey_var.set(f"Current Hotkey: {hotkey}")
            keyboard.add_hotkey(hotkey, toggle_running)

load_settings()

# ===== GUI =====

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

ttk.Label(main_frame, text="🖱️ Ultra Fast Autoclicker", font=("Arial", 16)).pack(pady=5)
ttk.Label(main_frame, text="Status:", font=("Arial", 12)).pack()
ttk.Label(main_frame, textvariable=status_var, font=("Arial", 14)).pack(pady=5)

btn_frame = tk.Frame(main_frame)
btn_frame.pack(pady=5)
ttk.Button(btn_frame, text="START", command=start).pack(side="left", padx=10)
ttk.Button(btn_frame, text="STOP", command=stop).pack(side="left", padx=10)

ttk.Label(main_frame, text="Mode:", font=("Arial", 12)).pack(pady=5)
for mode in modes:
    ttk.Radiobutton(main_frame, text=mode, value=mode, variable=mode_var,
                    command=lambda m=mode: set_mode(m)).pack(anchor="w", padx=20)

# Warning frame
warning_frame = tk.Frame(main_frame, bg="white", height=60)
warning_frame.pack(pady=10, fill="x", padx=10)
warning_frame.pack_propagate(False)
warning_label = tk.Label(warning_frame, textvariable=warning_var, wraplength=340,
                         justify="center", font=("Arial", 12, "bold"), fg="red", bg="white")
warning_label.pack(expand=True)

# Hotkey frame
hotkey_frame = tk.Frame(main_frame)
hotkey_frame.pack(pady=10)
ttk.Button(hotkey_frame, text="SET HOTKEY", command=set_hotkey).pack(side="left", padx=10, ipadx=10, ipady=5)
ttk.Label(hotkey_frame, textvariable=hotkey_var, font=("Arial", 12)).pack(side="left", padx=10)

root.mainloop()
