# https://pyodide.org/en/stable/usage/loading-custom-python-code.html#from-python
# Downloading a single file
await pyodide.runPythonAsync('
    from pyodide.http import pyfetch
    response = await pyfetch("https://.../script.py")
    with open("script.py", "wb") as f:
        f.write(await response.bytes())
')
pkg = pyodide.pyimport("script");
pkg.do_something();
