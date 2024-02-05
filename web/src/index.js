// catch errors before you run, setup your IDE to use tsserver:
// @ts-check
// read more: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
import DiverEditor from './editor/editor.js'
import DiverVisual from './diverComponent.js'
import { getElementOrError } from './utils.js'

//initialze editor
/**@type{DiverEditor} */
const diverEditor = getElementOrError("diver-editor")

//editor events
diverEditor.addEventListener("userRunCode", () => {
  runEditorSketch()
})
//site-wide events
document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.key === 'Enter') {
    event.preventDefault();
    runEditorSketch()
  }
});

//initialze user sketch
let sketchFileName = getFileFromURL()


//initialze diverVisual (handles running python and sketch output)
const diverVisual = new DiverVisual()
diverVisual.id = "mainDiverVisual"
if (sketchFileName) {
  console.log("file requested from url: ", sketchFileName)
  diverVisual.sketchFileName = sketchFileName
}

//update the editor everytime diverVisual loads a new sketch
diverVisual.addEventListener('sketchLoaded', e => {
  //@ts-ignore low priority
  diverEditor.setText(e.detail);
  addToOutput("Sketch Loaded")
});

//update the output panel when code is run
diverVisual.addEventListener('sketchRan', e => {
  //@ts-ignore low priority
  const sketchReults = e.detail
  if (sketchReults) {
    //@ts-ignore low priority
    addToOutput(sketchReults)
  }
  else {
    addToOutput("Sketch Ran")
  }
});

//update the output panel when code is run
diverVisual.addEventListener('pythonError', e => {
  //@ts-ignore low priority
  addToOutput("There was a python error:\n" + e.detail, "error")
  //TODO force output panel on #2
});

//put diverVisual onto the DOM
const diverVisualContainer = getElementOrError("diver-container")
diverVisualContainer.append(diverVisual)

//initialze output content
const outputPanelContent = getElementOrError("output-content")
outputPanelContent.textContent = "Initializing...\n"


/**setup that requires the DOM to be loaded */
document.addEventListener('DOMContentLoaded', function() {
  //main buttons
  const runButton = getElementOrError('run-button')
  runButton.addEventListener('click', () => {
    runEditorSketch()
  })
  // initial panel setup
  //TODO make output a child of code panel. see p5js editor for inspiration #3
  panelToggleSetup()
})


//utilities
function runEditorSketch() {
  diverVisual.runSketchString(diverEditor.getText());
}

/**Inital setup of output and editor panels */
function panelToggleSetup() {
  //help modal setup
  var helpModal = getElementOrError("helpModal");
  var helpBtn = getElementOrError("helpBtn");
  var closeSpan = getElementOrError("helpModalCloseBtn");

  // When the user clicks the button, open the modal 
  helpBtn.onclick = function() {
    helpModal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  closeSpan.onclick = function() {
    helpModal.style.display = "none";
  }

  // Close the modal if the user clicks anywhere outside of it
  window.onclick = function(event) {
    if (event.target == helpModal) {
      helpModal.style.display = "none";
    }
  }
  const toggleCodeButton = getElementOrError('toggle-code-button');
  const collapsibleCode = getElementOrError('collapsible-code');
  const codeContainer = getElementOrError("code-container");

  const toggleOutputButton = getElementOrError('toggle-output-button');
  const collapsibleOutput = getElementOrError('collapsible-output');


  // Event listeners
  toggleCodeButton.addEventListener('click', () => {
    togglePanel(toggleCodeButton, collapsibleCode, 'collapse', 'Code');
    codeContainer.style.visibility = collapsibleCode.classList.contains('collapse') ? "hidden" : "visible";
  });

  // TODO: refactor this to have a function that can toggle, or force on/off #3
  toggleOutputButton.addEventListener('click', () => {
    togglePanel(toggleOutputButton, collapsibleOutput, 'collapse', 'Output');
  });

}
/**Utility function to toggle elements and button text
 * @param {HTMLElement} button
 * @param {HTMLElement} element
 * @param {string} className
 * @param {string} textContent
*/
function togglePanel(button, element, className, textContent) {
  element.classList.toggle(className)
  button.textContent = element.classList.contains(className) ? `Show ${textContent}` : `Hide ${textContent}`
}


/**get a filename URL parameter if present
 * @returns {string | null}
 */
function getFileFromURL() {
  const currentUrl = window.location.href
  const url = new URL(currentUrl)
  const params = new URLSearchParams(url.search)

  //example URL "https://domain.com/page?filename=myfile.txt"
  const fileName = params.get('filename') // This would be 'myfile.txt'
  return fileName
}

/**
 * @param {string} text - text to be added
 * @param {string} [style]
 */
function addToOutput(text, style) {
  const line = document.createElement('div')
  line.textContent = text
  if (style) {
    line.className = style
  }
  outputPanelContent.append(line)

  //make sure output pane scrolls to the bottom
  const scroller = getElementOrError("collapsible-output")
  scroller.scrollTo(0, outputPanelContent.scrollHeight)
}

/** called from dev server when source chanages */
async function reloadDiverSrc() {
  window.location.reload()
}
globalThis.reloadDiver = reloadDiverSrc // expose to global scope for dev server
//called from devserver when sketch src changes, great for editing sketches externally
globalThis.reloadSketch = () => { diverVisual.reloadSketchAndRun() } // expose to global scope for dev server
