import ctypes
from ctypes import c_char_p, c_void_p, c_ulong, c_int, byref, POINTER
import time

x11 = ctypes.cdll.LoadLibrary('libX11.so.6')

x11.XOpenDisplay.restype = c_void_p
x11.XOpenDisplay.argtypes = [c_char_p]
d = x11.XOpenDisplay(None)
if not d:
    print("Cannot open display")
    exit(1)

x11.XInternAtom.restype = c_ulong
x11.XInternAtom.argtypes = [c_void_p, c_char_p, c_int]

CLIPBOARD = x11.XInternAtom(d, b"CLIPBOARD", False)
PRIMARY = x11.XInternAtom(d, b"PRIMARY", False)
UTF8_STRING = x11.XInternAtom(d, b"UTF8_STRING", False)
STRING = x11.XInternAtom(d, b"STRING", False)

x11.XCreateSimpleWindow.restype = c_ulong
x11.XCreateSimpleWindow.argtypes = [c_void_p, c_ulong, c_int, c_int, c_int, c_int, c_int, c_ulong, c_ulong]
x11.XDefaultRootWindow.restype = c_ulong
x11.XDefaultRootWindow.argtypes = [c_void_p]

root = x11.XDefaultRootWindow(d)
w = x11.XCreateSimpleWindow(d, root, 0, 0, 1, 1, 0, 0, 0)
SELECTION = x11.XInternAtom(d, b"XSEL_DATA", False)

class XEvent(ctypes.Structure):
    _fields_ = [("type", c_int), ("pad", c_ulong * 24)]

def try_read(sel_atom, target_atom):
    x11.XConvertSelection(d, sel_atom, target_atom, SELECTION, w, 0)
    x11.XFlush(d)
    t0 = time.time()
    found = False
    ev = XEvent()
    while time.time() - t0 < 0.5:
        if x11.XPending(d):
            x11.XNextEvent(d, byref(ev))
            if ev.type == 31:
                found = True
                break
        time.sleep(0.01)
    if found:
        actual_type = c_ulong()
        actual_format = c_int()
        nitems = c_ulong()
        bytes_after = c_ulong()
        prop = c_void_p()
        x11.XGetWindowProperty.argtypes = [
            c_void_p, c_ulong, c_ulong, c_ulong, c_ulong, c_int, c_ulong,
            POINTER(c_ulong), POINTER(c_int), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_void_p)
        ]
        x11.XGetWindowProperty(
            d, w, SELECTION, 0, 65536, False, 0,
            byref(actual_type), byref(actual_format), byref(nitems), byref(bytes_after), byref(prop)
        )
        if prop.value and nitems.value > 0:
            data = ctypes.string_at(prop.value, nitems.value)
            return data.decode('utf-8', errors='replace')
    return None

for sel_name, sel in [("CLIPBOARD", CLIPBOARD), ("PRIMARY", PRIMARY)]:
    for tgt_name, tgt in [("UTF8_STRING", UTF8_STRING), ("STRING", STRING)]:
        res = try_read(sel, tgt)
        if res:
            print(f"[{sel_name}/{tgt_name}] {res}")
            exit(0)

print("No selection data found.")
