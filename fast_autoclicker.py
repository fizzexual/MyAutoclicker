import ctypes
import threading
import time
import tkinter as tk
from tkinter import ttk
import keyboard

SendInput = ctypes.windll.user32.SendInput

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
root.geometry("360x380")
root.resizable(False, False)
root.attributes("-topmost", True)

status_var = tk.StringVar(value="OFF")
mode_var = tk.StringVar(value="Human")
warning_var = tk.StringVar(value="")

modes = {
    "Human": 5,
    "Normal": 20,
    "Above Normal": 50,
    "Fast": 200,
    "Ultra Fast": 500,
    "SONIC": 1000
}

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
        warning_var.set("⚠️ MAY FREEZE COMPUTER ⚠️")
        warning_frame.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
    else:
        burst = 1
        click_interval = 1 / cps
        warning_var.set("")
        warning_frame.config(highlightthickness=0)
    mode_var.set(mode)

ttk.Label(root, text="🖱️ Fast Autoclicker", font=("Arial", 16)).pack(pady=10)
ttk.Label(root, text="Status:").pack()
ttk.Label(root, textvariable=status_var, font=("Arial", 14)).pack()

ttk.Button(root, text="START", command=start).pack(pady=5)
ttk.Button(root, text="STOP", command=stop).pack(pady=5)

ttk.Label(root, text="Mode:").pack(pady=5)
for mode in modes:
    ttk.Radiobutton(root, text=mode, value=mode, variable=mode_var,
                    command=lambda m=mode: set_mode(m)).pack(anchor="w", padx=20)

warning_frame = tk.Frame(root, bg="white", height=50)
warning_frame.pack(pady=15, fill="x", padx=10)
warning_frame.pack_propagate(False)

warning_label = tk.Label(warning_frame, textvariable=warning_var, wraplength=340,
                         justify="center", font=("Arial", 12, "bold"), fg="red", bg="white")
warning_label.pack(expand=True)


keyboard.add_hotkey('F6', toggle_running)

root.mainloop()
