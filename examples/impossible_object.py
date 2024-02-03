from diver import CanvasManager
import math as m

WIDTH = 600
HEIGHT = WIDTH
print("hello from draw.py")


c1 = "#71847B"
c2 = "#859289"
c3 = "#9DA9A0"
cf = "#d3c6aa"


def update(self: CanvasManager, t):
    canvas = self.canvas
    ctx = self.ctx
    canvas.width = WIDTH
    canvas.height = HEIGHT

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    # put orign at center
    ctx.translate(WIDTH // 2, HEIGHT // 2)
    ctx.scale(30, -30)

    # spin the whole shape
    ctx.rotate(t / 2000)

    # I drew it on graph paper, and skewed it so that
    # everything fell on grid points
    xLength = 2
    yLength = m.sqrt(3)
    # correcting for that scale now
    ycorrection = yLength / xLength

    # fake parallax
    scalex = 1 + 0.1 * m.sin(t / 1000)
    scaley = 1 + 0.2 * m.sin(t / 500)
    ctx.scale(1 * scalex, ycorrection * scaley)

    # Center the shape
    ctx.translate(-6, -5)

    # start sketching
    # side 1
    ctx.lineWidth = 0.1
    ctx.strokeStyle = cf
    ctx.fillStyle = c3
    ctx.beginPath()
    ctx.moveTo(0, 2)
    ctx.lineTo(5, 12)
    ctx.lineTo(9, 4)
    ctx.lineTo(7, 4)
    ctx.lineTo(5, 8)
    ctx.lineTo(1, 0)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()

    # side 2
    ctx.fillStyle = c1
    ctx.beginPath()
    ctx.moveTo(4, 2)
    ctx.lineTo(5, 4)
    ctx.lineTo(9, 4)
    ctx.lineTo(5, 12)
    ctx.lineTo(7, 12)
    ctx.lineTo(12, 2)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()

    # side 3
    ctx.fillStyle = c2
    ctx.beginPath()
    ctx.moveTo(1, 0)
    ctx.lineTo(11, 0)
    ctx.lineTo(12, 2)
    ctx.lineTo(4, 2)
    ctx.lineTo(6, 6)
    ctx.lineTo(5, 8)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()


canvasManager = CanvasManager(update)
