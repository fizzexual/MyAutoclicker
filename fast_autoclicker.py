import ctypes
import time

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
    inp = INPUT()
    inp.type = 0
    inp.mi = MOUSEINPUT(0, 0, 0, 2, 0, ctypes.pointer(extra))
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))
    inp.mi.dwFlags = 4
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

print("Autoclicker started (MAX SPEED)")

while True:
    click()