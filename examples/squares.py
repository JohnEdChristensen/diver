from diver import CanvasManager
import math as m
from js import window

WIDTH = window.innerWidth
HEIGHT = window.innerHeight
WIDTH = HEIGHT = min(WIDTH, HEIGHT)
MARGIN = WIDTH * 0.99
print("hello from draw.py")


def update(self: CanvasManager, t):
    canvas = self.canvas
    ctx = self.ctx
    canvas.width = WIDTH
    canvas.height = HEIGHT
    w, h = WIDTH, HEIGHT

    def draw_square(size):
        ctx.strokeRect(-size, -size, size * 2, size * 2)

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.save()

    ctx.strokeStyle = "#d3c6aa"

    # y up, origin screen center
    ctx.translate(w * 0.5, h * 0.5)
    ctx.scale(1, -1)

    rotate_angle = t / 1000
    ctx.rotate(rotate_angle)

    ctx.lineWidth = 2
    number_of_square = 20
    max_width = (WIDTH - MARGIN) / m.sqrt(2)
    for i in range(1, number_of_square):
        ctx.rotate((m.pi / 32 * m.sin(rotate_angle)))
        base_length = max_width // 2 * (number_of_square - i)
        size = base_length * (i + m.sin(0.3 * i * rotate_angle + m.pi / 4))
        draw_square(size)
    ctx.restore()


canvasManager = CanvasManager(update)
