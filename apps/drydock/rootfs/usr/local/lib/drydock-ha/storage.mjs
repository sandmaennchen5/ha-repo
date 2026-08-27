import fs from 'node:fs';
import path from 'node:path';

function safeDirectory(root, relative) {
  const parts = relative.split('/');
  if (!parts.length || parts.some(p => !/^[A-Za-z0-9_-][A-Za-z0-9_.-]*$/.test(p))) {
    throw new Error('Invalid storage directory; use a relative path without dot segments');
  }
  let current = root;
  for (const part of parts) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) {
      throw new Error('Storage paths must not contain symlinks');
    }
    fs.mkdirSync(current, { recursive: true });
  }
  return current;
}

export function prepareStorage(options, roots = { data: '/data', config: '/config', share: '/share' }) {
  const location = options.storage_location ?? 'data';
  if (!Object.hasOwn(roots, location)) throw new Error('Invalid storage_location');
  const relative = location === 'share' ? (options.share_storage_directory ?? 'drydock-config') : 'drydock';
  if (location === 'share' && relative.split('/')[0] === 'ingress-sessions') throw new Error('Reserved storage directory');
  const target = safeDirectory(roots[location], relative);
  const marker = path.join(roots.data, '.drydock-storage.json');
  let source = path.join(roots.data, 'drydock');
  if (fs.existsSync(source) && fs.lstatSync(source).isSymbolicLink()) throw new Error('Storage paths must not contain symlinks');
  if (!fs.existsSync(source) || !fs.readdirSync(source).length) source = roots.data;
  if (fs.existsSync(marker)) {
    const previous = JSON.parse(fs.readFileSync(marker, 'utf8'));
    if (!Object.hasOwn(roots, previous.location)) throw new Error('Invalid previous storage location');
    source = safeDirectory(roots[previous.location], previous.relative);
  }
  if (source !== target) {
    if (source !== roots.data && (target.startsWith(source + path.sep) || source.startsWith(target + path.sep))) {
      throw new Error('Storage source and destination must not overlap');
    }
    const names = fs.readdirSync(source).filter(name => source !== roots.data || name === 'dd.json');
    if (names.length) {
      if (fs.readdirSync(target).length) throw new Error('Destination storage is not empty; refusing to overwrite it. Choose an empty directory.');
      // Copy while the application is stopped. Originals remain a recovery copy.
      for (const name of names) fs.cpSync(path.join(source, name), path.join(target, name), { recursive: true, errorOnExist: true, force: false, verbatimSymlinks: true });
      console.log('Drydock state copied to selected storage; previous location retained.');
    }
  }
  fs.writeFileSync(`${marker}.tmp`, JSON.stringify({ location, relative }), { mode: 0o600 });
  fs.renameSync(`${marker}.tmp`, marker);
  return target;
}
