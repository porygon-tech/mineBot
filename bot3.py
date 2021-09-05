#mineBot functions
#author: miguel roman @porygon-tech
import ctypes
from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware() 

from time import sleep
from numpy.random import normal as rnorm

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)

#https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
'''
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
'''
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), # If dwFlags does not contain MOUSEEVENTF_WHEEL, MOUSEEVENTF_XDOWN, or MOUSEEVENTF_XUP, then mouseData should be zero.
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#------------------
# functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def mouse_move(pos):
    (dx,dy) = pos
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx, dy, 0, 0x0001, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(0), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#documentation for coding functions:
#https://gist.github.com/tracend/912308
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
#https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

keycode = {
    1 : 0x11, # w    'forward'  
    2 : 0x1E, # a    'left'     
    3 : 0x1F, # s    'right'    
    4 : 0x20  # d    'backwards'
}



def walk(key1, key2=None, duration=1):
    if key2:
        PressKey(keycode[key1])
        PressKey(keycode[key2])
        sleep(duration)
        ReleaseKey(keycode[key1])
        ReleaseKey(keycode[key2])
    else:
        PressKey(keycode[key1])
        sleep(duration)
        ReleaseKey(keycode[key1])



def look(x, y):
    mouse_move((1,0))
    mouse_move((-1,0))
    k_x = 1 #yet to be adjusted
    k_y = 1 #yet to be adjusted
    mouse_move((int(k_x*x),int(k_y*y)))

    

#=======================================================
#          TEST ZONE


'''
print("Get ready...")
sleep(1)

PressKey(0x11)
sleep(.5)
ReleaseKey(0x11)

std=50

import numpy as np
for n in range(5):
    sleep(.5)
    print("movement no. {0}".format(n))
    dx = int(rnorm(0, std))
    dy = int(rnorm(0, std))
    mouse_move((dx,dy))

mouse_move((1,0))
mouse_move((-1,0))
sleep(.5)
mouse_move((272,0)) #100px = 33º

for n in range(5):
    mouse_move((100,0)) #100px = 33º
    sleep(.5)
'''




print("Get ready...")
sleep(1)
walk(1, duration=2)
sleep(.3)
walk(3)
#look(-90,0)
#look(-90,0)
sleep(1)


#smooth view movement experiment
for n in range(50):
    look(-2,1)
    sleep(.001)
