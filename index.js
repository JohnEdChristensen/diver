const output = document.getElementById("output-content");
const code = document.getElementById("code-content");

function addToOutput(s,showCode) {
  if(showCode){
  output.textContent += ">>>" + code.textContent + "\n";
  }
  output.textContent += s + "\n";
}

output.textContent = "Initializing...\n";
// init Pyodide
async function main() {
  let pyodide = await loadPyodide();
  output.textContent += "Ready!\n";
  return pyodide;
}
let pyodideReadyPromise = main();

async function evaluatePython() {
    addToOutput("Running Python...",false)
  let pyodide = await pyodideReadyPromise;
  try {
    let output = pyodide.runPython(code.textContent);
    addToOutput(output,false);
  } catch (err) {
    addToOutput(err,true);
  }
}



document.addEventListener('DOMContentLoaded', function () {
  // side toggle
  const codeContent = document.getElementById('code-content');
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
  const outputContent = document.getElementById('output-content');
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

  fetch('./main.py') // Adjust the path as necessary
    .then(response => response.text())
    .then(text => codeContent.textContent = text)
    .catch(error => console.error('Error fetching the file:', error));
});