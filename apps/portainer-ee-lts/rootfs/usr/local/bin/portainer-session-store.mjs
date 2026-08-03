import http from 'node:http';
import fs from 'node:fs';
import crypto from 'node:crypto';
const dir = '/data/ingress-sessions';
fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
const enabled = process.env.REMEMBER_INGRESS_USERS === 'true';
const reported = new Set();
const validationCache = new Map();
console.log(`Portainer ingress session storage ${enabled ? 'enabled' : 'disabled'}`);
console.log(`Portainer ingress session files at startup: ${fs.readdirSync(dir).filter((name) => name.endsWith('.json')).length}`);
function file(req) {
  const user = req.headers['x-remote-user-id'] || req.headers['x-remote-user-name'];
  if (!user) return null;
  return `${dir}/${crypto.createHash('sha256').update(String(user)).digest('hex')}.json`;
}
function tokenExpiry(jwt) {
  try {
    const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64url'));
    return typeof payload.exp === 'number' ? payload.exp * 1000 : null;
  } catch { return null; }
}
function tokenExpired(jwt) {
  const expiry = tokenExpiry(jwt);
  return expiry !== null && expiry <= Date.now();
}
function validateWithPortainer(credential, kind = 'jwt', useCache = true) {
  const cacheKey = `${kind}:${credential}`;
  const cached = validationCache.get(cacheKey);
  if (useCache && cached && cached.until > Date.now()) return Promise.resolve(cached.status);
  return new Promise((resolve) => {
    const request = http.request({
      hostname: '127.0.0.1', port: 9000, path: '/api/users/me', method: 'GET',
      headers: kind === 'apiKey' ? { 'X-API-Key': credential } : { Authorization: `Bearer ${credential}` }, timeout: 5000,
    }, (response) => {
      response.resume();
      const status = response.statusCode || 0;
      validationCache.set(cacheKey, { status, until: Date.now() + 5000 });
      if (validationCache.size > 32) validationCache.delete(validationCache.keys().next().value);
      resolve(status);
    });
    request.on('timeout', () => request.destroy(new Error('timeout')));
    request.on('error', () => resolve(0));
    request.end();
  });
}
http.createServer(async (req, res) => {
  const target = file(req);
  if (req.url === '/auth') {
    let authorization = String(req.headers['x-original-authorization'] || '');
    let jwt = '';
    let apiKey = '';
    if (enabled && target) {
      try {
        const stored = JSON.parse(fs.readFileSync(target));
        if (typeof stored.apiKey === 'string' && stored.apiKey.length <= 8192) {
          const status = await validateWithPortainer(stored.apiKey, 'apiKey');
          if (status === 200) {
            apiKey = stored.apiKey;
            authorization = '';
          }
          else if (status === 401 || status === 403) {
            fs.rmSync(target, { force: true });
            console.log(`Portainer ingress invalidated stale access token (HTTP ${status})`);
          }
        } else if (typeof stored.jwt === 'string' && stored.jwt.length <= 8192) {
          if (tokenExpired(stored.jwt)) {
            fs.rmSync(target, { force: true });
          } else {
            const status = await validateWithPortainer(stored.jwt);
            if (status === 200) {
              jwt = stored.jwt;
              authorization = `Bearer ${jwt}`;
            } else if (status === 401 || status === 403) {
              fs.rmSync(target, { force: true });
              console.log(`Portainer ingress invalidated stale session (HTTP ${status})`);
            }
          }
        }
      } catch {}
    }
    if (authorization) res.setHeader('X-Portainer-Authorization', authorization);
    if (apiKey) res.setHeader('X-Portainer-API-Key', apiKey);
    if (jwt) res.setHeader('X-Portainer-Cookie', `portainer_api_key=${jwt}`);
    const reportKey = target || 'no-user';
    if (!reported.has(reportKey)) {
      reported.add(reportKey);
      let expiry = 'unknown';
      if (jwt) {
        try {
          const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64url'));
          expiry = typeof payload.exp === 'number'
            ? (payload.exp * 1000 <= Date.now() ? 'expired' : new Date(payload.exp * 1000).toISOString())
            : 'not present';
        } catch {}
      }
      console.log(`Portainer ingress restore ${apiKey ? 'found (persistent access token)' : jwt ? 'found (temporary JWT)' : 'missing'}; expiry=${apiKey ? 'persistent' : expiry}`);
    }
    res.statusCode = 204;
    res.end();
    return;
  }
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store');
  if (!enabled) { res.end(JSON.stringify({ enabled: false, reason: 'disabled' })); return; }
  if (!target) {
    res.statusCode = 401;
    console.warn('Portainer ingress session request has no Home Assistant user header');
    res.end(JSON.stringify({ enabled: true, ok: false, reason: 'missing Home Assistant user header' }));
    return;
  }
  if (req.method === 'GET') {
    try {
      const stored = JSON.parse(fs.readFileSync(target));
      if (typeof stored.apiKey === 'string' && await validateWithPortainer(stored.apiKey, 'apiKey') === 200) {
        console.log('Portainer ingress persistent access token loaded for a Home Assistant user');
        res.end(JSON.stringify({ enabled: true, persistent: true }));
      } else if (typeof stored.jwt !== 'string' || tokenExpired(stored.jwt)) {
        fs.rmSync(target, { force: true });
        console.log(`Portainer ingress session load rejected (${typeof stored.jwt === 'string' ? 'expired' : 'invalid'})`);
        res.end(JSON.stringify({ enabled: true }));
      } else if (await validateWithPortainer(stored.jwt) === 200) {
        console.log('Portainer ingress session loaded for a Home Assistant user');
        res.end(JSON.stringify({ enabled: true, ...stored }));
      } else {
        fs.rmSync(target, { force: true });
        console.log('Portainer ingress session load rejected (token rejected by Portainer)');
        res.end(JSON.stringify({ enabled: true }));
      }
    }
    catch (error) {
      console.log(`Portainer ingress session load missing (${error && error.code === 'ENOENT' ? 'file not found' : 'unreadable file'})`);
      res.end(JSON.stringify({ enabled: true }));
    }
    return;
  }
  if (req.method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { if (body.length < 16384) body += chunk; });
    req.on('end', async () => {
      try {
        const parsed = JSON.parse(body);
        const kind = typeof parsed.apiKey === 'string' ? 'apiKey' : 'jwt';
        const credential = kind === 'apiKey' ? parsed.apiKey : parsed.jwt;
        if (typeof credential !== 'string' || credential.length > 8192) throw new Error();
        if (kind === 'jwt' && tokenExpired(credential)) {
          fs.rmSync(target, { force: true });
          res.statusCode = 400;
          res.end('{"ok":false,"reason":"expired token"}');
          return;
        }
        const validationStatus = await validateWithPortainer(credential, kind, false);
        console.log(`Portainer ingress token candidate validation: HTTP ${validationStatus || 'unavailable'}`);
        if (validationStatus !== 200) {
          res.statusCode = 400;
          res.end('{"ok":false,"reason":"token rejected by Portainer"}');
          return;
        }
        const temporary = `${target}.tmp`;
        const descriptor = fs.openSync(temporary, 'w', 0o600);
        try {
          fs.writeFileSync(descriptor, JSON.stringify(kind === 'apiKey' ? { apiKey: credential } : { jwt: credential }));
          fs.fsyncSync(descriptor);
        } finally { fs.closeSync(descriptor); }
        fs.renameSync(temporary, target);
        const directoryDescriptor = fs.openSync(dir, 'r');
        try { fs.fsyncSync(directoryDescriptor); }
        finally { fs.closeSync(directoryDescriptor); }
        console.log(`Stored Portainer ingress ${kind === 'apiKey' ? 'persistent access token' : 'temporary session'} for a Home Assistant user`);
        res.end('{"ok":true}');
      } catch { res.statusCode = 400; res.end('{"ok":false,"reason":"invalid token payload"}'); }
    });
    return;
  }
  res.statusCode = 405; res.end('{}');
}).listen(1338, '127.0.0.1');
