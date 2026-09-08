const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');

function fixture(t, name, options, modules = {}, clock = Date) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'openccu-session-test-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const source = fs.readFileSync(path.join(__dirname, '../openccu/overlay', name), 'utf8')
    .split('const apiProxy = createProxyMiddleware({')[0]
    .replace('{{ printf "%q" (index . "webui-url") }}', '"http://openccu"');
  const facade = Object.create(fs);
  facade.readFileSync = (file, ...args) => String(file).endsWith('/options.json')
    ? JSON.stringify(options) : fs.readFileSync(file, ...args);
  const context = {
    require: name => modules[name] || (name === 'fs' ? facade : ['express', 'http-proxy-middleware', 'ipaddr.js'].includes(name) ? {} : require(name)),
    process: { env: { HM_INGRESS_SESSION_DIR: directory }, pid: process.pid },
    Buffer, URL, URLSearchParams, Date:clock, console: { log() {}, warn() {}, error() {} },
  };
  vm.runInNewContext(source + '\nglobalThis.api = {sessionFile, writeSessionRecord, readSessionRecord, restoreWebSession, writeUserSid, readUserSid, deleteUserSid, encryptCredentials, decryptCredentials, rememberedSid, loginRuntime};', context);
  return { directory, ...context.api };
}

for (const name of ['ha-proxy.js', 'ha-proxy.js.gtpl']) {
  for(const outcome of ['success', 'invalid-password', 'invalid-web-session']) {
    test(`${name}: WebUI re-login after restart (${outcome}), server guard works without browser storage`, async t => {
      const {EventEmitter} = require('node:events');
      let now=100000, posts=0;
      const http = {request(url, options, callback) {
        const req=new EventEmitter();
        req.destroy=()=>{};
        req.end=payload=>setImmediate(()=>{
          const response=new EventEmitter();
          response.headers={}; response.statusCode=200;
          let body='<form id="gwlogin"></form>';
          if(options.method==='POST') {
            posts++;
            assert.equal(url.pathname, '/login.htm');
            assert.equal(options.headers['Content-Type'], 'application/x-www-form-urlencoded');
            const fields=new URLSearchParams(payload.toString());
            assert.equal(fields.get('tbUsername'), 'test-user');
            assert.equal(fields.get('tbPassword'), 'p&+ ä');
            if(outcome!=='invalid-password') {
              response.statusCode=302;
              response.headers.location='/index.htm?sid=fresh-web-sid';
            }
          } else if(url.searchParams.get('sid')==='fresh-web-sid' && outcome==='success') {
            body='<script>var SessionId = "fresh-web-sid";</script>';
          }
          callback(response);
          response.emit('data',Buffer.from(body)); response.emit('end');
        });
        return req;
      }};
      const f=fixture(t,name,{remember_ingress_users:true,remember_ingress_credentials:true},{http},{now:()=>now});
      const req={headers:{'x-remote-user-id':'alice','x-ingress-path':'/ingress/test'}};
      const file=f.sessionFile(req);
      f.writeSessionRecord(file,{sid:'stale-sid',credentials:f.encryptCredentials({username:'test-user',password:'p&+ ä'})});
      const first=f.restoreWebSession(file);
      assert.equal((await f.restoreWebSession(file)).retryAfter,30); // Parallel tab.
      const result=await first;
      assert.equal(Boolean(result.ok),outcome==='success');
      assert.equal(posts,1);
      assert.equal(f.readSessionRecord(file).sid,outcome==='success'?'fresh-web-sid':'stale-sid');
      let redirects=0;
      const browser={window:{FormSubmit(){},location:{replace(){redirects++;}}},document:{getElementById(){return null;}},
        sessionStorage:{getItem(){throw Error('blocked');},setItem(){throw Error('blocked');}},Date,
        fetch:async()=>({json:()=>f.restoreWebSession(file)})};
      vm.runInNewContext(f.loginRuntime(req).replace(/^<script>|<\/script>$/g,''),browser);
      await new Promise(resolve=>setImmediate(resolve));
      assert.equal(redirects,0); assert.equal(posts,1);
      now+=31000;
      f.writeSessionRecord(file,{...f.readSessionRecord(file),sid:'another-expired-sid'});
      assert.equal(Boolean((await f.restoreWebSession(file)).ok),outcome==='success');
      assert.equal(posts,2); // Later restart is not permanently blocked.
    });
  }
  test(`${name}: restart permits another auto-login and successful index clears loop guard`, async t => {
    const f = fixture(t, name, {remember_ingress_users:true, remember_ingress_credentials:true});
    const req = {headers:{'x-remote-user-id':'alice', 'x-ingress-path':'/api/hassio_ingress/test'}};
    const values = new Map();
    let requests = 0, redirects = 0;
    const browser = {window:{FormSubmit(){}, location:{replace(){redirects++;}}},
      document:{getElementById(){return null;}},
      sessionStorage:{getItem:k=>values.get(k), setItem:(k,v)=>values.set(k,v), removeItem:k=>values.delete(k)},
      fetch:async()=>{requests++; return {json:async()=>({ok:true})};}, Date};
    const run = async authenticated => {
      const script = f.loginRuntime(req, authenticated).replace(/^<script>|<\/script>$/g, '');
      vm.runInNewContext(script, browser);
      await new Promise(resolve=>setImmediate(resolve));
    };
    await run(false);
    assert.equal(redirects, 1);
    await run(false); // Immediate loop is suppressed.
    assert.equal(requests, 1);
    await run(true); // Successful authenticated index page.
    assert.equal(values.size, 0);
    await run(false); // Same tab, CCU restarted and SID no longer valid.
    assert.equal(requests, 2);
    assert.equal(redirects, 2);
    for(const key of values.keys()) values.set(key, '1'); // Old patch's permanent flag.
    await run(false);
    assert.equal(requests, 3);
  });
  test(`${name}: sessions are isolated by HA identity and logout removes only that user`, t => {
    const f = fixture(t, name, { remember_ingress_users: true });
    const alice = { headers: { 'x-remote-user-id': 'alice' } };
    const bob = { headers: { 'x-remote-user-id': 'bob' } };
    f.writeUserSid(alice, 'sid-alice'); f.writeUserSid(bob, 'sid-bob');
    assert.equal(f.readUserSid(alice), 'sid-alice');
    assert.equal(f.readUserSid(bob), 'sid-bob');
    assert.notEqual(f.sessionFile(alice), f.sessionFile(bob));
    assert.equal(f.sessionFile({ headers: {} }), null);
    f.deleteUserSid(alice);
    assert.equal(f.readUserSid(alice), null);
    assert.equal(f.readUserSid(bob), 'sid-bob');
  });
  test(`${name}: credentials use authenticated encryption; tampering is rejected`, t => {
    const f = fixture(t, name, { remember_ingress_users: true, remember_ingress_credentials: true });
    const credentials = { username: 'test-user', password: 'only-for-local-test' };
    const encrypted = f.encryptCredentials(credentials);
    assert.ok(!JSON.stringify(encrypted).includes(credentials.password));
    assert.equal(f.decryptCredentials({ credentials: encrypted }).password, credentials.password);
    encrypted.tag = Buffer.alloc(16).toString('base64');
    assert.equal(f.decryptCredentials({ credentials: encrypted }), null);
  });
  test(`${name}: retention off creates no user store`, t => {
    const f = fixture(t, name, {});
    const req = { headers: { 'x-remote-user-id': 'alice' } };
    f.writeUserSid(req, 'sid-test');
    assert.equal(f.sessionFile(req), null);
    assert.equal(fs.readdirSync(f.directory).length, 0);
  });
}
