(() => {
  const match = location.pathname.match(/^\/api\/hassio_ingress\/[^/]+/);
  if (!match) return;
  const prefix = match[0];
  globalThis.__DRYDOCK_INGRESS_BASE__ = prefix;
  const NativeURL = window.URL;
  function rewrite(value, base = location.href) {
    try {
      const url = new NativeURL(String(value), base);
      if (url.host === location.host && /^(https?|wss?):$/.test(url.protocol) &&
          !url.pathname.startsWith(prefix + '/') && url.pathname !== prefix) {
        url.pathname = prefix + url.pathname;
        return url.href;
      }
    } catch { /* pass malformed and non-URL values to the native API */ }
    return value;
  }
  const nativeFetch = window.fetch;
  window.fetch = (input, init) => nativeFetch.call(window,
    input instanceof Request ? new Request(rewrite(input.url), input) : rewrite(input), init);
  for (const name of ['EventSource', 'WebSocket']) {
    const Native = window[name];
    if (Native) window[name] = class extends Native { constructor(url, ...args) { super(rewrite(url), ...args); } };
  }
  const open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url, ...args) { return open.call(this, method, rewrite(url), ...args); };
  for (const method of ['pushState', 'replaceState']) {
    const original = history[method];
    history[method] = function(state, unused, url) { return original.call(this, state, unused, url == null ? url : rewrite(url)); };
  }
  function fix(element) {
    if (!(element instanceof Element)) return;
    for (const attr of ['href', 'src', 'action']) {
      const value = element.getAttribute(attr);
      if (value?.startsWith('/') && !value.startsWith('//') && !value.startsWith(prefix + '/')) element.setAttribute(attr, rewrite(value));
    }
  }
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'attributes') fix(record.target);
      for (const node of record.addedNodes) {
        fix(node);
        if (node.querySelectorAll) node.querySelectorAll('[href],[src],[action]').forEach(fix);
      }
    }
  }).observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['href', 'src', 'action'] });
  document.addEventListener('click', event => { const anchor = event.target.closest?.('a'); if (anchor) fix(anchor); }, true);
})();
