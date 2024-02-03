from diver import CanvasManager, Color
import math as m
from js import AudioContext

WIDTH = 720
HEIGHT = WIDTH
color_width = 5


background_color = Color(43, 51, 57)  # 2b3339

audioContext = AudioContext.new()
oscillator = audioContext.createOscillator()

oscillator.type = "sine"
oscillator.frequency.setValueAtTime(440, audioContext.currentTime)

oscillator.connect(audioContext.destination)
oscillator.start()

oscillator.stop(audioContext.currentTime + 2)


print(audioContext)


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
    ctx.translate(w * 0.5, h * 0.5)
    rotate_angle = t / 1000
    ctx.rotate(rotate_angle)
    ctx.lineWidth = 2
    for i in range(1, 20):
        ctx.rotate((m.pi / 32 * m.sin(rotate_angle)))
        draw_square(10 * (i + m.sin(0.3 * i * rotate_angle + m.pi / 4)))
    ctx.restore()


canvasManager = CanvasManager(update)
