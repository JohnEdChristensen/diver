
const output = document.getElementById("output-content");
const code = document.getElementById("code-content");
output.textContent = "Initializing...\n";
let diver = ""

function addToOutput(s, showCode) {
  if (showCode) {
    output.textContent += ">>>" + code.textContent + "\n";
  }
  output.textContent += s + "\n";
}
// init Pyodide
async function main() {
  console.log("Loading Pyodide")
  let pyodide = await loadPyodide();
  console.log("Loading Numpy")
  await pyodide.loadPackage("numpy")
  // install diver
  try {
    install_diver_py =
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
    console.log("Installed diver")
  } catch (err) {
    console.log("Error installing diver")
    console.log(diver)
    console.log(err)
  }
  output.textContent += "Python is Ready!\n";
  //run the inital code example for the first time
  console.log("Running Initial Sketch")
  await runPython(pyodide)
  return pyodide;
}
let pyodideReadyPromise = main();

async function evaluatePython() {
  addToOutput("Running Python...", false)
  console.log("Running Current Sketch")
  let pyodide = await pyodideReadyPromise;
  runPython(pyodide)
}

async function runPython(pyodide) {
  try {
    let output = await pyodide.runPythonAsync(code.textContent);
    addToOutput(output, false);
    console.log("Current Sketch Succeeded. Output(if any):" + output)
  } catch (err) {
    addToOutput(err, true);
    console.log("Current Sketch Failed. Output(if any):" + output)
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // side toggle
  const toggleCodeButton = document.getElementById('toggle-code-button');
  const collapsibleCode = document.getElementById('collapsible-code');

  toggleCodeButton.addEventListener('click', function() {
    // Toggle the collapsed class
    collapsibleCode.classList.toggle('collapse');
    if (collapsibleCode.classList.contains('collapse')) {
      toggleCodeButton.textContent = 'Show Code';
    } else {
      toggleCodeButton.textContent = 'Hide Code';
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

function reloadDiver() {
  addToOutput("Diver src changed, reloading...", false);
  loadDiver();
  main();
}
function reloadSketch() {
  addToOutput("Sketch src changed, reloading...", false);
  loadSketch();
  evaluatePython();
}
function loadDiver() {
  fetch('./diver.py')
    .then(response => response.text())
    .then(text => diver = text)
    .catch(error => console.error('Error fetching the file:', error))
}
function loadSketch() {
  const codeContent = document.getElementById('code-content');
  fetch('./draw.py')
    .then(response => response.text())
    .then(text => codeContent.textContent = text)
    .catch(error => console.error('Error fetching the file:', error));
}
