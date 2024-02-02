from proceso import Sketch
from js import window
from dataclasses import dataclass
import math as m
from typing import List, Optional


p5 = Sketch()
p5.describe(
    "A grid of green spirals on a black background. The spirals change their motion based on the mouse position."
)

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0


def resize_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH, HEIGHT
    if SCREEN_WIDTH == window.innerWidth and SCREEN_HEIGHT == window.innerHeight:
        return
    SCREEN_WIDTH, SCREEN_HEIGHT = window.innerWidth, window.innerHeight
    margin_vertical = 50
    margin_horizontal = 50
    WIDTH = SCREEN_WIDTH - margin_horizontal * 2
    HEIGHT = SCREEN_HEIGHT - margin_vertical * 2
    p5.resize_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)


resize_screen()


@dataclass
class Point:
    x: int | float
    y: int | float


def setup():
    p5.create_canvas(window.innerWidth, window.innerHeight)
    p5.no_stroke()
    p5.clear()
    p5.fill(40, 200, 40)
    p5.background(0)


def draw():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    p5.background(0, 200)  # translucent background (creates trails)
    resize_screen()

    p5.no_fill()
    p5.stroke(40, 200, 40)

    p5.translate(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    p5.scale(1, -1)

    # p5.rect(-WIDTH // 2, -HEIGHT // 2, WIDTH, HEIGHT)

    # draw_atan()
    draw_atan2()
    draw_triangles()


def draw_atan2():
    xs = range(-10, 11)
    ys = range(-10, 11)
    grid = [[int((m.atan2(-x, -y) / 2 + 0.5) * 100) for x in xs] for y in ys]
    draw_grid(grid)


def draw_grid(grid: List[List[int]], show_grid_lines=False, width: Optional[int] = None) -> None:
    p5.push()
    if width is None:
        size = min(WIDTH, HEIGHT) // len(grid)
    else:
        size = width // len(grid)

    if show_grid_lines is False:
        p5.no_stroke()

    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            p5.fill(val)
            p5.rect(x * size - WIDTH // 2, y * size - HEIGHT // 2, size, size)

    p5.pop()


def draw_atan():
    for x in range(-WIDTH // 2, WIDTH // 2, 10):
        p1 = Point(x, m.atan(x))
        x2 = x + 10
        p2 = Point(x2, m.atan(x2))

        xs = 50
        ys = 50

        p1.x *= xs
        p2.x *= xs
        p1.y *= ys
        p2.y *= ys
        p5.line(p1.x, p1.y, p2.x, p2.y)


def draw_triangles():
    height = min(WIDTH // 2, HEIGHT // 2)
    half_base = height / m.sqrt(2)

    num_triangles = 50

    mx = p5.mouse_x - SCREEN_WIDTH // 2
    my = -1 * (p5.mouse_y - SCREEN_WIDTH // 2)
    mAngle = m.atan2(my, mx)
    totalRotation = mAngle if p5.is_mouse_pressed else 2 * m.pi
    dTheta = (totalRotation) / num_triangles

    p5.push()
    p5.stroke(40, 200, 40)
    p5.scale(1, -1)
    p5.translate(-SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2)
    mx = p5.mouse_x
    my = p5.mouse_y
    p5.line(mx, my, p5.pmouse_x, p5.pmouse_y)
    p5.pop()

    for i in range(num_triangles):
        p1 = Point(-half_base, 0)
        p2 = Point(half_base, 0)
        p3 = Point(0, height)
        p5.triangle(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)
        p5.rotate(dTheta)


p5.run_sketch(setup=setup, draw=draw)
