import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export function patchRouter(text) {
  let count = 0;
  const output = text.replace(/history\s*:\s*([\w$]+)\(\s*(['"`])\/\2\s*\)/g, (_, fn) => {
    count++;
    return `history:${fn}(globalThis.__DRYDOCK_INGRESS_BASE__||"/")`;
  });
  return { output, count };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const directory = process.argv[2] ?? '/home/node/app/ui/assets';
  let count = 0;
  for (const name of fs.readdirSync(directory)) {
    if (!name.endsWith('.js')) continue;
    const file = path.join(directory, name);
    const result = patchRouter(fs.readFileSync(file, 'utf8'));
    if (result.count) { fs.writeFileSync(file, result.output); count += result.count; }
  }
  if (count !== 1) throw new Error(`Expected one Vue router base; found ${count}. Review upstream UI before publishing.`);
}
