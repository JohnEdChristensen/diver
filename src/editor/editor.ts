import { basicSetup, EditorView } from "codemirror"
import { python } from "@codemirror/lang-python"
import { everforest } from "./theme-everforest.js"

const code_container = document.getElementById("code-container") ?? document.body;

export class DiverEditor {
  editorView: EditorView;

  constructor(initialDoc: string) {
    this.editorView = new EditorView({
      doc: initialDoc,
      extensions: [basicSetup, python(), everforest],
      parent: code_container
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

