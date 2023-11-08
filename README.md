# Development Environemnts
I've had trouble getting my linter/typecheckers to behave with pyodide assumed modules like `js`

There's a packager that says it solved this, but It's not working out for me...

I resorted to adding the `js.py` and `js.pyi` to the main directory because I don't know how else to get it recognized by my typechecker and linter...

Hopefully I can find a better way!
