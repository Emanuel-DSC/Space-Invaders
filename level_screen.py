import pygame
import images
import audio
from time import sleep
import init_screen

pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

black = (0, 0, 0)

b1_left, b1_top, b1_width, b1_height = 60, 300, 100, 50
b2_left, b2_top, b2_width, b2_height = 190, 300, 100, 50
b3_left, b3_top, b3_width, b3_height = 315, 300, 100, 50
b4_left, b4_top, b4_width, b4_height = 445, 300, 100, 50

clock = pygame.time.Clock()

# cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def Level_screen():

    # cria a janela
    global menu_button1, menu_button2, menu_button3, menu_button4
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dificuldade = True

    while dificuldade:

        screen.blit(images.bg_dificuldade_image, (0, 0))
        pygame.draw.rect(screen, black, [b1_left, b1_top, b1_width, b1_height])
        screen.blit(images.facil_on, (b1_left, b1_top))
        pygame.draw.rect(screen, black, [b2_left, b2_top, b2_width, b2_height])
        screen.blit(images.medio_on, (b2_left, b2_top))
        pygame.draw.rect(screen, black, [b3_left, b3_top, b3_width, b3_height])
        screen.blit(images.dificil_on, (b3_left, b3_top))
        pygame.draw.rect(screen, black, [b4_left, b4_top, b4_width, b4_height])
        screen.blit(images.voltar_on, (b4_left, b4_top))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    audio.introMusic.fadeout(1100)
                    sleep(0.5)
                    audio.button_cursor.play()
                    sleep(1.3)
                    init_screen.Init_screen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                w = pygame.mouse.get_pos()[0]
                z = pygame.mouse.get_pos()[1]

                # facil
                if b1_left < w < (b1_left + b1_width) and b1_top < z < (b1_top + b1_height):
                    audio.introMusic.fadeout(1000)
                    sleep(0.5)
                    audio.button_confirma.play()
                    sleep(1.3)
                    dificuldade = False


                # medio
                if b2_left < w < (b2_left + b2_width) and b2_top < z < (b2_top + b2_height):
                    audio.introMusic.fadeout(1000)
                    sleep(0.5)
                    audio.button_confirma.play()
                    sleep(1.3)
                    dificuldade = False

                # dificil
                if b3_left < w < (b3_left + b3_width) and b3_top < z < (b3_top + b3_height):
                    audio.introMusic.fadeout(1000)
                    sleep(0.5)
                    audio.button_confirma.play()
                    sleep(1.3)
                    dificuldade = False

                # volta pro menu
                if b4_left < w < (b4_left + b4_width) and b4_top < z < (b4_top + b4_height):
                    audio.introMusic.fadeout(1100)
                    sleep(0.5)
                    audio.button_cursor.play()
                    sleep(1.3)
                    init_screen.Init_screen()

            mouse = pygame.mouse.get_pos()

            if b1_left + b1_width > mouse[0] > b1_left and b1_top + b1_height > mouse[1] > b1_top:
                images.facil_on = pygame.image.load('assets/images/facil_on.png').convert_alpha()
            else:
                images.facil_on = pygame.image.load('assets/images/facil_off.png').convert_alpha()

            if b2_left + b2_width > mouse[0] > b2_left and b2_top + b2_height > mouse[1] > b2_top:
                images.medio_on = pygame.image.load('assets/images/medio_on.png').convert_alpha()
            else:
                images.medio_on = pygame.image.load('assets/images/medio_off.png').convert_alpha()

            if b3_left + b3_width > mouse[0] > b3_left and b3_top + b3_height > mouse[1] > b3_top:
                images.dificil_on = pygame.image.load('assets/images/dificil_on.png').convert_alpha()
            else:
                images.dificil_on = pygame.image.load('assets/images/dificil_off.png').convert_alpha()

            if b4_left + b4_width > mouse[0] > b4_left and b4_top + b4_height > mouse[1] > b4_top:
                images.voltar_on = pygame.image.load('assets/images/voltar_on.png').convert_alpha()
            else:
                images.voltar_on = pygame.image.load('assets/images/voltar_off.png').convert_alpha()

        pygame.display.update()
        clock.tick(60)