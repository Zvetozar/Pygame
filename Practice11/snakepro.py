import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100,100), (80,100), (60,100)]
direction = (CELL, 0)

foods = []

def generate_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        if pos not in snake:
            return {
                "pos": pos,
                "value": random.choice([1,2,3]),
                "time": pygame.time.get_ticks()
            }

# создаём 2 еды
for _ in range(2):
    foods.append(generate_food())

score = 0
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

    # в себя
    if head in snake[1:]:
        pygame.quit()
        sys.exit()

    current_time = pygame.time.get_ticks()

    # удаляем старую еду
    foods = [f for f in foods if current_time - f["time"] < 5000]

    # ДОБАВЛЯЕМ НОВУЮ (ВАЖНО)
    while len(foods) < 2:
        foods.append(generate_food())

    # проверка еды
    ate = False
    for f in foods:
        if head == f["pos"]:
            score += f["value"]
            foods.remove(f)
            ate = True
            break

    if not ate:
        snake.pop()

    screen.fill((0,0,0))

    # змейка
    for s in snake:
        pygame.draw.rect(screen, (0,255,0), (*s, CELL, CELL))

    # еда
    for f in foods:
        color = (255,0,0) if f["value"] == 1 else (0,255,0) if f["value"] == 2 else (0,0,255)
        pygame.draw.rect(screen, color, (*f["pos"], CELL, CELL))

    # текст
    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(speed)