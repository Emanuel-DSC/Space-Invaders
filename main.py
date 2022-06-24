import pygame
import random
import fonts
from pygame import mixer
import images
import init_screen
from time import sleep

init_screen.Init_screen()

mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders Clone')

i = 5
j = 5
alien_shot_cooldown = random.randint(700, 1000)
last_alien_shot = pygame.time.get_ticks()
last_shot = pygame.time.get_ticks()
count = 3
last_count = pygame.time.get_ticks()
game_over = 0
green = (0, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)


def draw_bg():
    screen.blit(images.bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, lives):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.spaceship
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.lives_start = lives
        self.lives_remaining = lives
        self.last_shot = pygame.time.get_ticks()
        self.pause = 0

    def update(self):

        if self.pause:
            self.pause -= 1
            return

        speed = 8
        cd = 300
        game_over = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
            self.image = images.spaceship
        if key[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += speed
            self.image = images.spaceship

        actual_time = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and actual_time - self.last_shot > cd:
            #add som de tiro
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = actual_time

        self.mask = pygame.mask.from_surface(self.image)

        if self.lives_remaining <= 0:
            self.kill()
            game_over = -1
        return game_over


class Bullets(pygame.sprite.Sprite):
    score = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.bullet
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            Bullets.score += 50


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.alien
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_x = 1
        self.move_y = 1

    def update(self):

        self.rect.x += self.move_x
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.rect.y += 15
            self.move_x *= -1
            self.move_counter *= self.move_x

        if self.rect == spaceship.rect:
            spaceship.lives_remaining -= 1


class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.alien_bullet
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.lives_remaining -= 1
            spaceship.image = images.spaceship_shield
            spaceship.rect.center = [300, 700]


spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    for row in range(i):
        for item in range(j):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()

spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)


run = True
while run:

    clock.tick(fps)

    draw_bg()

    if count == 0:

        actuall_time = pygame.time.get_ticks()

        if actuall_time - last_alien_shot > alien_shot_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = actuall_time

        if len(alien_group) == 0:
            game_over = 1
            spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()

        if game_over == 0:
            game_over = spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:
                fonts.draw_text('DERROTA', fonts.fontfinal_grande, red, (screen_width / 2 - 180), (screen_height / 2
                                                                                                   + 100))
                sleep(2)
                init_screen.Init_screen()
            if game_over == 1:
                fonts.draw_text('VITÓRIA', fonts.fontfinal_grande, green, (screen_width / 2 - 180), (screen_height / 2
                                                                                                     + 100))

    if count > 0:
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 100:
            count -= 1
            last_count = count_timer

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    fonts.draw_text(str(clock), fonts.fontfinal, green, 20, 30)
    fonts.draw_text('PONTOS:' + str(Bullets.score), fonts.fontfinal, white, 500, 30)
    fonts.draw_text('VIDAS:' + str(spaceship.lives_remaining), fonts.fontfinal, white, 270, 30)

    pygame.display.update()

pygame.quit()
