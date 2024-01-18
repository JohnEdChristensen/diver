import { createEditor, setEditorText, getEditorText } from './editor.js'

const codeEditor = createEditor("");
const output = document.getElementById("output-content");
output.textContent = "Initializing...\n";
let diver = "";

//@type{PyodideAPI}
// let pyodide = await loadPyodide();
let pyodide = null;

function addToOutput(s, showCode) {
  if (showCode) {
    output.textContent += ">>>" + getEditorText(codeEditor) + "\n";
  }
  console.log(s)
  if (s != undefined) {
    output.textContent += s + "\n";
  }
  const scroller = document.getElementById("collapsible-output");
  scroller.scrollTo(0, output.scrollHeight);
}

// init Pyodide
async function main() {
  startLoadingIndicator();
  console.log("Loading pyodide")
  pyodide = await loadPyodide();
  await pyodide.loadPackage("numpy");//TODO remove numpy dependancy,figure otu dynamic imports
  // await pyodide.loadPackage("micropip");//install mircopip to install other packages
  // const micropip = pyodide.pyimport("micropip");
  // await micropip.install("numpy");
  // install diver
  try {
    let install_diver_py =
      `
# https://pyodide.org/en/stable/usage/loading-custom-python-code.html#from-python
# Downloading a single file
import importlib
from pathlib import Path

Path("diver.py").write_text("""
`
      + diver +
      `
"""
)
importlib.invalidate_caches() # Make sure Python notices the new .py file
`

    console.log("Loading Diver")
    //console.log(install_diver_py)
    let output = pyodide.runPython(install_diver_py);
    console.log("Installed diver. Output (if any):", output)
  } catch (err) {
    console.log("Error installing diver")
    console.log(diver)
    console.log(err)
  }
  output.textContent += "Python is Ready!\n";
  //run the inital code example for the first time
  console.log("Running Initial Sketch")
    stopLoadingIndicator();
  await runPython()
}

async function evaluatePython() {
  addToOutput("Running Python ad hoc...", false)
  console.log("Running Python ad hoc...")
  console.log("Running Current Sketch")
  runPython(pyodide)
}

async function runPython() {
  try {
    let pyCode = getEditorText(codeEditor)
    //this should work to dynamically install packages, but it isn't... I'll manuall install for now.
    // await pyodide.loadPackagesFromImports(pyCode,{messageCallback : (m)=>{console.log(m)}})
    let output = await pyodide.runPythonAsync(pyCode);
    addToOutput("Sketch Ran Successfully", false);
    addToOutput(output, false);
    console.log("Current Sketch Succeeded. Output(if any):" + output)
  } catch (err) {
    addToOutput(err, true);
    console.log("Current Sketch Failed. Output(if any):" + output)
  }
}
function startLoadingIndicator(){
  document.querySelector('.loader').style.display = 'block';
}
function stopLoadingIndicator(){
  document.querySelector('.loader').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
  // side toggle
  const runButton = document.getElementById('run-button');
  runButton.addEventListener('click', evaluatePython)
  const toggleCodeButton = document.getElementById('toggle-code-button');
  const collapsibleCode = document.getElementById('collapsible-code');

  toggleCodeButton.addEventListener('click', function() {
    // Toggle the collapsed class
    collapsibleCode.classList.toggle('collapse');
    if (collapsibleCode.classList.contains('collapse')) {
      toggleCodeButton.textContent = 'Show Code';
      document.getElementById("code-container").style.visibility = "hidden"
    } else {
      toggleCodeButton.textContent = 'Hide Code';
      document.getElementById("code-container").style.visibility = "visible"
    }
  });
  //bottom toggle
  const toggleOutputButton = document.getElementById('toggle-output-button');
  const collapsibleOutput = document.getElementById('collapsible-output');

  toggleOutputButton.addEventListener('click', function() {
    // Toggle the output-collapse class
    collapsibleOutput.classList.toggle('collapse');
    if (collapsibleOutput.classList.contains('collapse')) {
      toggleOutputButton.textContent = 'Show Output';
    } else {
      toggleOutputButton.textContent = 'Hide Output';
    }
  });
  loadDiver()
  loadSketch()
});

async function reloadDiver() {
  addToOutput("Diver src changed, reloading...", false);
  // await loadDiver();//make sure file is loaded before continouing!
  // pyodide.setInterruptBuffer;
  // main();
  window.location.reload();
}
globalThis.reloadDiver = reloadDiver
async function reloadSketch() {
  addToOutput("Sketch src changed, reloading...", false);
  await loadSketch();
  evaluatePython();
}
globalThis.reloadSketch = reloadSketch
async function loadDiver() {
  await fetch('./diver.py')
    .then(response => response.text())
    .then(text => diver = text)
    .catch(error => console.error('Error fetching the file:', error))
}
async function loadSketch() {
  let fileName = getFileFromURL()??'./draw.py'

  await fetch(fileName)
    .then(response => response.text())
    .then(text => setEditorText(codeEditor, text))
    .catch(error => console.error('Error fetching the file:', error));
}
function getFileFromURL(){
  const currentUrl = window.location.href;
  const url = new URL(currentUrl);
  const params = new URLSearchParams(url.search);

  //example URL "https://domain.com/page?filename=myfile.txt"
  const fileName = params.get('filename'); // This would be 'myfile.txt'
  return fileName
}
main();
