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
delay = 0.0

def clicker_loop():
    global running
    while True:
        if running:
            click()
            if delay > 0:
                time.sleep(delay)
        else:
            time.sleep(0.01)

threading.Thread(target=clicker_loop, daemon=True).start()

root = tk.Tk()
root.title("Ultra Fast Autoclicker")
root.geometry("320x260")
root.resizable(False, False)

status_var = tk.StringVar(value="OFF")
cps_var = tk.StringVar(value="∞ (MAX)")

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

def set_cps(val):
    global delay
    cps = int(float(val))
    if cps == 0:
        delay = 0
        cps_var.set("∞ (MAX)")
    else:
        delay = 1 / cps
        cps_var.set(str(cps))

ttk.Label(root, text="🖱️ Fast Autoclicker", font=("Arial", 16)).pack(pady=10)
ttk.Label(root, text="Status:").pack()
ttk.Label(root, textvariable=status_var, font=("Arial", 14)).pack()

ttk.Button(root, text="START", command=start).pack(pady=5)
ttk.Button(root, text="STOP", command=stop).pack(pady=5)

ttk.Label(root, text="CPS (0 = MAX):").pack(pady=5)
slider = ttk.Scale(root, from_=0, to=1000, orient="horizontal", command=set_cps)
slider.set(0)
slider.pack(fill="x", padx=20)

ttk.Label(root, text="Current CPS:").pack()
ttk.Label(root, textvariable=cps_var).pack()

keyboard.add_hotkey('F6', toggle_running)

root.mainloop()
