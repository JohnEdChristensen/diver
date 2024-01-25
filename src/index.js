// catch errors before you run, setup your IDE to use tsserver:
// @ts-check
// read more: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
"use strict"
import { DiverEditor } from './editor/editor.js'
import { DiverVisual } from './diverComponent.js'
import { getElementOrError } from './utils.js'

const diverEditor = new DiverEditor("")
const outputPanelContent =  getElementOrError("output-content")
//const outputPanelContent = document.getElementById("output-content")
outputPanelContent.textContent = "Initializing...\n"

/** @type {DiverVisual} */
const diverVisual  = getElementOrError("diverID") 
diverVisual.addEventListener('sketchLoaded',e=>diverEditor.setText(e.detail))

let sketchFileName = getFileFromURL()
// load python code 
if (sketchFileName) {
  diverVisual.URLFile = sketchFileName
}

console.log(diverVisual.sketchString)
// setup code that needs DOM elements
document.addEventListener('DOMContentLoaded', function() {
  // initial panel setup
  panelToggleSetup()
})

function panelToggleSetup() {
  //main buttons
  const runButton = document.getElementById('run-button')
  runButton.addEventListener('click', () => {
    diverVisual.sketchString = diverEditor.getText()
    diverVisual.runSketch()
  })

  // Utility function to toggle elements and button text
  const toggleElement = (button, element, className, textContent) => {
    element.classList.toggle(className);
    button.textContent = element.classList.contains(className) ? `Show ${textContent}` : `Hide ${textContent}`;
  };

  // Access DOM elements
  const toggleCodeButton = document.getElementById('toggle-code-button');
  const collapsibleCode = document.getElementById('collapsible-code');
  const codeContainer = document.getElementById("code-container");

  const toggleOutputButton = document.getElementById('toggle-output-button');
  const collapsibleOutput = document.getElementById('collapsible-output');

  // Event listeners
  toggleCodeButton.addEventListener('click', () => {
    toggleElement(toggleCodeButton, collapsibleCode, 'collapse', 'Code');
    codeContainer.style.visibility = collapsibleCode.classList.contains('collapse') ? "hidden" : "visible";
  });

  toggleOutputButton.addEventListener('click', () => {
    toggleElement(toggleOutputButton, collapsibleOutput, 'collapse', 'Output');
  });

}

async function reloadDiver() {
  addToOutput("Diver src changed, reloading...", false)
  window.location.reload()
  //previously used the following, but ran into multiple python instances running
  //only effects dev server workflow, so not critical to fix
  //
  // just reload diver module
  // await loadDiver()//make sure file is loaded before continuing!
  // pyodide.setInterruptBuffer
  // main()
}
globalThis.reloadDiver = reloadDiver // expose to global scope for dev server

async function reloadSketch() {
  diverVisual.reloadSketch()
}
globalThis.reloadSketch = reloadSketch // expose to global scope for dev server


function getFileFromURL() {
  const currentUrl = window.location.href
  const url = new URL(currentUrl)
  const params = new URLSearchParams(url.search)

  //example URL "https://domain.com/page?filename=myfile.txt"
  const fileName = params.get('filename') // This would be 'myfile.txt'
  return fileName
}

function addToOutput(s, showCode) {
  if (showCode) {
    outputPanelContent.textContent += ">>>" + diverEditor.getText() + "\n"
  }
  console.log(s)
  if (s != undefined) {
    outputPanelContent.textContent += s + "\n"
  }
  const scroller = document.getElementById("collapsible-output")
  scroller.scrollTo(0, outputPanelContent.scrollHeight)
}

