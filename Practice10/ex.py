import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake = [(100,100), (80,100), (60,100)]
direction = (20, 0)

# 👉 теперь список еды
foods = []

def generate_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
        if pos not in snake and pos not in foods:
            return pos

# создаём 2 яблока
for _ in range(2):
    foods.append(generate_food())

score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    # границы
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # столкновение с собой
    if head in snake[1:]:
        pygame.quit()
        sys.exit()

    # проверка еды
    if head in foods:
        score += 1
        foods.remove(head)
        foods.append(generate_food())

        # уровни
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    screen.fill((0,0,0))

    # змейка
    for segment in snake:
        pygame.draw.rect(screen, (0,255,0), (*segment, CELL, CELL))

    # еда (теперь несколько)
    for food in foods:
        pygame.draw.rect(screen, (255,0,0), (*food, CELL, CELL))

    # текст
    text = font.render(f"Score: {score}  Level: {level}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(speed)