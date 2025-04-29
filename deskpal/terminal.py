import os

# ----------------------------------------------------------------------------------------------------------------------
# ANSI characters
ANSI_RESET: str = "\033[0m"
ANSI_BOLD: str = "\033[1m"
ANSI_UNDERLINE: str = "\033[4m"
ANSI_INVERSE: str = "\033[7m"


# ----------------------------------------------------------------------------------------------------------------------
# ANSI control characters
def move(x: int, y: int):
    return f"\033[{y +1};{x +1}H"

def bgd(r: int, g: int, b: int):
    return f"\033[48;2;{r};{g};{b}m"

def fgd(r: int, g: int, b: int):
    return f"\033[38;2;{r};{g};{b}m"


# ----------------------------------------------------------------------------------------------------------------------
# ANSI methods
def clear_line():
    print("\033[2K", end='')

def clear_screen():
    print("\033[2J", end='')


# ----------------------------------------------------------------------------------------------------------------------
# General methods
def size() -> tuple[int, int]:
    _ts = os.get_terminal_size()
    return _ts.columns, _ts.lines


# ----------------------------------------------------------------------------------------------------------------------
# Draw calls
def draw_box(x: int, y: int, width: int, height: int, name: str = None, rounded: bool = True, dotted: bool = False):
    corner = '╭╮╰╯' if rounded else '┌┐└┘'
    edge = '╴╵' if dotted else '─│'

    _hline = (edge[0] *(width -2))
    out = move(x, y) + corner[0] + _hline + corner[1]
    for i in range(1, height -1):
        out += move(x, y +i) + edge[1] + move(x + width -1, y +i) + edge[1]
    out += move(x, y + height -1) + corner[2] + _hline  + corner[3]

    if name:
        out += f'{move(x +1, y)} {name[:width -3]} '

    print(out, end='')


# ----------------------------------------------------------------------------------------------------------------------
# OS specific handling
if os.name == 'nt':
    import ctypes
    import ctypes.wintypes as wintypes

    INPUT_KEYBOARD = 1
    INPUT_MOUSE = 2

    INPUT_MOUSE_BUTTON = 0
    INPUT_MOUSE_MOVE = 1
    INPUT_MOUSE_WHEEL = 4
    INPUT_MOUSE_BUTTON_LEFT = 1
    INPUT_MOUSE_BUTTON_RIGHT = 2
    INPUT_MOUSE_BUTTON_MIDDLE = 4
    INPUT_MOUSE_WHEEL_UP = 8388608
    INPUT_MOUSE_WHEEL_DOWN = 4286578688

    # Constants from Windows API
    _STD_INPUT_HANDLE = -10
    _STD_OUTPUT_HANDLE = -11
    _ENABLE_MOUSE_INPUT = 0x0010
    _ENABLE_EXTENDED_FLAGS = 0x0080
    _ENABLE_WINDOW_INPUT = 0x0008

    # Structs from Windows API
    class COORD(ctypes.Structure):
        _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

    class KEY_EVENT_RECORD(ctypes.Structure):
        _fields_ = [
            ("bKeyDown", wintypes.BOOL),
            ("wRepeatCount", wintypes.WORD),
            ("wVirtualKeyCode", wintypes.WORD),
            ("wVirtualScanCode", wintypes.WORD),
            ("uChar", wintypes.WCHAR),
            ("dwControlKeyState", wintypes.DWORD),
        ]

    class MOUSE_EVENT_RECORD(ctypes.Structure):
        _fields_ = [
            ("dwMousePosition", COORD),
            ("dwButtonState", wintypes.DWORD),
            ("dwControlKeyState", wintypes.DWORD),
            ("dwEventFlags", wintypes.DWORD),
        ]

    class EVENT_UNION(ctypes.Union):
        _fields_ = [
            ("KeyEvent", KEY_EVENT_RECORD),
            ("MouseEvent", MOUSE_EVENT_RECORD),
        ]

    class INPUT_RECORD(ctypes.Structure):
        _fields_ = [
            ("EventType", wintypes.WORD),
            ("Event", EVENT_UNION),
        ]

    # kernel32 config
    kernel32 = ctypes.windll.kernel32
    stdin_handle = kernel32.GetStdHandle(_STD_INPUT_HANDLE)
    console_flags_enabled = False

    # Set console mode to enable mouse input and extended flags
    def set_console_flags():
        global kernel32, console_flags_enabled
        console_flags_enabled = True
        kernel32.SetConsoleMode(
            stdin_handle,
            _ENABLE_EXTENDED_FLAGS | _ENABLE_MOUSE_INPUT | _ENABLE_WINDOW_INPUT
        )

    # Input
    _forced_input_stack = []
    def force_input(event: dict[str, int]):
        _forced_input_stack.append(event)

    def read_input() -> dict[str, int]:
        global console_flags_enabled
        global _forced_input_stack
        if _forced_input_stack:
            return _forced_input_stack.pop()
        
        if not console_flags_enabled:
            set_console_flags()

        record = INPUT_RECORD()
        count = wintypes.DWORD()

        kernel32.PeekConsoleInputW(stdin_handle, ctypes.byref(record), 1, ctypes.byref(count))
        if not count.value:
            return None

        kernel32.ReadConsoleInputW(stdin_handle, ctypes.byref(record), 1, ctypes.byref(count))
        if record.EventType == INPUT_KEYBOARD:
            key = record.Event.KeyEvent
            return {
                'type': INPUT_KEYBOARD,
                'key': ord(key.uChar),
                'press': key.bKeyDown,
                'keycode': key.wVirtualKeyCode,
                'scancode': key.wVirtualScanCode
            }

        if record.EventType == INPUT_MOUSE:
            mouse = record.Event.MouseEvent
            return {
                'type': INPUT_MOUSE,
                'event': mouse.dwEventFlags,
                'button': mouse.dwButtonState,
                'x': mouse.dwMousePosition.X,
                'y': mouse.dwMousePosition.Y,
            }

    # Window title
    def set_title(title: str):
        kernel32.SetConsoleTitleW(title)
        # os.system(f"title {title}") # closed alternative

    # Cursor
    def hide_cursor():
        class CONSOLE_CURSOR_INFO(ctypes.Structure):
            _fields_ = [
                ("dwSize", ctypes.c_int),
                ("bVisible", ctypes.c_bool)
            ]
        cursor_info = CONSOLE_CURSOR_INFO()
            
        stdout_handle = ctypes.windll.kernel32.GetStdHandle(_STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.GetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))
        cursor_info.bVisible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))

    def show_cursor():
        class CONSOLE_CURSOR_INFO(ctypes.Structure):
            _fields_ = [
                ("dwSize", ctypes.c_int),
                ("bVisible", ctypes.c_bool)
            ]
        cursor_info = CONSOLE_CURSOR_INFO()
            
        stdout_handle = ctypes.windll.kernel32.GetStdHandle(_STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.GetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))
        cursor_info.bVisible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))
else:
    raise NotImplementedError("UNIX systems are not yet implemented. Please yell at me at https://github.com/dervilha/deskpal")


# ----------------------------------------------------------------------------------------------------------------------
# Framerate
_TIME_ELAPSED_SAMPLE_COUNT: int = 8
_BASE_FRAMETIME: float = 0.025
_ftime = _BASE_FRAMETIME
_time_elapsed_ptr: int = 0
_time_elapsed_samples: list[float] = [_BASE_FRAMETIME for _ in range(_TIME_ELAPSED_SAMPLE_COUNT)]
def set_framerate(fps: int):
    global _ftime
    _ftime = max(0.001, min(1.0, 1.0 / fps))


# ----------------------------------------------------------------------------------------------------------------------
# Interface class
class Interface:
    def update(self): ...
    def resize(self, width: int, height: int): ...
    def keyboard(self, key: int, press: bool, keycode: int): ...
    def mouse_move(self, x: int, y: int): ...
    def mouse_button(self, x: int, y: int, button: int, press: bool): ...
    def mouse_scroll(self, x: int, y: int, direction: int): ...


# ----------------------------------------------------------------------------------------------------------------------
# Interface system
width, height = 1, 1
running = False
def stop():
    global running
    running = False

def run(interface: Interface):
    assert issubclass(interface.__class__, Interface), "interface must be a subclass of terminal.Interface"
    global _ftime, _time_elapsed_ptr, _time_elapsed_samples
    global width, height
    global running
    running = True
    import time
    from datetime import datetime

    set_console_flags()
    hide_cursor()
    clear_screen()

    while running:
        t0 = datetime.now()
        print(move(0, 0) + ANSI_RESET) # no end='' to flush the buffer

        _w, _h = size()
        if width != _w or height != _h:
            width, height = _w, _h
            clear_screen()
            interface.resize(width, height)

        while ie := read_input():
            if ie['type'] == INPUT_KEYBOARD:
                interface.keyboard(ie['key'], ie['press'], ie['keycode'])
            elif ie['type'] == INPUT_MOUSE:
                if ie['event'] == INPUT_MOUSE_MOVE:
                    interface.mouse_move(ie['x'], ie['y'])
                elif ie['event'] == INPUT_MOUSE_BUTTON:
                    interface.mouse_button(ie['x'], ie['y'], ie['button'], ie['button'] != 0)
                elif ie['event'] == INPUT_MOUSE_WHEEL:
                    interface.mouse_scroll(ie['x'], ie['y'], 1 if ie['button'] == INPUT_MOUSE_WHEEL_DOWN else -1)

        interface.update()

        _time_elapsed_samples[_time_elapsed_ptr] = float((datetime.now() - t0).microseconds) / 1_000_000
        time.sleep(max(0, _ftime - (sum(_time_elapsed_samples) / _TIME_ELAPSED_SAMPLE_COUNT)))
        _time_elapsed_ptr = (_time_elapsed_ptr +1) % _TIME_ELAPSED_SAMPLE_COUNT
    
    print(f"{move(0, 0)}{ANSI_RESET}", end='')
    show_cursor()
    clear_screen()
