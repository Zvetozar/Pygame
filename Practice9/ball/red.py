import pygame
import random
pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

radius = 25
x, y = random.randint(1,1000) // 2, random.randint(1,1000) // 2
speed = 10  # уменьшили, чтобы было плавно

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - speed - radius >= 0:
        x -= speed
    if keys[pygame.K_RIGHT] and x + speed + radius <= WIDTH:
        x += speed
    if keys[pygame.K_UP] and y - speed - radius >= 0:
        y -= speed
    if keys[pygame.K_DOWN] and y + speed + radius <= HEIGHT:
        y += speed

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()