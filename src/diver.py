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
