import math

import pygame
import pygame.gfxdraw

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

running = True
negate = False
percentage = 0.0
fps = 240
points = [(200, 300), (400, 100), (400, 500), (600, 300)]
line = []
held_point = -1


def lerp(a, b, t):
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


def dist(p1, p2):
    return math.sqrt(pow((p2[1] - p1[1]), 2) + pow((p2[0] - p1[0]), 2)) / 10


def AnimatedSingleBezier():
    for point in points:
        pygame.draw.circle(screen, red, point, 4)
    pygame.draw.line(screen, red, points[0], points[1], 1)
    pygame.draw.line(screen, red, points[1], points[2], 1)
    pygame.draw.line(screen, red, points[2], points[3], 1)

    p1 = lerp(points[0], points[1], percentage)
    p2 = lerp(points[1], points[2], percentage)
    p3 = lerp(points[2], points[3], percentage)
    pygame.draw.circle(screen, blue, p1, 4)
    pygame.draw.circle(screen, blue, p2, 4)
    pygame.draw.circle(screen, blue, p3, 4)
    pygame.draw.line(screen, blue, p1, p2, 1)
    pygame.draw.line(screen, blue, p2, p3, 1)

    p4 = lerp(p1, p2, percentage)
    p5 = lerp(p2, p3, percentage)
    pygame.draw.circle(screen, green, p4, 4)
    pygame.draw.circle(screen, green, p5, 4)
    pygame.draw.line(screen, green, p4, p5, 1)

    p6 = lerp(p4, p5, percentage)
    pygame.draw.circle(screen, black, p6, 4)
    line.append(p6)
    for i in range(len(line) - 1):
        p1 = line[i]
        p2 = line[i + 1]
        pygame.draw.line(screen, black, p1, p2, 1)


def draw():
    screen.fill(white)

    AnimatedSingleBezier()

    pygame.display.flip()


def update():
    global percentage, clock, fps, negate

    dt = clock.get_time() / 10000  # Delta time: The time since last frame.

    if negate:
        percentage -= 4 * dt
    else:
        percentage += 4 * dt

    if percentage >= 1:
        line.clear()
        negate = True
    elif percentage <= 0:
        line.clear()
        negate = False

    draw()


def events():
    global running, held_point
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if held_point >= 0:
                points[held_point] = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if held_point >= 0:
                held_point = -1
            else:
                for i, point in enumerate(points):
                    if dist(event.pos, point) < 1.0:
                        held_point = i


pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()

while running:
    events()
    update()
    clock.tick(fps)

pygame.quit()
