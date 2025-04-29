from . import terminal as dt


# ----------------------------------------------------------------------------------------------------------------------
# Classes
class Widget:
    def keyboard(self, key: int, press: bool, keycode: int): ...
    def mouse_move(self, x: int, y: int): ...
    def mouse_button(self, x: int, y: int, button: int, press: bool): ...
    def mouse_scroll(self, x: int, y: int, direction: int): ...
    def update(self): ...

    def draw(self):
        print(self, end='')

    def set_position(self, x: int, y: int):
        self.x, self.y = x, y

    def set_size(self, width: int, height: int):
        self.width, self.height = width, height


class ColorHint:
    def __init__(self, col: str = '', col_hover: str = '', col_active: str = ''):
        self.col = col
        self.col_hover = col_hover
        self.col_active = col_active
        self.hover: bool = False
        self.active: bool = False
    
    def __call__(self) -> str:
        return self.col_active if self.active else self.col_hover if self.hover else self.col


# ----------------------------------------------------------------------------------------------------------------------
# Buttons
class InlineTextButton(Widget):
    def __init__(self, x: int, y: int, text: str):
        self.set_position(x, y)
        self.set_size(len(text), 1)
        self.call = lambda: None
        self.text = text
        self.bgd = ColorHint(
            col=dt.bgd(80, 80, 80),
            col_hover=dt.bgd(0x80, 0xcd, 0xff),
            col_active=dt.bgd(0xff, 0xff, 0xff)
        )
        self.fgd = ColorHint(
            col=dt.fgd(0xff, 0xff, 0xff),
            col_hover=dt.fgd(0xff, 0xff, 0xff),
            col_active=dt.fgd(0x10, 0x10, 0x10)
        )
        self._pressed = False

    def __call__(self):
        self.call()

    def __str__(self):
        return f"{dt.move(self.x, self.y)}{self.bgd()}{self.fgd()}{self.text}"
    
    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + self.width and self.y == y
    
    def mouse_move(self, x: int, y: int):
        bounds = self._check_bounds(x, y)
        self.bgd.hover = bounds
        self.fgd.hover = bounds

    def mouse_button(self, x: int, y: int, button: int, press: bool):
        pressed = self._check_bounds(x, y) and press
        if not pressed and self._pressed:
            self()
        self._pressed = pressed

        self.bgd.active = pressed
        self.fgd.active = pressed

    def update(self):
        ...


# ----------------------------------------------------------------------------------------------------------------------
# Header Bar
class HeaderBar(Widget):
    def add_item(self, item: InlineTextButton):
        item.set_position(self._len_items +1, 0)
        item.bgd.col = self.bgd
        item.fgd.col = self.fgd
        self._items.append(item)
        self._len_items = sum([len(i.text) +1 for i in self._items])

    
    def __init__(self, width: int):
        self.set_position(0, 0)
        self.set_size(width, 1)
        self.bgd = dt.bgd(255, 255, 255)
        self.fgd = dt.fgd(10, 10, 10)

        self._items: list[InlineTextButton] = []
        self._len_items: int = 0


    def __str__(self):
        s = dt.move(0, 0) + self.bgd + self.fgd + " " * self.width
        for item in self._items:
            s += str(item)
        return s
    

    def mouse_move(self, x: int, y: int):
        for item in self._items:
            item.mouse_move(x, y)


    def mouse_button(self, x: int, y: int, button: int, press: bool):
        for item in self._items:
            item.mouse_button(x, y, button, press)

