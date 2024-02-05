from js import CanvasRenderingContext2D, HTMLCanvasElement, MouseEvent, document
from pyodide.ffi import create_proxy
from diver import CanvasManager
from dataclasses import dataclass
import numpy as np

WIDTH = 512
HEIGHT = WIDTH // 2
print("hello from draw.py")


@dataclass
class String:
    length: float = WIDTH
    n: int = 80
    xs = np.linspace(0, length, n)
    # points = np.zeros(xs.shape)
    amplitude = 50
    n_periods = 21
    # points = np.sin(2*m.pi*(xs/length)* n_periods) * amplitude
    points = np.zeros(xs.shape)
    past_points = points
    physical_const = 0.1
    should_update = True
    damping = 0.1

    def update(self, dt):  # TODO properly handle dt
        if not self.should_update:
            return
        new_points = self.points.copy()

        for i in range(1, self.n - 1):
            y = (
                self.physical_const * (self.points[i - 1] + self.points[i + 1] - 2 * self.points[i])
                + 2 * self.points[i]
                - self.past_points[i]
            )
            # niave damping
            # y_damp = y * (1/self.damping) * 1/(1+(self.points[i] - self.past_points[i])**2)
            new_points[i] = y
        self.past_points = self.points.copy()  # are these copies necessary?
        self.points = new_points.copy()

    def draw(self, ctx: CanvasRenderingContext2D):
        # move to the first point
        ctx.translate(0, HEIGHT // 2)
        ctx.lineWidth = 2
        ctx.moveTo(self.xs[0], self.points[0])

        for i, x in enumerate(self.xs[1:-1]):
            x = self.xs[i]
            y = self.points[i]
            xc = (x + self.xs[i + 1]) / 2
            yc = (y + self.points[i + 1]) / 2

            ctx.quadraticCurveTo(x, y, xc, yc)
            # ctx.lineTo(x,y)
        ctx.quadraticCurveTo(self.xs[-2], self.points[-2], self.xs[-1], self.points[-1])

        ctx.stroke()


string = String()


def update(cm: CanvasManager, time_milli):
    # update
    string.update(time_milli)
    # draw
    canvas = cm.canvas
    ctx = cm.ctx
    canvas.width = WIDTH
    canvas.height = HEIGHT

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.save()
    ctx.strokeStyle = "#d3c6aa"
    string.draw(ctx)
    # ctx.moveTo(0,0)
    # ctx.lineTo(500.1,0.0)
    # ctx.lineTo(600.1,0.0)
    # ctx.lineTo(700.1,0.0)
    # ctx.stroke()
    ctx.restore()


cm = CanvasManager(update)


def plucked(x, y):
    if not (0 < x < WIDTH and -HEIGHT // 2 < y < HEIGHT // 2):
        return
    # set an initial condition of a ramp up to the mouse, then down toward the fixed end
    string_percent = x / string.length
    click_index = int(string.n * string_percent)

    # we want to maintain boundary condition
    if click_index == 0 or click_index == string.n - 1:
        return

    string.points[0:click_index] = np.linspace(0, y, click_index)
    string.points[click_index:] = np.linspace(y, 0, string.n - click_index)

    # if we don't do this, then the string thinks it is moving toward the
    # mouse really quickly
    string.past_points = string.points.copy()


def move_end(_, y):
    if y > HEIGHT // 2:
        y = HEIGHT // 2
    if y < -HEIGHT // 2:
        y = -HEIGHT // 2
    # set an initial condition of a ramp up to the mouse, then down toward the fixed end

    string.points[0] = y

    # if we don't do this, then the string thinks it is moving toward the
    # mouse really quickly
    # string.past_points[0] = y


def getCanvasCursorPosition(canvas: HTMLCanvasElement, event: MouseEvent):
    rect = canvas.getBoundingClientRect()
    print(rect.top)
    return event.clientX - rect.left, event.clientY - rect.top - HEIGHT // 2


def onMouseDown(_: MouseEvent):
    document.addEventListener("mousemove", onMouseMove_proxy)
    document.addEventListener("mouseup", onMouseUp_proxy)
    string.should_update = True


def onMouseMove(event: MouseEvent):
    x, y = getCanvasCursorPosition(cm.canvas, event)
    move_end(x, y)


def onMouseUp(_: MouseEvent):
    document.removeEventListener("mousemove", onMouseMove_proxy)
    document.removeEventListener("mousemove", onMouseUp_proxy)
    string.should_update = True


onMouseDown_proxy = create_proxy(onMouseDown)
onMouseMove_proxy = create_proxy(onMouseMove)
onMouseUp_proxy = create_proxy(onMouseUp)

text = document.getElementById("simulation-description")
if text is None:
    text = document.createElement("div")
    text.id = "simulation-description"
    text.textContent = "Click and drag string up/down"
    document.body.appendChild(text)  # type: ignore


cm.canvas.addEventListener("mousedown", create_proxy(onMouseDown))
