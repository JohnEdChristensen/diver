// @ts-check


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

