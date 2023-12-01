import pygame
pygame.init()

screen = pygame.display.get_surface()

def setup(screen ,screen_):
    screen = screen_

font = pygame.font.Font('fonts/CaskaydiaCoveNerdFont-Regular.ttf', 20)

debug_list = []

def debug(text):
    text_surf = font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect()
    # screen.blit(text_surf, text_rect)
    debug_list.append([text_surf, text_rect])

def print_debug():
    for i, m in enumerate(debug_list):
        m[1].x = 0
        m[1].y = i * 30
        screen.blit(m[0], m[1])
    debug_list.clear()
