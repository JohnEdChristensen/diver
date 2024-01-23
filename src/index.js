"use strict"
import { DiverEditor } from './editor/editor.js'
import { PyodideManager } from './pyodideManager.js'

let pyodideManager = null
let diverLibString = ""
const diverEditor = new DiverEditor("")
const outputPanelContent = document.getElementById("output-content")
outputPanelContent.textContent = "Initializing...\n"



// init Pyodide
async function main() {

  startLoadingIndicator();
  console.log("Loading pyodide")

  pyodideManager = await PyodideManager.createPyodideInstance()
  await pyodideManager.installDiver(diverLibString)

  stopLoadingIndicator();

  outputPanelContent.textContent += "Python is Ready!\n"

  //run the initial code example for the first time
  await runSketch()
}
main()

function startLoadingIndicator() {
  document.querySelector('.loader').style.display = 'block'
}
function stopLoadingIndicator() {
  document.querySelector('.loader').style.display = 'none'
}


async function runSketch() {
  try {
    addToOutput("Running current sketch...", false)
    let pyCode = diverEditor.getText()
    let output = await pyodideManager.runPython(pyCode)
    addToOutput("Sketch Ran Successfully", false)
    addToOutput(output, false)
    console.log("Current Sketch Succeeded. Output(if any):" + output)
  } catch (err) {
    addToOutput(err, true)
    console.log("Current Sketch Failed. Output(if any):" + outputPanelContent)
  }
}

// setup code that needs DOM elements
document.addEventListener('DOMContentLoaded', function() {
  // load python code 
  loadDiver()
  loadSketch()
  // initial panel setup
  panelToggleSetup() 
})

function panelToggleSetup(){
  //main buttons
  const runButton = document.getElementById('run-button')
  runButton.addEventListener('click', runSketch)

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
  addToOutput("Sketch src changed, reloading...", false)
  await loadSketch()
  evaluatePython()
}
globalThis.reloadSketch = reloadSketch // expose to global scope for dev server

async function loadDiver() {
  await fetch('./diver.py')
    .then(response => response.text())
    .then(text => diverLibString = text)
    .catch(error => console.error('Error fetching the file:', error))
}

async function loadSketch() {
  let fileName = getFileFromURL() ?? './rainbow.py'
  await fetch("./sketches/" + fileName)
    .then(response => response.text())
    .then(text => diverEditor.setText(text))
    .catch(error => console.error('Error fetching the file:', error))
}

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

