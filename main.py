import math
import pygame

white = (255, 255, 255)
red = (255, 0, 0)
darkgrey = (25, 25, 25)

mouse_pos = (0, 0)

points = []

running = True

held_point = -1

lines_on = False


def events():
    global running, mouse_pos, held_point, lines_on
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if held_point >= 0:
                points[held_point] = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if held_point >= 0:
                    held_point = -1
                else:
                    for i, point in enumerate(points):
                        if dist(point, event.pos) < 1:
                            held_point = i
                            return

                    # 3 Points:
                    # if len(points) > 0:
                    #     points.append(lerp(points[len(points) - 1], event.pos, 0.5))

                    # 4 Points:
                    if len(points) > 0:
                        points.append(lerp(points[len(points) - 1], event.pos, 0.3))
                        points.append(lerp(points[len(points) - 1], event.pos, 0.6))

                    points.append(event.pos)

            elif event.button == 2:
                lines_on = not lines_on

            elif event.button == 3:

                # 3 Points:
                # if len(points) > 1:
                #     points.__delitem__(len(points) - 1)

                # 4 Points:
                if len(points) > 1:
                    points.__delitem__(len(points) - 1)
                    points.__delitem__(len(points) - 1)

                if len(points) > 0:
                    points.__delitem__(len(points) - 1)


def lines():
    for i in range(len(points) - 1):
        if (i - 1) % 3 != 0:
            p1 = points[i]
            p2 = points[i + 1]
            pygame.draw.line(screen, white, p1, p2)


def draw_points():
    if len(points) > 1:
        # 3 Points:
        # for i in range(len(points) - 2):
        #     if (i % 2) == 0:
        #         p1 = points[i]
        #         p2 = points[i + 1]
        #         p3 = points[i + 2]
        #
        #         d = int((dist(p1, p2) + dist(p2, p3)) * 0.8)
        #         for t in range(0, d, 1):
        #             t /= d
        #
        #             pos1 = lerp(p1, p2, t)
        #             pos2 = lerp(p2, p3, t)
        #
        #             pos3 = lerp(pos1, pos2, t)
        #
        #             pygame.draw.circle(screen, white, pos3, 1)

        # 4 Points:
        for i in range(len(points) - 3):
            if (i % 3) == 0:
                p1 = points[i]
                p2 = points[i + 1]
                p3 = points[i + 2]
                p4 = points[i + 3]

                d = int((dist(p1, p2) + dist(p2, p3)) + dist(p3, p4) * 0.7)
                for t in range(0, d, 1):
                    t /= d

                    pos1 = lerp(lerp(p1, p2, t), lerp(p2, p3, t), t)
                    pos2 = lerp(lerp(p2, p3, t), lerp(p3, p4, t), t)

                    pos3 = lerp(pos1, pos2, t)

                    pygame.draw.circle(screen, white, pos3, 1)


def draw_nodes():
    for count, point in enumerate(points):
        color = white
        if (count + 1) % 3 == 0 or (count - 1) % 3 == 0:
            color = red
        pygame.draw.circle(screen, color, point, 4)


def lerp(a, b, t):
    pos = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    return pos


def dist(p1, p2):
    d = math.sqrt(pow((p2[1] - p1[1]), 2) + pow((p2[0] - p1[0]), 2)) / 10
    return int(d)


def tick():
    print("Tick")


pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()

while running:

    events()
    screen.fill(darkgrey)

    draw_nodes()
    draw_points()

    if lines_on:
        lines()

    pygame.display.flip()

pygame.quit()
