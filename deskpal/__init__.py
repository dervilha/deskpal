import terminal as tl

class MyInterface(tl.Interface):
    def keyboard(self, key, press, keycode):
        if key == ord('q') and press:
            tl.stop()


if __name__ == "__main__":
    interface = MyInterface()
    tl.run(interface)