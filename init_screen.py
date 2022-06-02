import pygame
import images
import audio
import level_screen
import ranking_page
from time import sleep

BLACK = (0, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

b1_left, b1_top, b1_width, b1_height = 60, 300, 100, 50
b2_left, b2_top, b2_width, b2_height = 190, 300, 100, 50
b3_left, b3_top, b3_width, b3_height = 315, 300, 100, 50
b4_left, b4_top, b4_width, b4_height = 445, 300, 100, 50

clock = pygame.time.Clock()


# cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def Init_screen():

    # cria a janela
    global menu_button1, menu_button2, menu_button3, menu_button4
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    intro = True
    pygame.mixer.init()
    audio.introMusic.play(-1)
    pygame.mixer.music.set_volume(0.2)

    while intro:

        screen.blit(images.bg_menu_image, (0, 0))
        pygame.draw.rect(screen, BLACK, [b1_left, b1_top, b1_width, b1_height])
        screen.blit(images.iniciar_on, (b1_left, b1_top))
        pygame.draw.rect(screen, BLACK, [b2_left, b2_top, b2_width, b2_height])
        screen.blit(images.iniciar_off, (b2_left, b2_top))
        pygame.draw.rect(screen, BLACK, [b3_left, b3_top, b3_width, b3_height])
        screen.blit(images.dificuldade_on, (b3_left, b3_top))
        pygame.draw.rect(screen, BLACK, [b4_left, b4_top, b4_width, b4_height])
        screen.blit(images.dificuldade_off, (b4_left, b4_top))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                w = pygame.mouse.get_pos()[0]
                z = pygame.mouse.get_pos()[1]

                # inicia o jogo
                if b1_left < w < (b1_left + b1_width) and b1_top < z < (b1_top + b1_height):
                    audio.introMusic.fadeout(1000)
                    sleep(0.5)
                    audio.button_confirma.play()
                    sleep(1.3)
                    intro = False

                # vai para a pagina de dificuldade
                if b2_left < w < (b2_left + b2_width) and b2_top < z < (b2_top + b2_height):
                    sleep(0.5)
                    audio.button_cursor.play()
                    sleep(1.3)
                    intro = False
                    level_screen.Level_screen()

                # vai para a pagina de ranking
                if b3_left < w < (b3_left + b3_width) and b3_top < z < (b3_top + b3_height):
                    sleep(0.5)
                    audio.button_cursor.play()
                    sleep(1.3)
                    intro = False
                    ranking_page.Ranking_page()

                # fecha o jogo
                if b4_left < w < (b4_left + b4_width) and b4_top < z < (b4_top + b4_height):
                    pygame.quit()
                    quit()

            mouse = pygame.mouse.get_pos()

            if b1_left + b1_width > mouse[0] > b1_left and b1_top + b1_height > mouse[1] > b1_top:
                images.iniciar_on = pygame.image.load('assets/images/iniciar_on.png').convert_alpha()
            else:
                images.iniciar_on = pygame.image.load('assets/images/iniciar_off.png').convert_alpha()

            if b2_left + b2_width > mouse[0] > b2_left and b2_top + b2_height > mouse[1] > b2_top:
                images.iniciar_off = pygame.image.load('assets/images/dificuldade_on.png').convert_alpha()
            else:
                images.iniciar_off = pygame.image.load('assets/images/dificuldade_off.png').convert_alpha()

            if b3_left + b3_width > mouse[0] > b3_left and b3_top + b3_height > mouse[1] > b3_top:
                images.dificuldade_on = pygame.image.load('assets/images/ranking_on.png').convert_alpha()
            else:
                images.dificuldade_on = pygame.image.load('assets/images/ranking_off.png').convert_alpha()

            if b4_left + b4_width > mouse[0] > b4_left and b4_top + b4_height > mouse[1] > b4_top:
                images.dificuldade_off = pygame.image.load('assets/images/sair_on.png').convert_alpha()
            else:
                images.dificuldade_off = pygame.image.load('assets/images/sair_off.png').convert_alpha()

        pygame.display.update()
        clock.tick(60)
