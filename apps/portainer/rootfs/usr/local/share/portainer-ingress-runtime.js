(function () {
  // Do not resolve this against Portainer's <base href="/">. Under Home
  // Assistant ingress that would incorrectly address HA's document root.
  const ingress = location.pathname.match(/^\/api\/hassio_ingress\/[^/]+\//);
  const endpoint = ingress ? `${ingress[0]}__portainer_ingress_session` : '/__portainer_ingress_session';
  console.info('Portainer ingress session runtime loaded');
  const keys = ['portainer.JWT', 'JWT', 'jwt', 'portainer-session'];
  const authUrl = /(?:^|\/)api\/auth(?:\/|\?|$)/;
  let restoring = false;
  let lastPersisted = '';
  let restoredJwt = '';
  let sessionStored = false;
  let loginPassword = '';
  const nativeFetch = window.fetch.bind(window);
  // Home Assistant forbids synchronous requests inside ingress. Keep
  // Portainer's initial API calls waiting until this lookup has completed.
  const sessionReady = nativeFetch(endpoint, { credentials: 'same-origin', cache: 'no-store' })
    .then((response) => response.ok ? response.json() : null)
    .then((session) => {
      const cookiePath = ingress ? ingress[0] : '/';
      if (session && typeof session.jwt === 'string') {
        restoredJwt = session.jwt;
        sessionStored = true;
        // This cookie is scoped to the current random HA ingress path. The
        // durable token remains in the per-user server-side session file.
        document.cookie = `portainer_api_key=${encodeURIComponent(restoredJwt)}; Path=${cookiePath}; SameSite=Strict`;
        console.info('Portainer ingress session restored');
      } else {
        document.cookie = `portainer_api_key=; Path=${cookiePath}; Max-Age=0; SameSite=Strict`;
        if (session && session.persistent) {
          for (const storage of [localStorage, sessionStorage]) {
            for (const key of keys) storage.removeItem(key);
          }
        }
      }
      return session;
    })
    .catch(() => null);

  function jwtFrom(value) {
    if (typeof value !== 'string' || value.length === 0) return null;
    try {
      const parsed = JSON.parse(value);
      if (typeof parsed === 'string') return parsed;
      return parsed && typeof parsed.jwt === 'string' ? parsed.jwt : null;
    } catch {
      return value.split('.').length === 3 ? value : null;
    }
  }

  function jwtExpired(jwt) {
    try {
      const payload = JSON.parse(atob(jwt.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
      return typeof payload.exp === 'number' && payload.exp * 1000 <= Date.now();
    } catch { return false; }
  }

  function persist(jwt) {
    if (typeof jwt !== 'string' || !jwt || jwtExpired(jwt) || jwt === lastPersisted) return;
    lastPersisted = jwt;
    window.fetch(endpoint, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({jwt})
    }).then((response) => {
      if (!response.ok) throw new Error(`session store returned ${response.status}`);
      return response.json();
    }).then((result) => {
      if (!result.ok) throw new Error(result.reason || 'session was not stored');
      sessionStored = true;
    }).catch((error) => {
      lastPersisted = '';
      console.warn('Portainer ingress session could not be stored:', error.message);
    });
  }

  function persistApiKey(apiKey) {
    if (typeof apiKey !== 'string' || !apiKey) return;
    window.fetch(endpoint, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({apiKey})
    }).then((response) => {
      if (!response.ok) throw new Error(`access token store returned ${response.status}`);
      sessionStored = true;
      console.info('Portainer ingress persistent access token stored');
    }).catch((error) => console.warn('Portainer ingress access token could not be stored:', error.message));
  }

  async function createPersistentAccessToken(password) {
    if (!password) return;
    try {
      const prefix = ingress ? ingress[0] : '/';
      const meResponse = await nativeFetch(`${prefix}api/users/me`, { credentials: 'same-origin', cache: 'no-store' });
      if (!meResponse.ok) throw new Error(`current user returned ${meResponse.status}`);
      const user = await meResponse.json();
      const tokenResponse = await nativeFetch(`${prefix}api/users/${user.Id || user.id}/tokens`, {
        method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ password, description: 'Home Assistant ingress' })
      });
      if (!tokenResponse.ok) throw new Error(`access token creation returned ${tokenResponse.status}`);
      const token = await tokenResponse.json();
      persistApiKey(token.rawAPIKey);
    } catch (error) {
      console.warn('Portainer ingress persistent access token could not be created:', error.message);
    } finally {
      loginPassword = '';
    }
  }

  function rememberLoginPassword(body) {
    try {
      const parsed = typeof body === 'string' ? JSON.parse(body) : body;
      if (parsed && typeof parsed.password === 'string') loginPassword = parsed.password;
    } catch {}
  }

  function capture(body) {
    if (body && typeof body.jwt === 'string') persist(body.jwt);
  }

  function captureResponseSession(response) {
    const session = response.headers.get('X-Portainer-Ingress-Session');
    if (session) persist(session);
  }

  function scanStorage() {
    if (sessionStored) return;
    for (const storage of [localStorage, sessionStorage]) {
      for (const key of keys) {
        const jwt = jwtFrom(storage.getItem(key));
        if (jwt && jwtExpired(jwt)) {
          storage.removeItem(key);
          continue;
        }
        if (jwt) return persist(jwt);
      }
    }
  }

  sessionReady
    .then((s) => {
      if (!s || !s.enabled || !s.jwt) return;
      restoredJwt = s.jwt;
      if (!keys.some((k) => localStorage.getItem(k) === s.jwt)) {
        keys.forEach((k) => localStorage.setItem(k, s.jwt));
        if (!sessionStorage.getItem('portainer-ingress-restored')) {
          sessionStorage.setItem('portainer-ingress-restored', '1');
          restoring = true;
          location.reload();
        }
      }
    }).catch(() => {});
  const originalFetch = nativeFetch;
  window.fetch = async function (...args) {
    const url = String(args[0] && args[0].url ? args[0].url : args[0]);
    if (/api\//.test(url) && !authUrl.test(url)) await sessionReady;
    if (restoredJwt && /api\//.test(url) && !authUrl.test(url)) {
      const init = {...(args[1] || {})};
      const headers = new Headers(init.headers || (args[0] instanceof Request ? args[0].headers : undefined));
      headers.set('X-Portainer-Ingress-JWT', restoredJwt);
      init.headers = headers;
      args[1] = init;
    }
    const response = await originalFetch(...args);
    if (!restoring && authUrl.test(url) && response.ok) {
      rememberLoginPassword(args[1] && args[1].body);
      captureResponseSession(response);
      response.clone().json().then(capture).catch(() => {});
      setTimeout(() => createPersistentAccessToken(loginPassword), 0);
    }
    return response;
  };

  const originalOpen = XMLHttpRequest.prototype.open;
  const originalSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    const loginRequest = authUrl.test(String(url));
    this.__portainerRestoreAuth = Boolean(/\/api\//.test(String(url)) && !loginRequest);
    if (loginRequest) {
      this.addEventListener('load', () => {
        if (this.status < 200 || this.status >= 300) return;
        try {
          const session = this.getResponseHeader('X-Portainer-Ingress-Session');
          if (session) persist(session);
          capture(this.responseType === 'json' ? this.response : JSON.parse(this.responseText));
        } catch {}
        setTimeout(() => createPersistentAccessToken(loginPassword), 0);
      }, { once: true });
    }
    return originalOpen.call(this, method, url, ...rest);
  };
  XMLHttpRequest.prototype.send = function (...args) {
    if (!this.__portainerRestoreAuth) {
      rememberLoginPassword(args[0]);
    }
    if (!this.__portainerRestoreAuth) return originalSend.apply(this, args);
    const request = this;
    sessionReady.finally(() => {
      if (restoredJwt) {
        try { request.setRequestHeader('X-Portainer-Ingress-JWT', restoredJwt); } catch {}
      }
      originalSend.apply(request, args);
    });
  };

  window.addEventListener('storage', scanStorage);
  setInterval(scanStorage, 1000);
  scanStorage();
})();
