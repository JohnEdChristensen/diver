// @ts-check
//
import "https://cdn.jsdelivr.net/npm/pako@1.0.11/dist/pako.min.js"
/**
 * @template {HTMLElement} T
 * @param {string} id
 * @returns {T}
 */
export function getElementOrError(id) {
  const element = document.getElementById(id);
  if (!element) {
    throw new Error(`Element with ID '${id}' not found.`);
  }
  return /** @type {T} */ (element);
}

export function encodeForUrl(inputStr) {
  // Encode the string in Base64
  let base64Str = btoa(inputStr);
  // Make the Base64 string URL-safe by replacing "+" with "-", "/" with "_", and removing "="
  let urlSafeBase64Str = base64Str.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  return urlSafeBase64Str;
}
export function compressAndEncodeToUrlSafeBase64(text) {
  // Compress text using pako
  var compressed = pako.deflate(text, { to: 'string' });

  // Convert binary data to Base64
  var base64 = window.btoa(compressed);

  // Make the Base64 URL-safe
  var urlSafeBase64 = base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

  return urlSafeBase64;
}

export function decodeAndDecompressFromUrlSafeBase64(encodedText) {
  // Replace URL-safe Base64 characters to original
  var base64 = encodedText.replace(/-/g, '+').replace(/_/g, '/');

  // Decode Base64 to binary string
  var binaryString = window.atob(base64);

  // Convert binary string to character-number array
  var charCodeArray = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
    charCodeArray[i] = binaryString.charCodeAt(i);
  }

  // Decompress using pako
  var decompressed = pako.inflate(charCodeArray, { to: 'string' });

  return decompressed;
}

// test compression methods
// easiest to just call from console
function compare_compression(sketchSrcString) {
  console.log("original length: ", sketchSrcString.length); // Output: compressed string
  const encodedSketch = encodeForUrl(sketchSrcString)
  console.log("base64 encode length: ", encodedSketch.length); // Output: compressed string
  //Add following to index.html to test LZ compress. Pako performed better though using initial testing
  //<script src="https://cdnjs.cloudflare.com/ajax/libs/lz-string/1.4.4/lz-string.min.js"></script>
  // const compressedText = LZString.compressToBase64(sketchSrcString);
  // console.log("LZ compress base64", compressedText.length); // Output: compressed string
  // const UTF16compressedText = LZString.compressToUTF16(sketchSrcString);
  // console.log("LZ compress UTF16", UTF16compressedText.length); // Output: compressed string
  // const URIEncode = LZString.compressToEncodedURIComponent(sketchSrcString);
  // console.log("LZ URI:encode", URIEncode.length)
  const pakoText = compressAndEncodeToUrlSafeBase64(sketchSrcString);
  console.log("Pake compress", pakoText.length)
  console.log("Pake uncompress", decodeAndDecompressFromUrlSafeBase64(pakoText))
}
