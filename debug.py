from os import device_encoding
import pygame
pygame.init()
screen = pygame.display.get_surface()
font = pygame.font.Font('fonts/CaskaydiaCoveNerdFont-Regular.ttf', 20)

debug_list = []

def debug(text):
    text_surf = font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect()
    dect = {'text': text_surf, 'rect': text_rect}
    debug_list.append(dect)

def print_debug():
    for i, message in debug_list:
        print(len(debug_list))
        # message['rect'].y = 30 * i
        print("Message: ", end='')
        print(message[0], message[1])
        # screen.blit(message['text'], message['rect'])
