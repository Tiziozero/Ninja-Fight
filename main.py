import game
import debug
debug_log = input("Log messeges? [Y/n] ").lower()
if debug_log == 'y':
    debug.log_true = True
else:
    debug.log_debug = False
debug_log = input("Display debug? [Y/n] ").lower()
if debug_log == 'y':
    debug.debug_true = True
else:
    debug.debug_debug = False

try:
    if debug.log_true:
        print("[0] all")
        print("[1] game loading messeges")
        print("[2] deper game info")
        print("[3] entity interaction and info")
        print("[4] idk yet")
        print("[5] important only")
        debug.log_level = int(input("Log level:[0-5] "))
except:
    print("Invalid log level. Log level set to 0.")
    debug.log_level = 0

game_ = game.Game()
game_.run()
