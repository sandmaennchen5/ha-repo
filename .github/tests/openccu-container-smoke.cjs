// Run ONLY the ingress proxy in an isolated --network none container, not CCU init.
const fs = require('node:fs');
const { createRequire } = require('node:module');
const vm = require('node:vm');
const file = process.argv[2];
if (!['/bin/ha-proxy.js', '/app/ha-proxy.js.gtpl'].includes(file)) throw new Error('Unexpected proxy path');
process.env.HM_HAPROXY_SRC = '127.0.0.1/32';
let source = fs.readFileSync(file, 'utf8')
  .replace('{{ printf "%q" (index . "webui-url") }}', '"http://127.0.0.1:80"')
  .replaceAll('{{ index . "webui-url" }}', 'http://127.0.0.1:80');
vm.runInNewContext(source, {
  require: createRequire(file), process, Buffer, URL, URLSearchParams, console,
  setInterval, setTimeout, clearTimeout, clearInterval,
});
// Verify the ingress listener with a local request. Missing upstream must be
// handled as an HTTP error, not a startup/module-loading exception.
setTimeout(() => {
  const request = require('node:http').get('http://127.0.0.1:8099/', response => {
    response.resume();
    response.on('end', () => {
      if (response.statusCode < 400) throw new Error('Expected unavailable mock upstream');
      console.log('Isolated ingress listener is responding.');
      process.exit(0);
    });
  });
  request.on('error', error => { console.error(error); process.exit(1); });
}, 200);
setTimeout(() => { console.error('Ingress smoke test timed out'); process.exit(1); }, 10000);
