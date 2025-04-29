import os
from . import terminal as tl
from . import widgets as wg

class DirectoryInterface(tl.Interface):
    def __init__(self):
        self.widgets: dict[str, wg.Widget] = {
            'button': wg.InlineTextButton(x=1, y=1, text=" Hello! ")
        }
        self.widgets['button'].call = lambda: print(tl.move(0, 5) + f"hi!", end='')


    def resize(self, width: int, height: int):
        tl.clear_screen()
        for w in self.widgets.values():
            w.draw()

    def keyboard(self, key, press, keycode):
        if key == ord('q') and press:
            tl.stop()

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
        print(tl.move(0, 0) + f"{os.path.abspath('.')}", end='')
        for w in self.widgets.values():
            w.update()
            w.draw()
