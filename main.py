import pygame, sys
import random
import fonts
from pygame import mixer
import images
import ranking_page
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

list = []
user_text = ''
i = 5
j = 5
alien_shot_cooldown = 1000
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
    boss_lives = 3

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

        if pygame.sprite.spritecollide(self, boss_group, False):
            self.kill()
            Bullets.boss_lives -= 1
            print(Bullets.boss_lives)

        if Bullets.boss_lives == 0:
            pygame.sprite.spritecollide(self, boss_group, True)


class Aliens(pygame.sprite.Sprite):
    move_speed = 10

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
            self.move_x *= -1
            self.rect.y += Aliens.move_speed
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
boss_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()


def create_aliens():
    list_alien = []
    for row in range(i):
        for item in range(j):
            alien = Aliens(100 + item * 100, 100 + row * 70)

            # cria a lista de aliens
            list_alien.append(alien)
            alien_group.add(alien)

    # aleatoriamente seleciona um alien , o remove do grupo aliens e poe como boss
    boss = random.choice(list_alien)
    alien_group.remove(boss)
    boss_group.add(boss)
    boss.image = images.boss


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

        if len(alien_group) == 0 and len(boss_group) == 0:
            create_aliens()
            Aliens.move_speed += 4
            alien_shot_cooldown -= 100
            spaceship.update()
            bullet_group.update()
            boss_group.update()
            alien_group.update()
            alien_bullet_group.update()

        if game_over == 0:
            game_over = spaceship.update()
            bullet_group.update()
            alien_group.update()
            boss_group.update()
            alien_bullet_group.update()

    if count > 0:
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 100:
            count -= 1
            last_count = count_timer

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    boss_group.draw(screen)

    if spaceship.lives_remaining <= 0:
        # som derrota
        spaceship_group.empty()
        bullet_group.empty()
        alien_group.empty()
        alien_bullet_group.empty()
        draw_bg()
        fonts.draw_text('PONTOS:\n' + str(Bullets.score), fonts.fontfinal_grande, white, screen_width / 2 - 300,
                        screen_height/2 - 300)
        fonts.draw_text('DIGITE SEU NOME:\n', fonts.fontfinal_grande, white, screen_width/2 - 300,
                        screen_height/2 - 200)
        fonts.draw_text('APERTE ENTER', fonts.fontfinal_grande, white, 100, 600)
        fonts.draw_text('PARA CONCLUIR', fonts.fontfinal_grande, white, 100, 700)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # ONDE TIVE MAIOR DIFICULDADE
            # Se a vida for menor ouu igual a 0, captura o texto do jogador (nome) , caso aperte ENTER , salva o nome
            # e o placar. Depois encerra o loop e abre a pagina de ranking
        if spaceship.lives_remaining <= 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                with open('high_score.txt', 'a') as file:
                    file.write(f"{user_text}: {Bullets.score}\n")
                run = False
                ranking_page.Ranking_page()
            if event.type == pygame.KEYDOWN:
                user_text += event.unicode
            key = pygame.key.get_pressed()

    fonts.draw_text(user_text, fonts.fontfinal_grande, green, screen_width/2 - 50, screen_height/2 - 150)

    # fonts.draw_text(user_text, fonts.fontfinal, red, 220, 230)

    fonts.draw_text(str(clock), fonts.fontfinal, green, 20, 30)
    fonts.draw_text('PONTOS:' + str(Bullets.score), fonts.fontfinal, white, 500, 30)
    fonts.draw_text('VIDAS:' + str(spaceship.lives_remaining), fonts.fontfinal, white, 270, 30)

    pygame.display.update()

pygame.quit()
