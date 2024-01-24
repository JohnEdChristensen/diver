# Diver
**Work in progress :)**

## Examples

Live Examples:
- https://johnedchristensen.github.io/diver/src/?filename=/sketches/rainbow.py
- https://johnedchristensen.github.io/diver/src/?filename=/sketches/e_field.py
- https://johnedchristensen.github.io/diver/src/?filename=/sketches/squares.py
### Interactive
- https://johnedchristensen.github.io/diver/src/?filename=/sketches/string.py
## About
A simple python package that makes it easy to share interactive visuals on the web.
Uses Pyodide to run python directly in the browser, meaning code can be shared with others without any need to download/install/configure python. 

It also can be served from a static website server, meaning it is simple to embed visuals on personal websites/blogs.

## Features
- [x] Render static images to a canvas element
- [x] live reloading development server
- [x] Render animated canvas/WebGL
- [ ] pythonic drawing API (with beginner/user friendly documentation/examples)
- [x] Write code in browser
- [-] in browser LSP features like inline docs, autocomplete, linting, type checking
- [ ] Human friendly documentation (with live running/editable examples of course)
- [ ] Share feature. Generate link to custom sketches
- [ ] Embedding mode, for embedding in blog posts, etc.
- [ ]? Collaborative editing/ 1 way live sharing 
    - Only planning to do this if it doesn't require hosting a server. Currently looking into yjs + CodeMirror

## Usage
The current state of the library is in very active development. Expect breaking changes.
### Pixel level drawing
[This example (rainbow.py)](https://johnedchristensen.github.io/diver/src/?filename=rainbow.py) shows some basic usage. It specifies each pixel on the canvas, so you can draw anything you want directly this way. It isn't very performant this way, so the resolution needs to be pretty low to run smoothly.

### 2D Canvas API

[This example (squares.py)](https://johnedchristensen.github.io/diver/src/?filename=squares.py) draws to canvas using the JavaScript canvas API. This is much more performant, and can run at higher resolutions/frame rates. To use this mode you'll need to know (or learn) how to use the [canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

### Best of both worlds (for me)

A more user friendly API is planned that will have better documentation integration to make it easier to find what functions are available straight from the editor.


## Limitations

While many popular python packages run great in the browser, not all packages can. See https://Pyodide.org/en/stable/usage/packages-in-Pyodide.html for a list of packages that will work out of the box.

## Development
- [ ] Add details on how to get up and running
