// catch errors before you run, setup your IDE to use tsserver:
// @ts-check
// read more: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
import DiverEditor from './editor/editor.js'
import DiverVisual from './diverComponent.js'
import { getElementOrError } from './utils.js'

//initialze editor
const editorContainer = getElementOrError("code-container")
const diverEditor = new DiverEditor("", editorContainer)

//initialze output content
const outputPanelContent = getElementOrError("output-content")
outputPanelContent.textContent = "Initializing...\n"

//initialze diverVisual (handles running python and sketch output)
/** @type {DiverVisual} */
const diverVisual = getElementOrError("diverID")
diverVisual.addEventListener('sketchLoaded', e => {
  //@ts-ignore low priority
  diverEditor.setText(e.detail);
});

//initialze user sketch
let sketchFileName = getFileFromURL()
if (sketchFileName) {
  diverVisual.dynamicFileName = sketchFileName
}

/**setup that requires the DOM to be loaded */
document.addEventListener('DOMContentLoaded', function() {
  //main buttons
  const runButton = getElementOrError('run-button')
  runButton.addEventListener('click', () => {
    diverVisual.reloadSketch();
  })
  // initial panel setup
  panelToggleSetup()
})

/**Inital setup of output and editor panels */
function panelToggleSetup() {

  const toggleCodeButton = getElementOrError('toggle-code-button');
  const collapsibleCode = getElementOrError('collapsible-code');
  const codeContainer = getElementOrError("code-container");

  const toggleOutputButton = getElementOrError('toggle-output-button');
  const collapsibleOutput = getElementOrError('collapsible-output');

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

  // Event listeners
  toggleCodeButton.addEventListener('click', () => {
    togglePanel(toggleCodeButton, collapsibleCode, 'collapse', 'Code');
    codeContainer.style.visibility = collapsibleCode.classList.contains('collapse') ? "hidden" : "visible";
  });

  toggleOutputButton.addEventListener('click', () => {
    togglePanel(toggleOutputButton, collapsibleOutput, 'collapse', 'Output');
  });

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
 * @param {boolean} showSketchSrc - flag indicating if sketchSrc should also be added to output
 */
function addToOutput(text, showSketchSrc) {
  if (showSketchSrc) {
    outputPanelContent.textContent += ">>>" + diverEditor.getText() + "\n"
  }
  console.log(text)
  if (text != undefined) {
    outputPanelContent.textContent += text + "\n"
  }
  const scroller = getElementOrError("collapsible-output")
  scroller.scrollTo(0, outputPanelContent.scrollHeight)
}

/** called from dev server when source chanages */
async function reloadDiverSrc() {
  addToOutput("Diver src changed, reloading...", false)
  window.location.reload()
}
globalThis.reloadDiver = reloadDiverSrc // expose to global scope for dev server
//called from devserver when sketch src changes, great for editing sketches externally
globalThis.reloadSketch = diverVisual.reloadSketch // expose to global scope for dev server
