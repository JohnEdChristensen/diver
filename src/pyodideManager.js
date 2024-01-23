"use strict";
export class PyodideManager {

  constructor(pyodide) {
    this.pyodide = pyodide
  }

  static async createPyodideInstance() {
    let initPyodide = await loadPyodide()
    //initPyodide.setStdOut()

    await initPyodide.loadPackage("numpy");//TODO remove numpy dependancy, figure out dynamic imports
    // await pyodide.loadPackage("micropip");//install mircopip to install other packages
    // const micropip = pyodide.pyimport("micropip");
    // await micropip.install("numpy");
    // install diver
    return new PyodideManager(initPyodide)
  }
  async installDiver(diverLibString) {
    let install_diver_py =
      `
# https://pyodide.org/en/stable/usage/loading-custom-python-code.html#from-python
# Downloading a single file
import importlib
from pathlib import Path

Path("diver.py").write_text("""
`
      + diverLibString +// TODO change this, """ can't be used in diver.py this way...
      `
"""
)
importlib.invalidate_caches() # Make sure Python notices the new .py file
`
    try {

      console.log("Loading Diver")
      //console.log(install_diver_py)
      let output = this.pyodide.runPython(install_diver_py);
      console.log("Installed diver. Output (if any):", output)
    } catch (err) {
      console.log("Error installing diver")
      console.log(install_diver_py)
      console.log(err)
    }

  }

  async runPython(pythonCode) {
    //this should work to dynamically install packages, but it isn't... I'll manually install for now.
    // await pyodide.loadPackagesFromImports(pyCode,{messageCallback : (m)=>{console.log(m)}})
    return await this.pyodide.runPythonAsync(pythonCode)
  }
}
