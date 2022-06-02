import pygame
import images
import audio
from time import sleep

pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

black = (0, 0, 0)

b1_left, b1_top, b1_width, b1_height = 150, 200, 105, 50
b2_left, b2_top, b2_width, b2_height = 150, 300, 105, 50
b3_left, b3_top, b3_width, b3_height = 150, 400, 105, 50

clock = pygame.time.Clock()

# cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def Ranking_page():

    # cria a janela
    global menu_button1, menu_button2
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    intro = True

    while intro:

        screen.fill(black)
        pygame.display.update()
        clock.tick(60)