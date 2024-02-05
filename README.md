# Diver
**Work in progress :)**

## Examples

### Interactive

Examples:
- [Using processo](https://johnedchristensen.github.io/diver/?filename=examples/processo_figure_8.py)
- [Impossible Triangle](https://johnedchristensen.github.io/diver/?filename=examples/impossible_object.py)
- [Rainbow Wave](https://johnedchristensen.github.io/diver/?filename=examples/rainbow.py)
- [Swirling Squares](https://johnedchristensen.github.io/diver/?filename=examples/squares.py)
- [Simulated String](https://johnedchristensen.github.io/diver/src/?filename=sketches/string.py)
## About
A python package that aimes to make it easy to share interactive visuals online.

Uses Pyodide to run python directly in the browser, meaning code can be shared with others without any need to download/install/configure python. 

It also can be served from a static website server, meaning it is simple to embed visuals on personal websites/blogs.

## Features
- [x] Render static images to a canvas element
- [x] live reloading development server
- [x] Render animated canvas/WebGL
- [x] pythonic drawing API (with beginner/user friendly documentation/examples)
    - [x] [processo](https://github.com/nickmcintyre/proceso) offers a great python binding for p5js. It is now installed by default.
    - Examples: https://proceso.cc/examples/creative_coding/simple_shapes
- [x] Write code in browser
- [-] in browser LSP features like inline docs, autocomplete, linting, type checking
- [ ] Human friendly documentation (with live running/editable examples of course)
- [ ] Share feature. Generate link to custom sketches
- [ ] Embedding mode, for embedding in blog posts, etc.
- [ ]? Collaborative editing/ 1 way live sharing 
    - Only planning to do this if it doesn't require hosting a server. Currently looking into yjs + CodeMirror

## Usage
The current state of the library is in very active development. Expect breaking changes.


## Basics
Use "Show Code" button to view/edit the code yourself!
After making changes click "Run" or use Ctrl-Enter to run your code.

[Get started](https://johnedchristensen.github.io/diver/?filename=examples/processo_simple_shapes.py) with a drawing example using p5js (via processo).
### p5.js
> p5.js is a JavaScript library for creative coding, with a focus on making coding accessible and inclusive for artists, designers, educators, beginners, and anyone else! p5.js is free and open-source because we believe software, and the tools to learn it, should be accessible to everyone.vascript library
https://p5js.org/

p5.js is a great project, but is limited to using javascipt. Using Pyodide, python code can now run alongisde javascript code in your browser, and use all the functionality that p5.js offers. An additional library needs to handle translations between p5.js and python, and processo does just that!
### processo
The [processo](https://github.com/nickmcintyre/proceso) lets you use [p5js](https://p5js.org/) from python.
#### Example
[Try it out](https://johnedchristensen.github.io/diver/?filename=examples/processo_simple_shapes.py)
```python
from proceso import Sketch


p5 = Sketch()
p5.describe("A rectangle, circle, triangle, and flower drawn in pink on a gray background.")

# Create the canvas
p5.create_canvas(720, 400)
p5.background(200)

# Set colors
p5.fill(204, 101, 192, 127)
p5.stroke(127, 63, 120)

# A rectangle
p5.rect(40, 120, 120, 40)
# A circle
p5.circle(240, 240, 80)
# A triangle
p5.triangle(300, 100, 320, 100, 310, 80)

# A design for a simple flower
p5.translate(580, 200)
p5.no_stroke()
for _ in range(10):
    p5.ellipse(0, 30, 20, 80)
    p5.rotate(p5.PI / 5)
```
From processo documentation: 
Checkout more processo examples: https://proceso.cc/examples/creative_coding/

### Lower level APIs
These methods are a bit more complex, but can be useful if you want to work more directly with your visuals.
#### Pixel level drawing
[This example (rainbow.py)](https://johnedchristensen.github.io/diver/src/?filename=rainbow.py) shows some basic usage. It specifies each pixel on the canvas, so you can draw anything you want directly this way. It isn't very performant this way, so the resolution needs to be pretty low to run smoothly.


#### 2D Canvas API

[This example (squares.py)](https://johnedchristensen.github.io/diver/src/?filename=squares.py) draws to canvas using the JavaScript canvas API. This is much more performant than drawing pixel by pixel, and can run at higher resolutions/frame rates. To use this mode you'll need to know (or learn) how to use the [canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)


## Limitations

While many popular python packages run great in the browser, not all packages can. See https://Pyodide.org/en/stable/usage/packages-in-Pyodide.html for a list of packages that will work out of the box.

## Development
- [ ] Add details on how to get up and running
