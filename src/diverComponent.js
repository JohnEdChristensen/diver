import { PyodideManager } from "./pyodideManager.js";

export class DiverVisual extends HTMLElement {

  constructor() {
    super();
    this.pyodideManager = null
    this.diverLibString = null
    this.sketchString = null
    console.log("construct web component diver")
  }

  async connectedCallback() {
    //Process attributes
    if (!this.hasAttribute("sketch")) {
      //set a default sketch
      this.setAttribute("sketch", "/sketches/default.py")
    }
    if (!this.hasAttribute("id")) {
      //set a default ID, 
      //TODO warn of duplicate IDs
      this.setAttribute("id", "defaultDiverRootID")
    }
    this.sketchFileName = this.URLFile ?? this.getAttribute("sketch");
    this.diverRootId = this.getAttribute("id");

    console.log(`starting processing diver. id:${this.diverRootId}, sketch:${this.sketchFileName}`)
    //Add HTML elements
    const diverCanvasContainer = document.createElement("div")
    diverCanvasContainer.setAttribute("id", "diver-canvas-container")

    this.attachShadow({ mode: "open" });
    this.shadowRoot.appendChild(diverCanvasContainer);
    this.shadowRoot.appendChild(this.constructLoadingIndicator());
    
    //load resources
    this.startLoadingIndicator();

    this.loadDiver()
    this.loadSketch()

    console.log("Loading pyodide")
    this.pyodideManager = await PyodideManager.createPyodideInstance()

    console.log("loaded pyodide")

    await this.pyodideManager.installDiver(this.diverLibString, this.diverRootId)
    console.log("loaded diver")

    this.stopLoadingIndicator();

    //run the initial code example for the first time
    await this.runSketch()
  }

  async runSketch() {
    try {
      console.log("Running sketch..")
      let output = await this.pyodideManager.runPython(this.sketchString)
      console.log("Sketch load succeded! Output (if any):" + output)
      return output
    } catch (err) {
      console.log("Current Sketch Failed. Output(if any):" + err);
      return err
    }
  }
  async reloadSketch(){
    await this.loadSketch();
    await this.runSketch()
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
    this.shadowRoot.querySelector('#loader').style.display = 'block'
  }
  stopLoadingIndicator() {
    this.shadowRoot.querySelector('#loader').style.display = 'none'
  }

  async loadDiver() {
    await fetch('/diver.py')
      .then(response => response.text())
      .then(text => this.diverLibString = text)
      .catch(error => console.error('Error fetching the file:', error))
  }

  async loadSketch() {
    console.log("attempting to load " +  this.sketchFileName)
    await fetch(this.sketchFileName)
      .then(response => response.text())
      .then(text => this.sketchString = text)
      .catch(error => console.error('Error fetching the file:', error))
    //notify upstream of sketch contents
    this.dispatchEvent(new CustomEvent('sketchLoaded',{
      detail: this.sketchString
    }))
  }
}

customElements.define("diver-visual", DiverVisual);
