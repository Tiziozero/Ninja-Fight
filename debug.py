import pygame
pygame.init()

# screen = pygame.display.get_surface()
log_true = False
debug_true = False

log_level = 0

def setup(screen_, log_bool):
    screen = screen_
    screen = screen_
    print("Log:", log_true)
    print("Debug info:", debug_true)
    # log_true = log_bool

font = pygame.font.Font('fonts/CaskaydiaCoveNerdFont-Regular.ttf', 20)

debug_list = []

def log(text, end=None, level=0):
    if log_true:
        if level >= log_level:
            for i in range(level): print("\t", end='')
            text = str(text)
            print("Log:", text, end=end)

def debug(text):
    text_surf = font.render(str(text), True, (255,255,255))
    text_rect = text_surf.get_rect()
    # screen.blit(text_surf, text_rect)
    debug_list.append([text_surf, text_rect])

def print_debug():
    if debug_true:
        for i, m in enumerate(debug_list):
            m[1].x = 0
            m[1].y = i * 30
            screen.blit(m[0], m[1])
    debug_list.clear()
