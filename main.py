import pygame
import init_screen

init_screen.Init_screen()


class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False

        hero = Hero(self, width / 2, height - 20)
        generator = Generator(self)
        rocket = None

        previous_time = pygame.time.get_ticks()

        while not done:

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and not self.lost:
                    current_time = pygame.time.get_ticks()
                    if current_time - previous_time > 600:
                        previous_time = current_time
                        self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((255, 255, 255))

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost: hero.draw()

            self.displayText(str(self.clock))

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 14)
        textsurface = font.render(text, False, (0, 200, 0))
        self.screen.blit(textsurface, (10, 5))


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (240, 0, 255),
                         pygame.Rect(self.x, self.y, 10, 7))


class Generator:
    def __init__(self, game):
        margin = 30
        width = 50


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), pygame.Rect(self.x, self.y, 4, 6))
        self.y -= 2


if __name__ == '__main__':
    game = Game(600, 400)

