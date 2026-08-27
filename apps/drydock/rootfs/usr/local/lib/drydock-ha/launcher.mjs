import fs from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
import { prepareStorage } from './storage.mjs';
import { createIngressProxy } from './proxy.mjs';

const options = JSON.parse(fs.readFileSync('/data/options.json', 'utf8'));
const store = prepareStorage(options);
execFileSync('chown', ['-hR', 'node:node', store]);
fs.chmodSync(store, 0o700);
const environment = { ...process.env };
for (const item of options.environment ?? []) {
  if (!/^DD_[A-Z0-9_]+$/.test(item.name) || typeof item.value !== 'string') throw new Error('Invalid Drydock environment option');
  environment[item.name] = item.value;
}
if (options.auth_password_hash) {
  environment.DD_AUTH_BASIC_HA_USER = options.auth_username || 'admin';
  environment.DD_AUTH_BASIC_HA_HASH = options.auth_password_hash;
  environment.DD_ANONYMOUS_AUTH_CONFIRM = 'false';
}
// Fixed transport/storage settings cannot be overridden by extra options.
Object.assign(environment, { DD_STORE_PATH: store, DD_SERVER_PORT: '3000', DD_SERVER_TLS_ENABLED: 'false', DD_SERVER_TRUSTPROXY: '1' });
const proxy = createIngressProxy({ remember: options.remember_ingress_users === true });
const child = spawn('/usr/bin/entrypoint.sh', ['node', 'dist/index.js'], { stdio: 'inherit', env: environment });
proxy.listen(1337, '0.0.0.0');
proxy.on('error', error => { console.error('Ingress listener failed:', error.message); child.kill('SIGTERM'); process.exitCode = 1; });
child.on('error', error => { console.error('Drydock startup failed:', error.message); proxy.close(); process.exitCode = 1; });
child.on('exit', code => { proxy.close(); process.exit(code ?? 1); });
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => child.kill(signal));
