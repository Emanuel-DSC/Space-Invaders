import pygame
import fonts
import images
import audio
from time import sleep
import init_screen
import os

pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

b4_left, b4_top, b4_width, b4_height = 480, 630, 100, 50

clock = pygame.time.Clock()

# cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))


def Ranking_page():

    # cria a janela
    global menu_button4
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    list = []
    intro = True

    f = open("high_score.txt", "r")

    last_lines = get_last_n_lines("high_score.txt", 6)
    for lines in last_lines:
        list.append(lines)

    while intro:

        screen.blit(images.ranking_bg, (0, 0))
        pygame.draw.rect(screen, black, [b4_left, b4_top, b4_width, b4_height])
        screen.blit(images.voltar_on, (b4_left, b4_top))

        fonts.draw_text(list[4], fonts.fontfinal_media, green, SCREEN_WIDTH - 550, 200)
        fonts.draw_text(list[3], fonts.fontfinal_media, white, SCREEN_WIDTH - 550, 300)
        fonts.draw_text(list[2], fonts.fontfinal_media, white, SCREEN_WIDTH - 550, 400)
        fonts.draw_text(list[1], fonts.fontfinal_media, white, SCREEN_WIDTH - 550, 500)
        fonts.draw_text(list[0], fonts.fontfinal_media, white, SCREEN_WIDTH - 550, 600)

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

                # volta pro menu
                if b4_left < w < (b4_left + b4_width) and b4_top < z < (b4_top + b4_height):
                    audio.introMusic.fadeout(1100)
                    sleep(0.5)
                    audio.button_cursor.play()
                    sleep(1.3)
                    init_screen.Init_screen()

            mouse = pygame.mouse.get_pos()

            if b4_left + b4_width > mouse[0] > b4_left and b4_top + b4_height > mouse[1] > b4_top:
                images.voltar_on = pygame.image.load('assets/images/voltar_on.png').convert_alpha()
            else:
                images.voltar_on = pygame.image.load('assets/images/voltar_off.png').convert_alpha()

        pygame.display.update()
        clock.tick(60)


