//@ts-check
import "https://cdn.jsdelivr.net/pyodide/v0.23.2/full/pyodide.js"
//import { loadPyodide } from "pyodide";
export class PyodideManager {

  /** Don't use the default constructor to initalize this class. 
   * Use PyodideManager.createPyodideInstance
   * @param {import("pyodide").PyodideInterface} pyodide
   */
  constructor(pyodide) {
    this.pyodide = pyodide
  }
  /**Initialize a pyodide instance*/
  static async createPyodideInstance() {
    console.log("[PyodideManager] Start Creating Pyodide Instance")
    // @ts-ignore Not sure why, but can't import pyodide
    let initPyodide = await loadPyodide()
    //initPyodide.setStdOut()

    console.log("[PyodideManager] Pyodide loaded, installing modules")
    await initPyodide.loadPackage(["typing-extensions", "numpy", "dist/proceso-0.0.14-py3-none-any.whl"]);//TODO remove numpy dependancy, figure out dynamic imports #5
    //TODO remove numpy dependancy, figure out dynamic imports #5
    // await pyodide.loadPackage("micropip");//install mircopip to install other packages
    // const micropip = pyodide.pyimport("micropip");
    // await micropip.install("numpy");
    // install diver
    console.log("[PyodideManager] Pyodide instace created")
    return new PyodideManager(initPyodide)
  }

  /**
     * @param {string} diverLibString
     * @param {string} diverRootId
     */
  installDiver(diverLibString, diverRootId) {
    //pass javascript root ID of diver element
    diverLibString = `diverRootId = "${diverRootId}"\n` + diverLibString
    // Replace single backslash (\) with double backslashes (\\)
    diverLibString = diverLibString.replace(/\\/g, '\\\\');

    // Replace newline characters (\n) with their escaped version (\\n)
    diverLibString = diverLibString.replace(/\n/g, '\\n').replace(/"/g, '\\"')
    let install_diver_py =
      `
# https://pyodide.org/en/stable/usage/loading-custom-python-code.html#from-python
# Downloading a single file
import importlib
from pathlib import Path

Path("diver.py").write_text("""${diverLibString}""")
importlib.invalidate_caches() # Make sure Python notices the new .py file
`
    try {
      console.log("[PyodideManager] Loading Diver")
      //console.log(install_diver_py)
      //let output = this.pyodide.runPython(install_diver_py);
      //
      let output = this.pyodide.runPython(install_diver_py)
      console.log("[PyodideManager] Installed diver. Output (if any):", output)
    } catch (err) {
      console.log("[PyodideManager] Error installing diver")
      console.log(install_diver_py)
      console.log(err)
      throw err
    }
  }

  /**
     * @param {string} pythonCode
     */
  runPython(pythonCode) {
    console.log("[PyodideManager] Running Python Using Pyodide")
    // this should work to dynamically install packages, but it isn't... I'll manually install for now.
    // TODO [feat] support dynamic package loading #5
    // await pyodide.loadPackagesFromImports(pyCode,{messageCallback : (m)=>{console.log(m)}})
    try {
      //this try will not catch errors that happen in the js event loop of animation. 
      //It will only catch errors that happen during sketch definition.
      //TODO [style] unify error handling from CanvasManager and sketch
      let output = this.pyodide.runPython(pythonCode)
      console.log("[PyodideManager] Pyodide Ran Python. Output(if any): " + output)
      return
    } catch (e) {
      // replace error message
      console.log("[PyodideManager] Python code failed: " + e)
      //diverComponent.pythonErrorHandler(e)
      throw e;
    }
  }
}
