import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    canvas = pygame.Surface((640, 480))
    canvas.fill((255, 255, 255))

    mode = 'blue'
    tool = 'brush'
    radius = 5

    drawing = False
    start_pos = None
    last_pos = None

    def get_color(mode):
        if mode == 'blue':
            return (0, 0, 255)
        elif mode == 'red':
            return (255, 0, 0)
        elif mode == 'green':
            return (0, 255, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # цвета
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # инструменты
                elif event.key == pygame.K_1:
                    tool = 'brush'
                elif event.key == pygame.K_2:
                    tool = 'rect'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_4:
                    tool = 'eraser'
                elif event.key == pygame.K_5:
                    tool = 'square'
                elif event.key == pygame.K_6:
                    tool = 'triangle'
                elif event.key == pygame.K_7:
                    tool = 'eq_triangle'
                elif event.key == pygame.K_8:
                    tool = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos

                if tool == 'rect':
                    pygame.draw.rect(
                        canvas,
                        get_color(mode),
                        pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])),
                        2
                    )

                elif tool == 'circle':
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = min(100, int((dx**2 + dy**2) ** 0.5))
                    pygame.draw.circle(canvas, get_color(mode), start_pos, r, 2)

                # 🔲 квадрат
                elif tool == 'square':
                    size = abs(end_pos[0] - start_pos[0])
                    pygame.draw.rect(canvas, get_color(mode),
                        pygame.Rect(start_pos[0], start_pos[1], size, size), 2)

                # 🔺 прямоугольный треугольник
                elif tool == 'triangle':
                    pygame.draw.polygon(canvas, get_color(mode), [
                        start_pos,
                        (start_pos[0], end_pos[1]),
                        end_pos
                    ], 2)

                # 🔺 равносторонний треугольник
                elif tool == 'eq_triangle':
                    size = abs(end_pos[0] - start_pos[0])
                    h = size * math.sqrt(3) / 2

                    pygame.draw.polygon(canvas, get_color(mode), [
                        (start_pos[0], start_pos[1]),
                        (start_pos[0] + size, start_pos[1]),
                        (start_pos[0] + size//2, start_pos[1] - h)
                    ], 2)

                # 🔷 ромб
                elif tool == 'rhombus':
                    cx = (start_pos[0] + end_pos[0]) // 2
                    cy = (start_pos[1] + end_pos[1]) // 2

                    pygame.draw.polygon(canvas, get_color(mode), [
                        (cx, start_pos[1]),
                        (end_pos[0], cy),
                        (cx, end_pos[1]),
                        (start_pos[0], cy)
                    ], 2)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.line(canvas, get_color(mode), last_pos, event.pos, radius)
                        last_pos = event.pos

                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, (255,255,255), event.pos, 10)

        screen.blit(canvas, (0,0))
        pygame.display.flip()
        clock.tick(60)

main()