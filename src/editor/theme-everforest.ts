import { EditorView } from "@codemirror/view"
import { Extension } from "@codemirror/state"
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language"
import { tags as t } from "@lezer/highlight"


// previuos oneDark colors
// https://github.com/one-dark/vscode-one-dark-theme/ as reference for the colors
// const chalky = "#e5c07b",
//   coral = "#e06c75",
//   cyan = "#56b6c2",
//   invalid = "#ffffff",
//   ivory = "#abb2bf",
//   stone = "#7d8799", // Brightened compared to original to increase contrast
//   malibu = "#61afef",
//   sage = "#98c379",
//   whiskey = "#d19a66",
//   violet = "#c678dd",;
//   darkBackground = "#21252b",
//   highlightBackground = "#2c313a",
//   background = "#282c34",
//   tooltipBackground = "#353a42",
//   selection = "#3E4451",
//   cursor = "#528bff"


// everforest theme colors
// https://github.com/sainnhe/everforest/blob/master/palette.md
const yellow = "#DBBC7F", // Originally #e5c07b
  red = "#E67E80", // Originally #e06c75
  aqua = "#83C092", // Originally #56b6c2
  invalid = "#514045", // Originally #ffffff
  ivory = "#D3C6AA", // Originally #abb2bf,
  grey0 = "#7A8478", // Originally #7d8799
  blue = "#7FBBB3", // Originally #61afef,
  green = "#A7C080", // Originally #98c379, 
  orange = "#E69875", // Originally #d19a66, 
  purple = "#D699B6", // Originally #c678dd
  bg_dim = "#232A2E", // Originally #21252b
  bg1 = "#343F44", // Originally #2c313a, 
  bg0 = "#2D353B", // Originally #282c34
  bg2 = "#3D484D", // Originally #353a42
  bg3 = "#475258", // Originally #3E4451
  cursor = ivory; // no origional

/// The colors used in the theme, as CSS color strings.
export const color = {
  yellow,
  red,
  aqua,
  invalid,
  ivory,
  grey0,
  blue,
  green,
  orange,
  purple,
  bg_dim,
  bg1,
  bg0,
  bg2,
  bg3,
  cursor
}

/// The editor theme styles for One Dark.
export const everforestTheme = EditorView.theme({
  "&": {
    color: ivory,
    backgroundColor: bg0
  },

  ".cm-content": {
    caretColor: cursor
  },

  ".cm-cursor, .cm-dropCursor": { borderLeftColor: cursor },
  "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection": { backgroundColor: bg3 },

  ".cm-panels": { backgroundColor: bg_dim, color: ivory },
  ".cm-panels.cm-panels-top": { borderBottom: "2px solid black" },
  ".cm-panels.cm-panels-bottom": { borderTop: "2px solid black" },

  ".cm-searchMatch": {
    backgroundColor: "#72a1ff59",
    outline: "1px solid #457dff"
  },
  ".cm-searchMatch.cm-searchMatch-selected": {
    backgroundColor: "#6199ff2f"
  },

  ".cm-activeLine": { backgroundColor: "#6699ff0b" },
  ".cm-selectionMatch": { backgroundColor: "#aafe661a" },

  "&.cm-focused .cm-matchingBracket, &.cm-focused .cm-nonmatchingBracket": {
    backgroundColor: "#bad0f847"
  },

  ".cm-gutters": {
    backgroundColor: bg0,
    color: grey0,
    border: "none"
  },

  ".cm-activeLineGutter": {
    backgroundColor: bg1
  },

  ".cm-foldPlaceholder": {
    backgroundColor: "transparent",
    border: "none",
    color: "#ddd"
  },

  ".cm-tooltip": {
    border: "none",
    backgroundColor: bg2
  },
  ".cm-tooltip .cm-tooltip-arrow:before": {
    borderTopColor: "transparent",
    borderBottomColor: "transparent"
  },
  ".cm-tooltip .cm-tooltip-arrow:after": {
    borderTopColor: bg2,
    borderBottomColor: bg2
  },
  ".cm-tooltip-autocomplete": {
    "& > ul > li[aria-selected]": {
      backgroundColor: bg1,
      color: ivory
    }
  }
}, { dark: true })


// export const pythonHighlighting = {
//   "async \"*\" \"**\" FormatConversion FormatSpec": t.modifier,
//   "CallExpression/MemberExpression/PropertyName": t.function(t.propertyName),
//   At: t.meta,
// }
/// The highlighting style for code in the everforest ish theme
export const everforestHighlightStyle = HighlightStyle.define([
  {
    //   "with as print": t.keyword,
    //   "for while if elif else try except finally return raise break continue with pass assert await yield match case": t.controlKeyword,
    tag: t.keyword,
    color: purple
  },
  {
    //   VariableName: t.variableName,
    //   PropertyName: t.propertyName,
    //   Ellipsis: t.punctuation,
    //   "( )": t.paren,
    //   "[ ]": t.squareBracket,
    //   "{ }": t.brace,
    tag: [t.name, t.punctuation, t.deleted, t.character, t.macroName],
    color: ivory
  },
  {
    //   "CallExpression/VariableName": t.function(t.variableName),
    //   "FunctionDefinition/VariableName": t.function(t.definition(t.variableName)),
    tag: [t.function(t.variableName), t.labelName],
    color: green
  },
  {
    tag: [t.propertyName],
    color: blue
  },
  {
    tag: [t.color, t.constant(t.name), t.standard(t.name)],
    color: orange
  },
  {
    //   Number: t.number,
    //   "ClassDefinition/VariableName": t.definition(t.className),
    tag: [t.definition(t.name),t.number],
    color: yellow
  },
  {
    //   At: t.meta,
    tag: [t.typeName, t.className, t.changed, t.annotation, t.modifier, t.self, t.namespace, t.meta],
    //   None: t.null,
    color: yellow
  },
  {
    //   "from def class global nonlocal lambda": t.definitionKeyword,
    //   import: t.moduleKeyword,
    tag: [t.definitionKeyword,t.moduleKeyword],
    color: red
  },
  {
    //   String: t.string,
    //   FormatString: t.special(t.string),
    tag: [t.string],
    color: aqua
  },
  {
    //   "in not and or is del": t.operatorKeyword,
    //   ".": t.derefOperator,
    //   ", ;": t.separator
    tag: [t.derefOperator,t.url, t.escape, t.regexp, t.link, t.special(t.string),t.separator],
    color: ivory
  },
  {
    //   Comment: t.lineComment,
    tag: [t.comment],
    color: grey0
  },
  {
    tag: t.strong,
    fontWeight: "bold"
  },
  {
    tag: t.emphasis,
    fontStyle: "italic"
  },
  {
    tag: t.strikethrough,
    textDecoration: "line-through"
  },
  {
    tag: t.link,
    color: grey0,
    textDecoration: "underline"
  },
  {
    tag: t.heading,
    fontWeight: "bold",
    color: red
  },
  {

    //   Boolean: t.bool,
    //   UpdateOp: t.updateOperator,
    //   "ArithOp!": t.arithmeticOperator,
    //   BitOp: t.bitwiseOperator,
    //   CompareOp: t.compareOperator,
    //   AssignOp: t.definitionOperator,
    tag: [t.atom, t.bool, t.special(t.variableName),t.operator,t.operatorKeyword],
    color: orange
  },
  {
    tag: [t.processingInstruction,  t.inserted],
    color: green
  },
  {
    tag: t.invalid,
    color: invalid
  },
])

/// Extension to enable the One Dark theme (both the editor theme and
/// the highlight style).
export const everforest: Extension = [everforestTheme, syntaxHighlighting(everforestHighlightStyle)]
