import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

image_background = pygame.image.load('Practice10/AnimatedStreet.png')
image_player = pygame.image.load('Practice10/Player.png')
image_enemy = pygame.image.load('Practice10/Enemy.png')

pygame.mixer.music.load('Practice10/background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('Practice10/crash.wav')

font_big = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 30)

image_game_over = font_big.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 8
        self.generate()

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 2, 3])

        self.image = pygame.Surface((20, 20))
        if self.value == 1:
            self.image.fill((255, 215, 0))
        elif self.value == 2:
            self.image.fill((0, 255, 0))
        else:
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.speed = 4 + self.value
        self.generate()

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()


player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group(player, enemy, coin)
enemy_sprites = pygame.sprite.Group(enemy)

coins = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.move()

    screen.blit(image_background, (0, 0))

    for e in all_sprites:
        e.move()
        screen.blit(e.image, e.rect)

    # 💰 СБОР КОИНА (ИСПРАВЛЕНО)
    if pygame.sprite.collide_rect(player, coin):
        coins += coin.value
        coin.kill()  # ❗ удаляем старый коин
        coin = Coin()
        all_sprites.add(coin)

        if coins % 5 == 0:
            enemy.speed += 1

    # 💥 СТОЛКНОВЕНИЕ
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        exit()

    text = font_small.render(f"Coins: {coins}", True, (0,0,0))
    screen.blit(text, (250, 10))

    pygame.display.flip()
    clock.tick(60)