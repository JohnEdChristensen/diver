import { basicSetup, EditorView } from "codemirror"
import { EditorState } from "@codemirror/state"
import { python } from "@codemirror/lang-python"
import { keymap, KeyBinding } from "@codemirror/view"
import { everforest } from "./theme-everforest.js"
import { indentUnit } from "@codemirror/language";
import {
  indentLess,
  indentMore,
} from "@codemirror/commands";

export default class DiverEditor extends HTMLElement {
  editorView: EditorView;
  initialDoc: string | null | undefined

  constructor(initialDoc?: string) {
    super()
    this.initialDoc = initialDoc
  }

  raiseRunCodeEvent() {
    console.log("User Running code via shortcut")
    return this.dispatchEvent(new CustomEvent("userRunCode"))
  }

  async connectedCallback() {
    //prioritize code passed in constructor, then inside HTML tag, then default to ""
    if (!this.initialDoc) {
      this.initialDoc = this.textContent ?? ""//initialize editor from just HTML
      this.textContent = "" //don't show the raw inner inital text
    }
    // The suggested tab binding: `import { indentWithTab } from "@codemirror/commands"`
    // didn't use 4 tabs for some reason.
    // workaround from https://github.com/microbit-foundation/python-editor-v3/blob/main/src/editor/codemirror/config.ts#L77
    const indentSize = 4
    const customTabBinding: KeyBinding = {
      key: "Tab",
      run: indentMore,
      shift: indentLess,
    };
    const runCodeBinding: KeyBinding = {
      //key: "Ctrl-Enter",
      key: "Ctrl-Enter",
      run: () => {
        this.raiseRunCodeEvent()
        return true
      }
    }
    this.editorView = new EditorView({
      doc: this.initialDoc,
      extensions: [
        //visual 
        everforest,
        //language
        python(),
        //tab
        keymap.of([customTabBinding, runCodeBinding]),
        EditorState.tabSize.of(indentSize),
        indentUnit.of(" ".repeat(indentSize)),
        // base setup, at the bottom so everything above overrides
        basicSetup,
      ],
      parent: this
    });
  }
  getText(): string {
    return this.editorView.state.doc.toString()
  }

  setText(text: string): void {
    // Create a transaction that replaces the entire document
    const transaction = this.editorView.state.update({
      changes: { from: 0, to: this.editorView.state.doc.length, insert: text }
    });

    // Apply the transaction
    this.editorView.dispatch(transaction);
  }
}

customElements.define("diver-editor", DiverEditor)
