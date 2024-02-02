// @ts-check
import { PyodideManager } from "./pyodideManager.js"

export default class DiverVisual extends HTMLElement {

  /** @type {PyodideManager | null} */
  #pyodideManager = null

  constructor() {
    super()
    /** @type {string} */
    this.sketchFileName = this.getAttribute("sketch") ?? "sketches/impossible_object.py"
    /** @type {string} */
    this.diverSrcFileName = this.getAttribute("diverSrc") ?? "diver.py"
    console.log("[DiverVisual] Constructed webcomponent DiverVisual, id: " + this.id)
  }

  async connectedCallback() {
    // error schecking
    if (!this.id) {
      console.warn("[DiverVisual] No ID set on diver-visual component. \
        Setting default ID. If multiple diver-visual \
        components are created, you must specify a unique ID for each.\
        ")
      //warn the first time, then throw errors if multiple are added
      this.id = "defaultDiverRootID"
    }

    if (document.querySelectorAll('#' + this.id).length > 1) {
      console.error("[DiverVisual] There are multiple diver-visual elements with the same id. \
                    This will break things! Use unique ID attributes for each element")
    }

    if (!this.sketchFileName) {
      throw Error("[DiverVisual] No sketch file available, pass as a `sketch` attribute in HTML, or set this.dynamicFileName before DOM load")
    }
    //Add HTML elements
    let shadowRoot = this.attachShadow({ mode: "open" })
    shadowRoot.innerHTML = this.#getTemplate()

    //load all external resources
    this.#startLoadingIndicator()
    console.log(`[DiverVisual] starting processing diver. id:${this.id}, sketch:${this.sketchFileName}`)

    await this.#loadExternalResource(this.sketchFileName, this.diverSrcFileName)

    this.#stopLoadingIndicator()
  }
  #getTemplate() {
    // HTML 
    return `
    <style>
    #loader #spinner {
      border: 4px solid var(--text-color,#555);
      border-top: 4px solid var(--panel-color,#555);
      border-radius: 50%;
      width: 80px;
      height: 80px;
      margin: 20px;
      animation: spin 2s linear infinite;
    }
    #loader span{
      marin: auto;
    }

    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }

      100% {
        transform: rotate(360deg);
      }
    }
    </style>
    <div id="diver-canvas-container"></div>
    <div id="loader">
      <div id="spinner"></div>
      <span>Loading Python...</span>
    </div>
    `
  }

  /**
   * Attempts to reload the sketch file specified at 
   * `this.sketchFileName` and Runs the reloaded sketch.
   * Requires DiverVisual to be fully initialized
   */
  async reloadSketchAndRun() {
    if (!this.sketchFileName) {
      throw Error("[DiverVisual] no sketch file provided, can't reload")
    }
    const sketchSrcString = await this.#loadSketch(this.sketchFileName)
    if (sketchSrcString) {
      this.runSketchString(sketchSrcString)
    } else {
      throw Error("[DiverVisual] Failed to load sketch")
    }
  }

  /** Runs given sketch source string
   * Requires DiverVisual to be fully initialized
     * @param {string} sketchSrcString - Python source code string
     */
  runSketchString(sketchSrcString) {
    if (!this.#pyodideManager) {
      throw Error("[DiverVisual] Pyodide manager not setup. Called reload too early, or something has gone horribly wrong")
    }
    this.#runSketch(this.#pyodideManager, sketchSrcString)
  }

  /** Loads all the resources that are needed
   * @param {string} sketchFileName
   * @param {string} diverSrcFileName
   */
  async #loadExternalResource(sketchFileName, diverSrcFileName) {
    try {
      const [sketchSrcString, diverLibString, pyodideManager] = await Promise.all([
        this.#loadSketch(sketchFileName),
        this.#loadDiverSrc(diverSrcFileName),
        PyodideManager.createPyodideInstance()
      ])
      //install intial python dependencies
      pyodideManager.installDiver(diverLibString, this.id)
      console.log("[DiverVisual] loaded diver")

      //run the initial code example for the first time
      this.#runSketch(pyodideManager, sketchSrcString)
      // save pyodideManager for future runs
      this.#pyodideManager = pyodideManager
    } catch (error) {
      console.log("[DiverVisual] " + error)
      this.innerText = "[DiverVisual] An error occured: " + error.toString()
      console.error(this.innerText)
    }

  }

  /** Runs the provided python sketch string using the provided pyodideManager
   * @param {PyodideManager} pyodideManager
   * @param {string} sketchSrcString - python sketch string
   */
  #runSketch(pyodideManager, sketchSrcString) {
    try {
      console.log("[DiverVisual] Running sketch..")
      let output = pyodideManager.runPython(sketchSrcString)
      console.log("[DiverVisual] Sketch load succeded! Output (if any):" + output)
      //notify upstream of sketch contents
      this.dispatchEvent(new CustomEvent('sketchRan', {
        detail: output
      }))
    } catch (err) {
      this.dispatchEvent(new CustomEvent('pythonError', {
        detail: err.toString()
      }))
    }
  }
  /**
     * @param {string} err
     */
  pythonErrorHandler(err) {
    console.log("Python error", err)
    this.dispatchEvent(new CustomEvent('pythonError', {
      detail: err
    }))
  }

  #startLoadingIndicator() {
    //@ts-ignore low priority
    this.shadowRoot.querySelector('#loader').style.display = 'block'
  }
  #stopLoadingIndicator() {
    //@ts-ignore low priority
    this.shadowRoot.querySelector('#loader').style.display = 'none'
  }

  /**
     * @param {string} diverSrcFileName
     * @returns {Promise<string>}
     */
  async #loadDiverSrc(diverSrcFileName) {
    try {
      const response = await fetch(diverSrcFileName)
      if (!response.ok) {
        throw new Error('[DiverVisual] Http error, status= ' + response.status)
      }
      return response.text()
    }
    catch (e) {
      throw new Error("[DiverVisual] Could not load diver library: " + diverSrcFileName + " error: " + e)
    }
  }

  /**
     * @param {string} sketchFileName
     * @returns {Promise<string>}
     */
  async #loadSketch(sketchFileName) {
    console.log("[DiverVisual] attempting to load " + sketchFileName)
    try {
      let response = await fetch(sketchFileName)
      if (!response.ok) {
        throw new Error('[DiverVisual] Http error, status= ' + response.status)
      }

      //await this so we can dispatch the following event now
      let sketchSrcString = await response.text()

      //notify upstream of sketch contents
      this.dispatchEvent(new CustomEvent('sketchLoaded', {
        detail: sketchSrcString
      }))
      console.log("[DiverVisual] successfully loaded " + sketchFileName)
      return sketchSrcString
    }
    catch (e) {
      throw new Error("[DiverVisual] Could not load sketch: " + sketchFileName + " error: " + e)
    }
  }
}

customElements.define("diver-visual", DiverVisual)
