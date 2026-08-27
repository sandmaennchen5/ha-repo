import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

export function patchSessionStore(source) {
  const pattern = /from\s+(['"])connect-loki\1/g;
  const matches = [...source.matchAll(pattern)];
  if (matches.length !== 1) throw new Error(`Expected one connect-loki import, found ${matches.length}; review upstream session implementation`);
  return source.replace(pattern, "from '/usr/local/lib/drydock-ha/session-store.cjs'");
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const file = process.argv[2] ?? '/home/node/app/dist/api/auth.js';
  fs.writeFileSync(file, patchSessionStore(fs.readFileSync(file, 'utf8')));
}
