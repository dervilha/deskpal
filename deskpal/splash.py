import json
from datetime import datetime

from . import (
    terminal as dt,
    widgets as dw
)
from .res_loader import load_resource

CONFIG: dict = json.loads(load_resource("config.json"))

# Splash screen title
splash_screen_title = "<TITLE>"
_hour = datetime.now().hour
if _hour > 12:
    splash_screen_title = "Good evening!" if _hour > 17 else "Good afternoon!"
else:
    splash_screen_title = "Good morning!" if _hour > 4 else "Up late, eh?"


class SplashScreenInterface(dt.Interface):
    def __init__(self):
        width = dt.size()[0]
        self.widgets: dict[str, dw.Widget] = {
            'header-bar': dw.HeaderBar(width)
        }


        self.widgets['header-bar'].add_item(button_start := dw.InlineTextButton(0, 0, "Start"))
        self.widgets['header-bar'].add_item(button_help := dw.InlineTextButton(0, 0, "Help"))
        button_start.call = lambda: print(dt.move(0, 5) + "S")
        button_help.call = lambda: print(dt.move(0, 5) + "H")


    def resize(self, width: int, height: int):
        self.widgets['header-bar'].set_size(width, 1)
        
        dt.clear_screen()
        print(dt.move(2, 2) + splash_screen_title)

        for w in self.widgets.values():
            w.draw()


    def keyboard(self, key, press, keycode):
        if key == ord('q') and press:
            dt.stop()

        for w in self.widgets.values():
            w.keyboard(key, press, keycode)

        
    def mouse_move(self, x: int, y: int):
        for w in self.widgets.values():
            w.mouse_move(x, y)


    def mouse_button(self, x: int, y: int, button: int, press: bool):
        for w in self.widgets.values():
            w.mouse_button(x, y, button, press)


    def mouse_scroll(self, x: int, y: int, direction: int):
        for w in self.widgets.values():
            w.mouse_scroll(x, y, direction)


    def update(self):
        for w in self.widgets.values():
            w.update()
            w.draw()
