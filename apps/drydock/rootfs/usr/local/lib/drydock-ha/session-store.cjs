'use strict';

// Resolve the original libraries from the upstream app, not the HA overlay.
const { createRequire } = require('node:module');
const fs = require('node:fs');
const upstreamRequire = createRequire('/home/node/app/package.json');

function createDurableStore(session, connectLoki = upstreamRequire('connect-loki')) {
  const LokiStore = connectLoki(session);
  class DurableStore extends LokiStore {
    constructor(options) {
      // Two independent Loki instances must never save to the same dd.json.
      super({ ...options, path: `${options.path}.sessions`, autosave: false });
    }
  }
  for (const method of ['set', 'destroy', 'clear', 'touch']) {
    DurableStore.prototype[method] = function (...args) {
      const callback = typeof args.at(-1) === 'function' ? args.pop() : () => {};
      LokiStore.prototype[method].call(this, ...args, error => {
        if (error) return callback(error);
        this.client.saveDatabase(saveError => {
          if (saveError) return callback(saveError);
          try { fs.chmodSync(this.storePath, 0o600); }
          catch (permissionError) { return callback(permissionError); }
          callback(null);
        });
      });
    };
  }
  return DurableStore;
}

module.exports = createDurableStore;
