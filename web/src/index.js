// catch errors before you run, setup your IDE to use tsserver:
// @ts-check
// read more: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
import DiverEditor from './editor/editor.js'
import DiverVisual from './diverComponent.js'
import { getElementOrError, compressAndEncodeToUrlSafeBase64, decodeAndDecompressFromUrlSafeBase64 } from './utils.js'
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


//initialze diverVisual (handles running python and sketch output)
const diverVisual = new DiverVisual()
diverVisual.id = "mainDiverVisual"

//initialze user sketch
const sketchFileName = getURLParam('filename')
const sketchEncodedCompressed = getURLParam('b64Sketch')

if (sketchFileName) {
  console.log("file requested from url: ", sketchFileName)
  diverVisual.sketchFileName = sketchFileName
} else if (sketchEncodedCompressed) {
  console.log("file encoded in URL, decoding/decompressing: ", sketchEncodedCompressed)

  const sketchSrcString = decodeAndDecompressFromUrlSafeBase64(sketchEncodedCompressed)
  console.log("decoded decompressed: ", sketchSrcString)
  diverEditor.setText(sketchSrcString)
  diverVisual.rawSrcString = sketchSrcString
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
  const runButton = getElementOrError('runButton')
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

  const shareButton = getElementOrError("shareButton")
  const copyToClipboardLink = getElementOrError("copyToClipboardLink")
  const longShareLink = getElementOrError("longShareLink")
  copyToClipboardLink.addEventListener('click', function() {
    copyTextToClipboard(longShareLink.textContent)
    copyToClipboardLink.textContent = "Copied!"
  })

  shareButton.addEventListener('click', function() {
    console.log("creating shareable link")
    const sketchSrcString = diverEditor.getText()
    const compressedEncodedSrc = compressAndEncodeToUrlSafeBase64(sketchSrcString);
    console.log("uncompressed source length: ", sketchSrcString.length)
    console.log("compressed/encoded length: ", compressedEncodedSrc.length)
    const shareURL = window.location.host + "diver/?b64Sketch=" + compressedEncodedSrc
    longShareLink.textContent = shareURL
  })

  setupModal(getElementOrError("helpModal"), getElementOrError("helpButton"), getElementOrError("helpModalCloseBtn"))
  setupModal(getElementOrError("shareModal"), shareButton, getElementOrError("shareModalCloseBtn"))

  /**
   * @param {HTMLElement} modalContainer
   * @param {HTMLElement} modalLaunchButton
   * @param {HTMLElement} modalCloseButton
   */
  function setupModal(modalContainer, modalLaunchButton, modalCloseButton) {
    // When the user clicks the button, open the modal 
    modalLaunchButton.onclick = function() {
      for (let e of document.getElementsByClassName("modal")) {
        e.style.display = "none"
      }
      modalContainer.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    modalCloseButton.onclick = function() {
      modalContainer.style.display = "none";
    }

  }
  // Close the modal if the user clicks anywhere outside of it
  window.onclick = function(/** @type{Event} */event) {
    /** @type{HTMLElement}*/
    //@ts-ignore
    const target = event.target
    if (target.classList.contains("modal"))
      target.style.display = "none";
  }


  const toggleCodeButton = getElementOrError('toggleCodeButton');
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
  console.log("finished UI setup")

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


/**
 * get a filename URL parameter if present
 * @param {string} paramName
 * @returns {string | null}
 */
function getURLParam(paramName) {
  const currentUrl = window.location.href
  const url = new URL(currentUrl)
  const params = new URLSearchParams(url.search)

  //example URL "https://domain.com/page?filename=myfile.txt"
  const fileName = params.get(paramName) // This would be 'myfile.txt'
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

/**
 * @param {string | null} text
 */
function copyTextToClipboard(text) {
  if (text) {
    navigator.clipboard.writeText(text).then(function() {
      console.log('Copying to clipboard was successful!');
    }, function(err) {
      console.error('Could not copy text: ', err);
    });
  }
}

globalThis.reloadDiver = reloadDiverSrc // expose to global scope for dev server
//called from devserver when sketch src changes, great for editing sketches externally
globalThis.reloadSketch = () => { diverVisual.reloadSketchAndRun() } // expose to global scope for dev server


