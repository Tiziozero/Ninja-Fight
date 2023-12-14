import game
import debug
debug_log = input("Log debug? [Y/n] ").lower()
if debug_log == 'y':
    debug.log_true = True
else:
    debug.log_debug = False

game_ = game.Game()
game_.run()
