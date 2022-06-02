import pygame
from pygame import mixer

mixer.init()

button_confirma = pygame.mixer.Sound('assets/audio/confirm.wav')
button_confirma.set_volume(0.5)
button_cursor = pygame.mixer.Sound('assets/audio/cursor.wav')
button_cursor.set_volume(1.5)
introMusic = pygame.mixer.Sound('assets/audio/Spaceship.ogg')
introMusic.set_volume(0.3)