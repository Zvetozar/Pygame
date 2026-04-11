import pygame
pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

radius = 25
x, y = WIDTH // 2, HEIGHT // 2
speed = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x - speed - radius >= 0:
                x -= speed
            elif event.key == pygame.K_RIGHT and x + speed + radius <= WIDTH:
                x += speed
            elif event.key == pygame.K_UP and y - speed - radius >= 0:
                y -= speed
            elif event.key == pygame.K_DOWN and y + speed + radius <= HEIGHT:
                y += speed

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pygame.display.flip()

pygame.quit()