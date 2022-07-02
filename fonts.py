import pygame

pygame.font.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fontfinal = pygame.font.Font('Reboot.ttf', 15)
fontfinal_grande = pygame.font.Font('Reboot.ttf', 60)


# texto na tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))