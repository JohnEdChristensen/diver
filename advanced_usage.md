## Advanced Usage

### Lower level APIs
These methods are a bit more complex, but can be useful if you want to work more directly with your visuals.
#### Pixel level drawing
[This example (rainbow.py)](https://johnedchristensen.github.io/diver/?filename=examples/rainbow.py) shows some basic usage. It specifies each pixel on the canvas, so you can draw anything you want directly this way. It isn't very performant this way, so the resolution needs to be pretty low to run smoothly.


#### 2D Canvas API

[This example (squares.py)](https://johnedchristensen.github.io/diver/?filename=exampels/squares.py) draws to canvas using the JavaScript canvas API. This is much more performant than drawing pixel by pixel, and can run at higher resolutions/frame rates. To use this mode you'll need to know (or learn) how to use the [canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)



### Use your own editor


TODO: make this process easier by putting the package on pypi. Let me know if there if you would like this to be easier


You can run diver from your own computer and use whatever editor you would like!
To start a local server, clone this repository,
```
git clone https://github.com/JohnEdChristensen/diver.git
```
enter the repo directory and install Diver using Poetry
```
cd diver
poetry install
```

Now you can serve any python file to run in the browser using `diver_serve`
```
poetry run diver_serve ./examples/squares.py
```
When the file you are serving is edited, the web interface will reload the file automatically!

### Limitations

While many popular python packages run great in the browser, not all packages can. See https://Pyodide.org/en/stable/usage/packages-in-Pyodide.html for a list of packages that will work out of the box.



### Development
Want to run the site locally?
1. Use the local server mentioned in the offline section above. It will live reload the site when source files are changed.
2. Everything except for the code editor `src/editor/` runs without any build step, so it should just work by using `diver_serve`, or any basic web-server from the root directory.
i.e. `python -m http.server


Run specific sketch files either by using `diver_serve` or by setting the `filename` url parameter to python file relative to the root repo directory.
```
0.0.0.0:8000?filename=examples/squares.py
```


### Offline (not well tested)
in progress:
- After diver is loaded, there is no longer any need to remain online. As long as your browser caches everything it should be possible
- let me know if there is interest in this! It should be pretty simple to package an offline application using something like Tauri, or make the site a PWA

### Roadmap
- [x] Run python code with no installation/setup
- [x] Write code in browser
- [x] Easily share code via a link
- [x] Auto reloading to optionally edit files locally with any editor
- [x] Render animated canvas
    - [x] [proceso](https://github.com/nickmcintyre/proceso) offers a great python binding for p5js. It is now installed by default.
    - Examples: https://proceso.cc/examples/creative_coding/simple_shapes
- [ ] in browser LSP features like inline docs, autocomplete, linting, type checking
- [ ] Human friendly documentation (with live running/editable examples of course)
- [/] Embedding mode, for embedding in blog posts, etc.
    - It should be possibly to use Diver as webcomponent in your own site, I haven't tested this well yet though 
- [?] Collaborative editing/ 1 way live sharing 
    - Only planning to do this if it doesn't require hosting a server. Currently looking into yjs + CodeMirror
