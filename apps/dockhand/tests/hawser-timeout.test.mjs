import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { withHawserComposeTimeout } from '../rootfs/usr/local/lib/dockhand-ha/hawser-timeout.mjs';

test('compose dispatch overrides the hidden 300s limits and preserves request options', async () => {
  let received;
  const handler = {};
  const signal = AbortSignal.abort();
  const delegate = { dispatch(options, actualHandler) {
    assert.equal(actualHandler, handler); received = options; return true;
  }};
  const fetch = withHawserComposeTimeout(async (input, init) => {
    assert.equal(init.signal, signal);
    assert.equal(init.body, 'compose payload');
    return init.dispatcher.dispatch({ path: '/_hawser/compose', headersTimeout: 300000, bodyTimeout: 300000, body: init.body }, handler);
  }, () => delegate, 1800000);
  assert.equal(await fetch('http://agent:2376/_hawser/compose', { method: 'POST', signal, body: 'compose payload' }), true);
  assert.equal(received.headersTimeout, 1800000);
  assert.equal(received.bodyTimeout, 1800000);
  assert.equal(received.body, 'compose payload');
});

test('unrelated requests retain their original dispatcher and options', async () => {
  for (const [url, method] of [
    ['http://agent/system/df', 'GET'],
    ['http://agent/_hawser/compose', 'GET'],
    ['http://agent/_hawser/compose/other', 'POST']
  ]) {
    const init = { method };
    const fetch = withHawserComposeTimeout(async (actualUrl, actualInit) => {
      assert.equal(actualUrl, url); assert.equal(actualInit, init);
    }, () => { throw Error('must not resolve dispatcher'); }, 1800000);
    await fetch(url, init);
  }
});

test('Request input and explicit or replaced global dispatchers are retained', async () => {
  let current;
  const calls = [];
  const first = { dispatch(options) { calls.push('first'); return true; }};
  const second = { dispatch(options) { calls.push('second'); return true; }};
  const fetch = withHawserComposeTimeout(async (input, init) => init.dispatcher.dispatch({}, {}), () => current, 900000);
  const request = new Request('http://agent/_hawser/compose', { method: 'POST' });
  current = first; await fetch(request);
  current = second; await fetch(request);
  await fetch(request, { dispatcher: first });
  assert.deepEqual(calls, ['first', 'second', 'first']);
});

test('launcher maps options without enabling false-valued collector switches', () => {
  const source = fs.readFileSync(new URL('../rootfs/usr/local/lib/dockhand-ha/launcher.mjs', import.meta.url), 'utf8').replace(/^import .*;\n/gm, '');
  function environment(options) {
    let result;
    const proxy = { listen() {}, on() {} };
    vm.runInNewContext(source, {
      fs: { readFileSync: () => JSON.stringify(options) },
      prepareStorage: () => '/data/dockhand',
      createIngressProxy: () => proxy,
      spawn: (command, args, config) => { result = config.env; return { on() {} }; },
      process: { env: { SKIP_DF_COLLECTION: 'false', MINIMUM_RELEASE_AGE_HOURS: '72', NODE_OPTIONS: '--use-openssl-ca' }, on() {} }
    });
    return result;
  }
  const defaults = environment({});
  assert.equal(defaults.COMPOSE_TIMEOUT, '900');
  assert.equal(defaults.REGISTRY_REQUEST_TIMEOUT, '10');
  assert.equal(defaults.DISABLE_LOCAL_LOGIN, 'false');
  assert.equal('SKIP_DF_COLLECTION' in defaults, false);
  assert.equal('MINIMUM_RELEASE_AGE_HOURS' in defaults, false);
  assert.match(defaults.NODE_OPTIONS, /^--use-openssl-ca --import=.*hawser-preload.mjs$/);
  const configured = environment({ compose_timeout: 1800, registry_request_timeout: 60, disable_local_login: true, skip_df_collection: true, minimum_release_age_hours: 0 });
  assert.equal(configured.COMPOSE_TIMEOUT, '1800');
  assert.equal(configured.REGISTRY_REQUEST_TIMEOUT, '60');
  assert.equal(configured.DISABLE_LOCAL_LOGIN, 'true');
  assert.equal(configured.SKIP_DF_COLLECTION, '1');
  assert.equal(configured.MINIMUM_RELEASE_AGE_HOURS, '0');
  assert.equal('SKIP_DF_COLLECTION' in environment({ skip_df_collection: false }), false);
});
