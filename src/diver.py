from dataclasses import dataclass
from typing import List, cast, Tuple

import numpy as np
from js import (
    CanvasRenderingContext2D,
    HTMLCanvasElement,
    ImageData,
    document,
    window,
)
from pyodide.ffi import create_proxy

currentCanvasManager = None


@dataclass
class Color:
    r: int
    g: int
    b: int


@dataclass
class Image:
    width: int
    height: int
    pixels: List[List[Tuple[int, int, int, int]]]


class CanvasManager:
    def __init__(self, animate_func):
        global currentCanvasManager
        # currently only supports one loop
        if currentCanvasManager is not None:
            currentCanvasManager.cancelAnimationLoop()
        currentCanvasManager = self
        print("hello from CanvasManager, ('diver.py')")
        self.animate_func = animate_func
        self.animate_loop_proxy = create_proxy(self.animate_loop)
        self.canvas = cast(HTMLCanvasElement, document.getElementById("myCanv"))
        if self.canvas is None:
            print("Existing canvas not found, attempting to create new one")
            self.canvas = cast(HTMLCanvasElement, document.createElement("canvas"))
            self.canvas.id = "myCanv"  # TODO clean up names to disambiguate

            pyCanv = document.getElementById("python-canvas-container")
            if pyCanv is not None:
                pyCanv.appendChild(self.canvas)
            else:
                print(
                    "Could not find div to append canvs to.",
                    "There should be a div with 'python-canvas-container' id",
                )

        self.ctx = cast(CanvasRenderingContext2D, self.canvas.getContext("2d"))
        self.last_frame_id = 0
        self.last_frame_time = 0
        self.start_time = 0
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
            self.frame_rate = 1000 / (frame_time_mili - self.last_frame_time)
            if self.frame_count % 100 == 0:
                print(self.frame_rate)
        self.last_frame_time = frame_time_mili
        self.frame_count += 1

        self.animate_func(self, frame_time_mili)
        self.last_frame_id = window.requestAnimationFrame(self.animate_loop_proxy)

    def cancelAnimationLoop(self):
        window.cancelAnimationFrame(self.last_frame_id)

    def clear_screen(self, image: Image, c: Color) -> None:
        for y in range(image.height):
            for x in range(image.width):
                image.pixels[y][x] = (c.r, c.g, c.b, 255)

    def draw_pixel(self, image: Image, x: int, y: int, c: Color) -> None:
        if 0 <= x < image.width and 0 <= y < image.height:
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

        # update this incase it has changed
        self.canvas.width = w
        self.canvas.height = h
        scaled_image = np.ravel(
            np.uint8(np.reshape(scaled_image, (h * w * d, -1)))
        ).tobytes()

        pixels_proxy = create_proxy(scaled_image)
        pixels_buf = pixels_proxy.getBuffer("u8clamped")
        img_data = ImageData.new(pixels_buf.data, w, h)

        self.ctx.putImageData(img_data, 0, 0)
        self.ctx.drawImage(canvas, 0, 0)

        pixels_proxy.destroy()
        pixels_buf.release()
        return "Created Image", w, h


# Example usage
# background_color = Color(1, 128, 128)
# img = create_image(100, 100, background_color)
# Clear the screen with the background color
# clear_screen(img, background_color)
# draw_pixel(img, 10, 10, Color(255, 0, 0))  # Draw a red pixel at (10, 10)
#
#
# draw_image(img)
