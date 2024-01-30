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

export default class DiverEditor {
  editorView: EditorView;

  constructor(initialDoc: string, parent: HTMLElement) {
    // the suggested tab binding: import { indentWithTab } from "@codemirror/commands"
    // didn't use 4 tabs for some reason.
    // workaround from https://github.com/microbit-foundation/python-editor-v3/blob/main/src/editor/codemirror/config.ts#L77
    const indentSize = 4
    const customTabBinding: KeyBinding = {
      key: "Tab",
      run: indentMore,
      shift: indentLess,
    };
    this.editorView = new EditorView({
      doc: initialDoc,
      extensions: [basicSetup,
        //visual 
        everforest,
        //language
        python(),
        //tab
        keymap.of([customTabBinding]),
        EditorState.tabSize.of(indentSize),
        indentUnit.of(" ".repeat(indentSize))
      ],
      parent: parent
    });
    console.log(this.editorView.state.tabSize)
    // Assuming `myEditor` is your EditorView instance
    const currentIndentUnit = this.editorView.state.facet(EditorState.tabSize);

    console.log("Current indentUnit:", currentIndentUnit);
    // Assuming `myEditor` is your instance of EditorView
    // const indentConfig = this.editorView.state.facet(indentUnit);
    // console.log("Current Indentation Setting:", indentConfig);

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

