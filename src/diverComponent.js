// @ts-check
import { PyodideManager } from "./pyodideManager.js";

export default class DiverVisual extends HTMLElement {

  constructor() {
    super();
    /** @type {PyodideManager | null} */
    this.pyodideManager = null
    /** @type {string | null} */
    this.diverLibString = null
    /** @type {string | null} */
    this.sketchSrcString = null
    /** @type {string | null} */
    this.sketchFileName = "/sketches/default.py"
    /** @type {string |  null} */
    this.dynamicFileName = null
    /** @type {string} */
    this.diverSrcFileName = "diver.py"
    console.log("construct web component diver")
  }

  async connectedCallback() {
    //Process attributes
    this.diverSrcFileName = this.getAttribute("diverSrc") ?? this.diverSrcFileName
    this.sketchFileName = this.getAttribute("sketch") ?? this.sketchFileName
    this.sketchFileName = this.dynamicFileName ?? this.sketchFileName;
    if (!this.hasAttribute("id")) {
      //set a default ID, 
      //TODO warn of duplicate IDs
      this.setAttribute("id", "defaultDiverRootID")
    }
    if (!this.sketchFileName) {
      throw Error("No sketch file available, pass as a `sketch` attribute in HTML, or set this.dynamicFileName before DOM load")
    }
    this.loadSketch(this.sketchFileName)
    this.loadDiverSrc()
    this.diverRootId = this.getAttribute("id");

    console.log(`starting processing diver. id:${this.diverRootId}, sketch:${this.sketchFileName}`)
    //Add HTML elements
    const diverCanvasContainer = document.createElement("div")
    diverCanvasContainer.setAttribute("id", "diver-canvas-container")

    let shadowRoot = this.attachShadow({ mode: "open" });
    shadowRoot.appendChild(diverCanvasContainer);
    shadowRoot.appendChild(this.constructLoadingIndicator());

    //load resources
    this.startLoadingIndicator();


    console.log("Loading pyodide")
    this.pyodideManager = await PyodideManager.createPyodideInstance()

    console.log("loaded pyodide")

    await this.pyodideManager.installDiver(this.diverLibString, this.diverRootId)
    console.log("loaded diver")

    this.stopLoadingIndicator();

    //run the initial code example for the first time
    await this.runSketch(this.pyodideManager)
  }

  /**
     * @param {PyodideManager} pyodideManager
     */
  async runSketch(pyodideManager) {
    try {
      console.log("Running sketch..")
      let output = await pyodideManager.runPython(this.sketchSrcString)
      console.log("Sketch load succeded! Output (if any):" + output)
      return output
    } catch (err) {
      console.log("Current Sketch Failed. Output(if any):" + err);
      return err
    }
  }
  async reloadSketch() {
    if (!this.sketchFileName) {
      throw Error("no sketch file provided, can't reload")
    }
    await this.loadSketch(this.sketchFileName);
    if (!this.pyodideManager) {
      throw Error("Pyodide manager not setup. Called reload too early, or something has gone horribly wrong")
    }
    await this.runSketch(this.pyodideManager)
  }

  constructLoadingIndicator() {
    const loaderDiv = document.createElement("div")
    loaderDiv.setAttribute("id", "loader")
    loaderDiv.appendChild(document.createElement("div")).setAttribute("id", "spinner")
    const loadText = document.createElement("span")
    loadText.textContent = "Loading Python..."
    loaderDiv.appendChild(loadText)
    return loaderDiv
  }
  startLoadingIndicator() {
    //@ts-ignore low priority
    this.shadowRoot.querySelector('#loader').style.display = 'block'
  }
  stopLoadingIndicator() {
    //@ts-ignore low priority
    this.shadowRoot.querySelector('#loader').style.display = 'none'
  }

  async loadDiverSrc() {
    await fetch(this.diverSrcFileName)
      .then(response => response.text())
      .then(text => this.diverLibString = text)
      .catch(error => console.error('Error fetching the file:', error))
  }

  /**
     * @param {string} sketchFileName
     */
  async loadSketch(sketchFileName) {
    console.log("attempting to load " + sketchFileName)
    await fetch(sketchFileName)
      .then(response => response.text())
      .then(text => this.sketchSrcString = text)
      .catch(error => console.error('Error fetching the file:', error))
    //notify upstream of sketch contents
    this.dispatchEvent(new CustomEvent('sketchLoaded', {
      detail: this.sketchSrcString
    }))
  }
}

customElements.define("diver-visual", DiverVisual);
