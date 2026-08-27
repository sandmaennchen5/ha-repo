import fs from 'node:fs';
import { spawn } from 'node:child_process';
import { prepareStorage } from './storage.mjs';
import { createIngressProxy } from './proxy.mjs';

const options = JSON.parse(fs.readFileSync('/data/options.json', 'utf8'));
const dataDir = prepareStorage(options);
const proxy = createIngressProxy({ remember: options.remember_ingress_users === true });
const child = spawn('/usr/local/bin/docker-entrypoint.sh', [], {
  stdio: 'inherit',
  env: { ...process.env, DATA_DIR: dataDir, PORT: '3000', HOST: '0.0.0.0', HTTPS_MODE: 'off' }
});
proxy.listen(1337, '0.0.0.0');
proxy.on('error', error => { console.error('Ingress listener failed:', error.message); child.kill('SIGTERM'); process.exitCode = 1; });
child.on('error', error => { console.error('Dockhand startup failed:', error.message); proxy.close(); process.exitCode = 1; });
child.on('exit', code => { proxy.close(); process.exit(code ?? 1); });
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => child.kill(signal));
