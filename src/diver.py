import sys
import traceback
from dataclasses import dataclass
from typing import List, Tuple, cast
import numpy as np

from js import (  # pyright: ignore
    CanvasRenderingContext2D,
    HTMLCanvasElement,
    ImageData,
    document,
    window,
)
from pyodide.ffi import create_proxy


from proceso import Sketch as procesoSketch
from typing import TypedDict
from typing_extensions import Unpack
from enum import Enum, auto
import time

SCREEN_WIDTH = SCREEN_HEIGHT = WIDTH = HEIGHT = 0


class Origin(Enum):
    CENTER = auto()
    TOP_LEFT = auto()


class SketchConfig(TypedDict, total=False):
    margin: int
    auto_fill_screen: bool
    origin: Origin


print("Hello from diver setup")


@dataclass
class Sketch(procesoSketch):
    """proceso wrapper class with helpers"""

    def __init__(self, **options: Unpack[SketchConfig]):
        print("starting diver sketch")
        super().__init__()
        self.margin = options.get("margin", 50)
        self.origin = options.get("origin", Origin.CENTER)
        self.auto_fill_screen = options.get("auto_fill_screen")

        self._update_system_variables()

        self.world_offset_x = 0
        self.world_offset_y = 0
        self.world_zoom_scale = 1
        self.diver_draw_end_time = time.time()

    # proceso seems to not refresh self.window_width and height well
    def debug_screen(self, desc):
        self.push()
        # print(f"{desc:20},js       :{window.innerWidth:4},{window.innerHeight:4}")
        # print(f"{desc:20},p5 window:{self.window_width:4},{self.window_height:4}")
        # print(f"{desc:20},p5 canvas:{self.width:4},{self.height:4}")

        # print(self.screen_left, self.screen_middle_x, self.screen_right)
        # print(self.screen_bottom, self.screen_middle_y, self.screen_top)
        # Axis
        self.stroke("green")
        self.stroke_weight(5)
        self.line(
            self.screen_left + 1,
            self.screen_top,
            self.screen_left + 1,
            self.screen_bottom,
        )
        self.line(
            0,
            self.screen_top,
            0,
            self.screen_bottom,
        )
        self.line(
            self.screen_right - 1,
            self.screen_top,
            self.screen_right - 1,
            self.screen_bottom,
        )

        self.stroke("red")
        self.line(
            self.screen_left,
            self.screen_top - 1,
            self.screen_right,
            self.screen_top - 1,
        )
        self.line(
            self.screen_left,
            0,
            self.screen_right,
            0,
        )
        self.line(
            self.screen_left, self.screen_bottom, self.screen_right, self.screen_bottom
        )

        self.pop()

    def square_draw_area(self):
        """set the width and height as large as possible while still square"""
        figure_width = window.innerWidth - 2 * self.margin
        figure_height = window.innerHeight - 2 * self.margin

        # Make a square drawing area, based on the smaller dimension
        self.figure_width = min(figure_width, figure_height)
        self.figure_height = figure_width
        self.figure_bottom = -self.figure_height // 2
        self.figure_top = self.figure_height // 2
        self.figure_left = -self.figure_width // 2
        self.figure_right = self.figure_width // 2

    def fill_screen(self):
        # print(self.world_zoom_scale)
        # init
        self.screen_bottom = -1 * window.innerHeight / 2
        self.screen_top = window.innerHeight / 2
        self.screen_left = -1 * window.innerWidth / 2
        self.screen_right = window.innerWidth / 2

        if self.width != window.innerWidth or self.height != window.innerHeight:
            print("resizing canvas")
            self.resize_canvas(window.innerWidth, window.innerHeight)

    def setup_screen(self):
        self.fill_screen()
        self.square_draw_area()

        if self.origin == Origin.CENTER:
            self.translate(self.width // 2, self.height // 2)
            self.scale(1, -1)

        # TODO make sure this works in both oriing modes
        self.translate(self.world_offset_x, self.world_offset_y)

        # TODO IMPORTANT Fix this... Grid lines should still work when moving
        self.screen_top -= self.world_offset_y
        self.screen_bottom -= self.world_offset_y
        self.screen_left -= self.world_offset_x
        self.screen_right -= self.world_offset_x
        # self.screen_middle_y = (self.screen_top + self.screen_bottom) // 2
        # self.screen_middle_x = (self.screen_left + self.screen_right) // 2

        s = 1 / self.world_zoom_scale
        self.screen_bottom *= s
        self.screen_top *= s
        self.screen_left *= s
        self.screen_right *= s

    def apply_zoom(self, s):
        self.world_zoom_scale = self.world_zoom_scale * s
        self.world_zoom_scale = max(min(self.world_zoom_scale, 2.0), 0.1)
        # print(self.world_zoom_scale)
        # world_mouse_x = self.mouse_x - self.width // 2
        # world_mouse_y = -1 * (self.mouse_y - self.height // 2)
        # self.world_offset_x = world_mouse_x * (1 - s) + self.world_offset_x * s
        # self.world_offset_y = world_mouse_y * (1 - s) + self.world_offset_y * s
        # print(self.world_offset_x, self.world_offset_y)
        # print(world_mouse_x, world_mouse_y)

    def text(
        self,
        txt: str,
        x: float,
        y: float,
        x2: float | None = None,
        y2: float | None = None,
    ) -> None:
        """Override p5js text to handle flipping y axis for text"""
        self.push()
        if self.origin == Origin.CENTER:
            self.scale(1, -1)
            y = -y
            if y2 is not None:
                y2 = -y2
        super().text(txt, x, y, x2, y2)
        self.pop()
        return

    def diver_setup(self):
        self.setup_screen()
        self.user_setup()

    def diver_draw(self):
        # print(f"time between loop: {self.diver_draw_end_time - time.time()}")
        self.diver_start_draw_time = time.time()
        speed = 10
        if self.key_is_down(self.RIGHT_ARROW):  # type: ignore
            self.world_offset_x -= speed
        if self.key_is_down(self.LEFT_ARROW):  # type: ignore
            self.world_offset_x += speed
        if self.key_is_down(self.UP_ARROW):  # type: ignore
            self.world_offset_y -= speed
        if self.key_is_down(self.DOWN_ARROW):  # type: ignore
            self.world_offset_y += speed

        # setup world units
        self.setup_screen()
        self.scale(self.world_zoom_scale)

        # print(f"diver setup time: {self.diver_start_draw_time - time.time()}")
        # self.debug_screen("draw")
        # finally call user's draw
        self.user_draw_start_time = time.time()
        self.user_draw()
        self.diver_draw_end_time = time.time()
        # print(
        #     f"user draw  time: {self.user_draw_start_time - self.diver_draw_end_time}"
        # )

    def mouse_wheel(self, event):
        scale = 1.05 if event.deltaY > 0 else 0.95

        self.apply_zoom(scale)

    def start(self, user_setup, user_draw):
        self.user_setup = user_setup
        self.user_draw = user_draw

        self.run_sketch(
            setup=self.diver_setup, draw=self.diver_draw, mouse_wheel=self.mouse_wheel
        )


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255


@dataclass
class Image:
    width: int
    height: int
    pixels: List[List[Tuple[int, int, int, int]]]

    def draw_pixel(self, x: int, y: int, c: Color) -> None:
        # Draw a single pixel to the image.
        # x=0,y=0 is the top left of the image.
        # y **increases** the further you go down the screen
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = (c.r, c.g, c.b, 255)


class CanvasManager:
    def __init__(self, animate_func, resetTime=True, canvas=None):
        global currentCanvasManager
        # `diverRootId` is set dynamically from javascript
        self.rootElement = document.getElementById(diverRootId)  # pyright: ignore # noqa
        self.shadowRootElement = document.getElementById(
            diverRootId  # pyright: ignore # noqa
        ).shadowRoot  # pyright: ignore # noqa
        # currently only supports one loop
        if currentCanvasManager is not None:
            currentCanvasManager.cancelAnimationLoop()
        currentCanvasManager = self
        print("hello from CanvasManager, ('diver.py')")
        if self.shadowRootElement is None:
            print("Root element (diverID for now) was not found. Exiting")
            return
        self.animate_func = animate_func
        self.animate_loop_proxy = create_proxy(self.animate_loop)
        if canvas is None:  # diver canvas
            self.canvas = cast(
                HTMLCanvasElement,
                self.shadowRootElement.getElementById("diver-canvas"),
            )
            if self.canvas is None:
                print("Existing canvas not found, attempting to create new one")
                self.canvas = cast(HTMLCanvasElement, document.createElement("canvas"))
                self.canvas.id = "diver-canvas"

                diverContainer = self.shadowRootElement.getElementById(
                    "diver-canvas-container"
                )
                if diverContainer is not None:
                    diverContainer.appendChild(self.canvas)
                else:
                    print(
                        "Could not find div to append canvs to.",
                        "There should be a div with 'python-canvas-container' id",
                    )
            self.ctx = cast(CanvasRenderingContext2D, self.canvas.getContext("2d"))
        else:  # external canvs (p5js)
            print(canvas)
            self.canvas = cast(HTMLCanvasElement, canvas)
            print(self.canvas)

        self.last_frame_id = 0
        self.last_frame_time = 0
        self.start_time = 0
        self.resetTime = resetTime
        self.frame_count = 0
        self.start()

    # animation info

    def start(self):
        # make sure if we have already started a loop, that it gets stopped
        self.cancelAnimationLoop()
        # a proxy is necessary to pass a python function to js
        # this starts the animation (and keeps track of the current frame)

        self.last_frame_id = window.requestAnimationFrame(self.animate_loop_proxy)

    def animate_loop(self, frame_time_mili):
        if self.start_time == 0:
            self.start_time = frame_time_mili
        else:
            # TODO [style] better way of handling div by zero? #5
            if frame_time_mili != self.last_frame_time:
                self.frame_rate = 1000 / (frame_time_mili - self.last_frame_time)
                if self.frame_count % 10 == 0:
                    ...
                    # print(self.frame_rate)
        self.last_frame_time = frame_time_mili
        if self.resetTime:
            total_time = self.last_frame_time - self.start_time
        else:
            total_time = self.last_frame_time
        self.frame_count += 1
        try:
            self.animate_func(self, total_time)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            last_call = tb[-1]  # Get the last call information
            msg = (
                "Error on line {}, in function {}".format(
                    last_call.lineno, last_call.name
                )
                + "\n"
                + str(e)
            )
            # TODO [feat] return structured exception data? #4
            self.rootElement.pythonErrorHandler(msg)  # pyright: ignore
            return  # don't call next animation frame so the loop stops

        self.last_frame_id = window.requestAnimationFrame(self.animate_loop_proxy)

    def cancelAnimationLoop(self):
        window.cancelAnimationFrame(self.last_frame_id)

    def clear_screen(self, image: Image, c: Color) -> None:
        for y in range(image.height):
            for x in range(image.width):
                image.pixels[y][x] = (c.r, c.g, c.b, 255)

    def create_image(self, width: int, height: int, bc: Color) -> Image:
        return Image(
            width,
            height,
            # [[Color(0,0,0) for _ in range(width)] for _ in range(height)],
            [[(bc.r, bc.g, bc.b, 255) for _ in range(width)] for _ in range(height)],
        )

    def draw_image(self, image: Image, scale_factor: int):
        canvas = self.canvas
        numpy_image = np.array(image.pixels, dtype=np.uint8)
        scaled_image = np.repeat(numpy_image, scale_factor, axis=0)
        scaled_image = np.repeat(scaled_image, scale_factor, axis=1)

        h, w, d = scaled_image.shape

        # update this in case it has changed
        self.canvas.width = w
        self.canvas.height = h
        scaled_image = np.ravel(
            np.uint8(np.reshape(scaled_image, (h * w * d, -1)))
        ).tobytes()

        pixels_proxy = create_proxy(scaled_image)
        pixels_buf = pixels_proxy.getBuffer("u8clamped")  # pyright: ignore
        img_data = ImageData.new(pixels_buf.data, w, h)

        self.ctx.putImageData(img_data, 0, 0)
        self.ctx.drawImage(canvas, 0, 0)

        pixels_proxy.destroy()
        pixels_buf.release()
        return "Created Image", w, h


currentCanvasManager: None | CanvasManager = None
