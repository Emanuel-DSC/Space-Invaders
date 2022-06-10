import pygame
import fonts
from pygame import mixer
import images
import init_screen

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
last_shot = pygame.time.get_ticks()
count = 3
last_count = pygame.time.get_ticks()
game_over = 0
green = (0, 255, 0)
white = (255, 255, 255)


def draw_bg():
    screen.blit(images.bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.spaceship
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):

        speed = 8
        cd = 300
        game_over = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > cd:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)
        if self.health_remaining <= 0:
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
            spaceship.health_remaining -= 1


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

        if len(alien_group) == 0:
            game_over = 1
            spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()

        if game_over == 0:
            spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()

    if count > 0:
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 100:
            count -= 1
            last_count = count_timer

    explosion_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    fonts.draw_text(str(clock), fonts.fontfinal, green, 20, 30)
    fonts.draw_text('PONTOS:' + str(Bullets.score), fonts.fontfinal, white, 500, 30)

    pygame.display.update()

pygame.quit()
