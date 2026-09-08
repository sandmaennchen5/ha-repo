// Run inside the built Drydock image, without Docker socket or network access.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const { once } = require('node:events');
const session = require('/home/node/app/node_modules/express-session');
const Store = require('/usr/local/lib/drydock-ha/session-store.cjs')(session);

(async () => {
  const { createIngressProxy } = await import('/usr/local/lib/drydock-ha/proxy.mjs');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'drydock-session-'));
  const database = path.join(dir, 'dd.json');
  const original = '{"application":"must remain unchanged"}';
  fs.writeFileSync(database, original);
  let store, backend, proxy;
  async function start() {
    store = new Store({ path: database, ttl: 86400 });
    await once(store, 'connect');
    const middleware = session({ name:'drydock.sid', store,
      secret:'test-secret-stable-across-restarts', resave:false, saveUninitialized:false,
      cookie:{ maxAge:86400000, httpOnly:true } });
    backend = http.createServer((req, res) => middleware(req, res, error => {
      assert.ifError(error);
      if (req.url === '/login') { req.session.user='test-user'; res.end('logged in'); }
      else if (req.url === '/auth/logout') {
        req.session.destroy(err => {
          assert.ifError(err);
          res.setHeader('Set-Cookie', 'drydock.sid=; Max-Age=0; Path=/');
          res.end('logged out');
        });
      } else { res.statusCode=req.session.user ? 200 : 401; res.end('checked'); }
    }));
    backend.listen(0, '127.0.0.1'); await once(backend, 'listening');
    proxy = createIngressProxy({ backendPort:backend.address().port, remember:true,
      sessionDirectory:path.join(dir, 'ingress'), allowedPeers:new Set(['127.0.0.1']) });
    proxy.listen(0, '127.0.0.1'); await once(proxy, 'listening');
  }
  async function stop() {
    await new Promise(resolve => proxy.close(resolve));
    await new Promise(resolve => backend.close(resolve));
    // No save during shutdown: login/logout must already have been durable.
    store.client.autosaveDisable();
    store.collection.setTTL(-1);
  }
  function request(url, user='alice', prefix='first') {
    return new Promise((resolve, reject) => {
      const req=http.get({hostname:'127.0.0.1',port:proxy.address().port,path:url,
        headers:{'x-ingress-path':`/api/hassio_ingress/${prefix}`, 'x-remote-user-id':user}}, res => {
        res.resume(); res.on('end',()=>resolve(res.statusCode));
      });
      req.on('error',reject);
    });
  }
  try {
    await start();
    assert.equal(await request('/me'), 401);
    assert.equal(await request('/login'), 200);
    assert.equal(await request('/me'), 200);
    assert.equal(fs.readFileSync(database,'utf8'), original);
    assert.equal(fs.statSync(database+'.sessions').mode & 0o777, 0o600);
    await stop();
    await start();
    // Neither browser cookies nor the previous ingress URL are needed.
    assert.equal(await request('/me','alice','after-restart'), 200);
    assert.equal(await request('/me','bob','after-restart'), 401);
    assert.equal(await request('/auth/logout'), 200);
    await stop();
    await start();
    assert.equal(await request('/me'), 401);
    assert.equal(fs.readFileSync(database,'utf8'), original);
    await stop();
    console.log('PASS: remembered session survives restart; HA users isolated; logout persists; main database unchanged.');
  } finally {
    fs.rmSync(dir,{recursive:true,force:true});
  }
})().then(()=>process.exit(0),error=>{console.error(error);process.exit(1);});
