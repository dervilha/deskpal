import sys
import deskpal as dp

COMMANDS = {
    'cd': None
}

def entry_args():
    config = dp.load_resource("config.json")

    if sys.argv[1].lower() in COMMANDS.keys():      # Command
        print(f"Command {sys.argv[1]}")
    else:                                           # Path
        print(f"Path {sys.argv[1]}")


if __name__ == '__main__':
    dp.terminal.set_title("Deskpal")
    dp.terminal.set_framerate(30)

    if len(sys.argv) > 1:       # entry args
        entry_args()
    else:                       # entry standalone
        from deskpal.splash import SplashScreenInterface
        dp.terminal.run(SplashScreenInterface())

