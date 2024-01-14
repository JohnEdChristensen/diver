import { basicSetup, EditorView } from "codemirror"
import { python } from "@codemirror/lang-python"
import { oneDark } from "@codemirror/theme-one-dark"
//import { languages } from "@codemirror/language-data"
//editor
const code_container = document.getElementById("code-container") ?? document.body;

export function createEditor(initialDoc: string) {
  return new EditorView({
    doc: initialDoc,
    extensions: [basicSetup, python(), oneDark],
    parent: code_container
  });
}

export function getEditorText(editor: EditorView) {
  return editor.state.doc.toString()
}

export function setEditorText(editor:EditorView, text: string) {
  // Create a transaction that replaces the entire document
  const transaction = editor.state.update({
    changes: { from: 0, to: editor.state.doc.length, insert: text }
  });

  // Apply the transaction
  editor.dispatch(transaction);
}

