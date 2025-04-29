import os
from . import terminal as tl

class DirectoryInterface(tl.Interface):
    def keyboard(self, key, press, keycode):
        if key == ord('q') and press:
            tl.stop()

    def update(self):
        print(tl.move(0, 0) + f"{os.path.abspath('.')}", end='')

def entry_main(args: list[str] = []):
    tl.set_title("Deskpal")
    tl.run(DirectoryInterface())
