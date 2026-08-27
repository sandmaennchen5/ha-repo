import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const cookieName = 'drydock.sid';
const runtime = fs.readFileSync(new URL('./runtime.js', import.meta.url));
const roots = 'assets|fonts';
const literalPaths = new RegExp('(["\'`])/(?!/)(?=(?:' + roots + ')(?:[/?#"\'`]|$))', 'g');
const trustedPeers = new Set(['172.30.32.2', '::ffff:172.30.32.2']);

export function rewriteText(text, prefix, type) {
  text = text.replace(literalPaths, `$1${prefix}/`);
  if (/javascript/.test(type)) text = text.replace(/return\s*(["'`])\/\1\s*\+/g, `return ${JSON.stringify(prefix + '/')}+`);
  if (type.includes('text/html')) {
    text = text.replace(/(\b(?:href|src|action)=(["']))\/(?!\/|api\/hassio_ingress\/)/gi, `$1${prefix}/`);
    text = text.replace(/<head([^>]*)>/i, `<head$1><script src="${prefix}/__drydock_ingress.js"></script>`);
  }
  if (type.includes('text/css')) text = text.replace(/url\((['"]?)\/(?!\/|api\/hassio_ingress\/)/g, `url($1${prefix}/`);
  return text;
}

export function createIngressProxy({ backendPort = 3000, remember = false, sessionDirectory = '/data/ingress-sessions', allowedPeers = trustedPeers } = {}) {
  fs.mkdirSync(sessionDirectory, { recursive: true, mode: 0o700 });
  fs.chmodSync(sessionDirectory, 0o700);
  if (!remember) for (const name of fs.readdirSync(sessionDirectory)) {
    if (/^[a-f0-9]{64}\.json$/.test(name)) fs.rmSync(path.join(sessionDirectory, name));
  }

  function context(req) {
    if (!allowedPeers.has(req.socket.remoteAddress)) return null;
    const raw = req.headers['x-ingress-path'];
    if (typeof raw !== 'string' || !/^\/api\/hassio_ingress\/[A-Za-z0-9_-]+\/?$/.test(raw)) return null;
    const user = req.headers['x-remote-user-id'];
    // Identity is mandatory: never fall back to a shared browser session.
    if (typeof user !== 'string' || !user.trim()) return null;
    const key = crypto.createHash('sha256').update(user).digest('hex');
    const prefix = raw.replace(/\/$/, '');
    const url = req.url.startsWith(prefix + '/') ? req.url.slice(prefix.length) : req.url;
    if (!url.startsWith('/') || url.startsWith('//')) return null;
    return { prefix, url, file: path.join(sessionDirectory, `${key}.json`), browserName: `${cookieName}_${key.slice(0, 24)}` };
  }

  function saved(ctx) {
    if (!remember) return '';
    try {
      const session = JSON.parse(fs.readFileSync(ctx.file, 'utf8'));
      if (session.expires > Date.now() && /^[A-Za-z0-9_%+.=:\/-]+$/.test(session.value)) return session.value;
      fs.unlinkSync(ctx.file);
    } catch { /* no valid stored session */ }
    return '';
  }

  function requestHeaders(req, ctx) {
    const headers = { ...req.headers, 'accept-encoding': 'identity' };
    const cookies = (headers.cookie ?? '').split(';').map(c => c.trim()).filter(Boolean);
    const browser = cookies.find(c => c.startsWith(ctx.browserName + '='))?.slice(ctx.browserName.length + 1);
    const value = (remember && saved(ctx)) || browser;
    // Drop every Drydock session cookie before adding the current HA user's session.
    headers.cookie = cookies.filter(c => !c.startsWith(cookieName + '=') && !c.startsWith(cookieName + '_')).join('; ');
    if (value && /^[A-Za-z0-9_%+.=:\/-]+$/.test(value)) headers.cookie += `${headers.cookie ? '; ' : ''}${cookieName}=${value}`;
    delete headers['x-remote-user-id'];
    delete headers['x-remote-user-name'];
    delete headers['x-ingress-path'];
    return headers;
  }

  function responseHeaders(headers, ctx) {
    headers = { ...headers, 'x-accel-buffering': 'no' };
    if (headers.location?.startsWith('/') && !headers.location.startsWith('//') && !headers.location.startsWith(ctx.prefix + '/')) headers.location = ctx.prefix + headers.location;
    if (headers.link) headers.link = headers.link.replace(/<\/(?!\/)/g, `<${ctx.prefix}/`);
    if (headers['set-cookie']) headers['set-cookie'] = headers['set-cookie'].map(cookie => {
      if (cookie.startsWith(cookieName + '=')) {
        const value = cookie.split(';', 1)[0].slice(cookieName.length + 1);
        const age = /;\s*max-age=(-?\d+)/i.exec(cookie);
        const expiresText = /;\s*expires=([^;]+)/i.exec(cookie);
        const expires = age ? Date.now() + Number(age[1]) * 1000 : Date.parse(expiresText?.[1] ?? '');
        if (remember) {
          if (ctx.url.split('?')[0] !== '/auth/logout' && value && /^[A-Za-z0-9_%+.=:\/-]+$/.test(value) && Number.isFinite(expires) && expires > Date.now()) {
            const temp = `${ctx.file}.${crypto.randomBytes(8).toString('hex')}.tmp`;
            fs.writeFileSync(temp, JSON.stringify({ value, expires }), { mode: 0o600 });
            fs.renameSync(temp, ctx.file);
          } else fs.rmSync(ctx.file, { force: true });
        }
        cookie = ctx.browserName + cookie.slice(cookieName.length);
      }
      return cookie.replace(/;\s*domain=[^;]*/ig, '').replace(/;\s*path=[^;]*/i, `; Path=${ctx.prefix}/`);
    });
    return headers;
  }

  const server = http.createServer((req, res) => {
    const ctx = context(req);
    if (!ctx) { res.writeHead(403); res.end('Home Assistant Ingress required'); return; }
    if (ctx.url === '/__drydock_ingress.js') {
      res.writeHead(200, { 'content-type': 'application/javascript', 'cache-control': 'no-store' });
      res.end(runtime); return;
    }
    const headersToBackend = requestHeaders(req, ctx);
    if (ctx.url.split('?')[0] === '/auth/logout') fs.rmSync(ctx.file, { force: true });
    const upstream = http.request({ hostname: '127.0.0.1', port: backendPort, path: ctx.url, method: req.method, headers: headersToBackend }, response => {
      let headers;
      try { headers = responseHeaders(response.headers, ctx); }
      catch { response.destroy(); res.writeHead(502); res.end('Ingress session storage failed'); return; }
      const type = headers['content-type'] ?? '';
      const transform = /text\/html|(?:application|text)\/javascript|text\/css/.test(type) && !headers['content-encoding'];
      if (!transform) { res.writeHead(response.statusCode, headers); response.pipe(res); return; }
      const chunks = [];
      let size = 0;
      response.on('data', chunk => {
        size += chunk.length;
        if (size > 16 * 1024 * 1024) { response.destroy(); res.destroy(); return; }
        chunks.push(chunk);
      });
      response.on('end', () => {
        const body = rewriteText(Buffer.concat(chunks).toString('utf8'), ctx.prefix, type);
        delete headers['content-length']; delete headers.etag;
        headers['cache-control'] = 'no-store';
        res.writeHead(response.statusCode, headers); res.end(body);
      });
      response.on('error', () => res.destroy());
    });
    upstream.on('error', () => { if (!res.headersSent) res.writeHead(502); res.end('Drydock backend unavailable'); });
    req.on('aborted', () => upstream.destroy());
    res.on('close', () => upstream.destroy());
    req.pipe(upstream);
  });

  server.on('upgrade', (req, socket, head) => {
    const ctx = context(req);
    if (!ctx) { socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n'); return; }
    const upstream = http.request({ hostname: '127.0.0.1', port: backendPort, path: ctx.url, method: 'GET', headers: requestHeaders(req, ctx) });
    upstream.on('upgrade', (response, backend, backendHead) => {
      socket.write(`HTTP/1.1 ${response.statusCode} ${response.statusMessage}\r\n` + Object.entries(response.headers).map(([key, value]) => `${key}: ${value}\r\n`).join('') + '\r\n');
      if (backendHead.length) socket.write(backendHead);
      if (head.length) backend.write(head);
      socket.pipe(backend); backend.pipe(socket);
      socket.on('error', () => backend.destroy()); backend.on('error', () => socket.destroy());
      socket.on('close', () => backend.destroy()); backend.on('close', () => socket.destroy());
    });
    upstream.on('response', response => { socket.end(`HTTP/1.1 ${response.statusCode} Rejected\r\nConnection: close\r\n\r\n`); response.resume(); });
    upstream.on('error', () => socket.destroy());
    socket.on('error', () => upstream.destroy());
    upstream.end();
  });
  return server;
}
