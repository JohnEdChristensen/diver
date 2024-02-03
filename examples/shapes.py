# DRAFT SKETCH EXAMPLE!
from js import CanvasRenderingContext2D
from diver import CanvasManager
import math as m
from dataclasses import dataclass

WIDTH = 3200
HEIGHT = WIDTH
print("hello from draw.py")


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    def to_string(self):
        return f"rgba({self.r},{self.g},{self.b},{self.a})"


@dataclass
class DiverCtx:
    ctx: CanvasRenderingContext2D

    def draw_line(self, p1: Point, p2: Point | None = None, c: Color | None = None, width: int | None = None):
        ctx = self.ctx
        if c is not None:
            ctx.strokeStyle = c.to_string()
        if width is not None:
            ctx.lineWidth = 1

        if p2 is not None:
            ctx.moveTo(p1.x, p1.y)
            ctx.lineTo(p2.x, p2.y)
        if p1 is not None:
            ctx.lineTo(p1.x, p1.y)
        ctx.stroke()

    def drawT1(self, width=50.0):
        ctx = self.ctx
        ctx.save()
        ctx.moveTo(0, 0)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 2)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-(m.pi - m.pi / 2))
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 2)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.stroke()
        ctx.restore()

    def drawT2(self, width=50.0):
        # angle=30
        ctx = self.ctx
        ctx.save()
        ctx.moveTo(0, 0)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 6)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-(m.pi - m.pi / 6))
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 6)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.stroke()
        ctx.restore()

    def drawT3(self, width=50.0):
        # angle=30
        ctx = self.ctx
        ctx.save()
        ctx.moveTo(0, 0)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 4)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-(m.pi - m.pi / 4))
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.rotate(-m.pi / 4)
        ctx.lineTo(width, 0)
        ctx.translate(width, 0)
        ctx.stroke()
        ctx.restore()


def update(self: CanvasManager, t):
    canvas = self.canvas
    dtx = DiverCtx(self.ctx)
    canvas.width = WIDTH
    canvas.height = HEIGHT
    w, h = WIDTH, HEIGHT

    dtx.ctx.clearRect(0, 0, canvas.width, canvas.height)

    dtx.ctx.translate(w * 0.5, h * 0.5)
    dtx.ctx.scale(4, 4)
    dtx.ctx.lineWidth = 2
    dtx.ctx.strokeStyle = "#d3c6aa"

    rotate_angle = 2 * m.pi * t / 1000 * 1 / 2
    a1 = 0.2
    wave1 = (1 - a1) + m.sin(rotate_angle) * a1
    a2 = 0.2
    wave2 = 0.3 + m.sin(rotate_angle) * a2
    length = 50
    l1 = length + length * wave1
    l2 = length * wave2
    for _ in range(12):
        dtx.drawT2(l1)
        dtx.ctx.rotate(m.pi / 6)

    dtx.ctx.lineWidth = 1
    for _ in range(12):
        dtx.drawT2(l1 // 2)
        dtx.ctx.rotate(m.pi / 6)

    dtx.ctx.strokeStyle = "#d3c6aa"
    dtx.ctx.beginPath()
    dtx.ctx.fillStyle = "#83C092"
    dtx.ctx.lineWidth = 1
    for _ in range(12):
        dtx.drawT2(l2)
        dtx.ctx.rotate(m.pi / 6)

    dtx.ctx.fill()
    for _ in range(12):
        dtx.drawT2(l2)
        dtx.ctx.rotate(m.pi / 6)


canvasManager = CanvasManager(update)
