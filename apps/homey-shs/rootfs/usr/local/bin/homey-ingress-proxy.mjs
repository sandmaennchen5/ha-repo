import http from "node:http";
import net from "node:net";
import crypto from "node:crypto";
import fs from "node:fs/promises";

const listenPort = 8099;
const targetPort = Number.parseInt(process.env.PORT_SERVER_HTTP ?? "4859", 10);
const targetHost = "127.0.0.1";
const rememberIngressUsers =
  process.env.HOMEY_INGRESS_REMEMBER_USERS === "1";
const sessionDirectory = "/data/ingress-sessions";
const replayUsername = "__home_assistant_ingress_session__";
const recentReplays = new Map();
const allowedRemoteAddresses = new Set([
  "172.30.32.2",
  "::ffff:172.30.32.2",
  "127.0.0.1",
  "::1",
]);

function isAllowed(request) {
  return allowedRemoteAddresses.has(request.socket.remoteAddress ?? "");
}

function homeAssistantUserId(request) {
  const value = request.headers["x-remote-user-id"];
  return typeof value === "string" && value.length > 0 ? value : null;
}

function sessionFile(request) {
  const userId = homeAssistantUserId(request);
  if (!rememberIngressUsers || !userId) return null;
  const digest = crypto.createHash("sha256").update(userId).digest("hex");
  return `${sessionDirectory}/${digest}.json`;
}

function browserStorageNamespace(request) {
  const userId = homeAssistantUserId(request);
  if (!userId) return "anonymous";
  return crypto.createHash("sha256").update(userId).digest("hex").slice(0, 24);
}

async function readSession(request) {
  const file = sessionFile(request);
  if (!file) return null;
  try {
    return JSON.parse(await fs.readFile(file, "utf8"));
  } catch {
    return null;
  }
}

async function writeSession(request, statusCode, headers, body) {
  const file = sessionFile(request);
  if (!file) return;
  await fs.mkdir(sessionDirectory, { recursive: true, mode: 0o700 });
  const temporary = `${file}.${process.pid}.tmp`;
  const record = {
    format: 1,
    statusCode,
    contentType: String(headers["content-type"] ?? "application/json"),
    setCookie: headers["set-cookie"] ?? [],
    body: body.toString("base64"),
    createdAt: new Date().toISOString(),
  };
  await fs.writeFile(temporary, JSON.stringify(record), { mode: 0o600 });
  await fs.rename(temporary, file);
}

async function deleteSession(request) {
  const file = sessionFile(request);
  if (!file) return;
  await fs.rm(file, { force: true });
}

async function readRequestBody(request, limit = 1024 * 1024) {
  const chunks = [];
  let length = 0;
  for await (const chunk of request) {
    length += chunk.length;
    if (length > limit) throw new Error("Request body too large");
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

function isReplayLogin(body) {
  try {
    const value = JSON.parse(body.toString("utf8"));
    return value?.username === replayUsername;
  } catch {
    return false;
  }
}

function ingressPath(request) {
  const value = request.headers["x-ingress-path"];
  if (typeof value !== "string") return "";
  const normalized = `/${value}`.replace(/\/+/g, "/").replace(/\/$/, "");
  return normalized === "/" ? "" : normalized;
}

function upstreamHeaders(request) {
  const headers = { ...request.headers };
  headers.host = `${targetHost}:${targetPort}`;
  headers["accept-encoding"] = "identity";
  delete headers["if-none-match"];
  delete headers["if-modified-since"];

  if (headers.origin) {
    headers.origin = `http://${targetHost}:${targetPort}`;
  }
  if (headers.referer) {
    headers.referer = `http://${targetHost}:${targetPort}/`;
  }

  return headers;
}

function rewriteLocation(value, basePath) {
  if (!basePath || typeof value !== "string") return value;
  try {
    const parsed = new URL(value, `http://${targetHost}:${targetPort}`);
    const isAbsolute = /^[a-z][a-z0-9+.-]*:/i.test(value);
    if (
      parsed.hostname === targetHost ||
      parsed.hostname === "localhost" ||
      !isAbsolute
    ) {
      return `${basePath}${parsed.pathname}${parsed.search}${parsed.hash}`;
    }
  } catch {
    if (value.startsWith("/")) return `${basePath}${value}`;
  }
  return value;
}

function rewriteCookies(values, basePath) {
  if (!basePath || !Array.isArray(values)) return values;
  return values.map((cookie) => {
    if (/;\s*Path=/i.test(cookie)) {
      return cookie.replace(/;\s*Path=([^;]*)/i, (_match, path) => {
        const suffix = path.startsWith("/") ? path : `/${path}`;
        return `; Path=${basePath}${suffix}`;
      });
    }
    return `${cookie}; Path=${basePath}/`;
  });
}

function ingressRuntime(basePath, storageNamespace) {
  return `
(() => {
  const base = ${JSON.stringify(basePath)};
  const storagePrefix = ${JSON.stringify(
    storageNamespace ? `__ha_${storageNamespace}__:` : "",
  )};
  const homeyPort = ${JSON.stringify(String(targetPort))};
  if (storagePrefix) {
    const storageGetItem = Storage.prototype.getItem;
    const storageSetItem = Storage.prototype.setItem;
    const storageRemoveItem = Storage.prototype.removeItem;
    Storage.prototype.getItem = function(key) {
      return storageGetItem.call(this, storagePrefix + key);
    };
    Storage.prototype.setItem = function(key, value) {
      return storageSetItem.call(this, storagePrefix + key, value);
    };
    Storage.prototype.removeItem = function(key) {
      return storageRemoveItem.call(this, storagePrefix + key);
    };
  }
  const realLocation = window.location;
  const strip = (path) => {
    if (path === base) return "/";
    return path.startsWith(base + "/") ? path.slice(base.length) : path;
  };
  const prefix = (value) => {
    if (typeof value !== "string" || value === "") return value;
    try {
      const url = new URL(value, realLocation.href);
      const targetsHomey =
        (
          url.port === homeyPort ||
          url.hostname.endsWith(".homey.homeylocal.com")
        ) &&
        (url.protocol === "http:" ||
          url.protocol === "https:" ||
          url.protocol === "ws:" ||
          url.protocol === "wss:");
      const sameBrowserHost = url.host === realLocation.host;
      if (
        url.origin !== realLocation.origin &&
        !sameBrowserHost &&
        !targetsHomey
      ) return value;
      if (targetsHomey) {
        const websocket =
          url.protocol === "ws:" || url.protocol === "wss:";
        url.protocol = websocket
          ? (realLocation.protocol === "https:" ? "wss:" : "ws:")
          : realLocation.protocol;
        url.host = realLocation.host;
      }
      if (!url.pathname.startsWith(base + "/") && url.pathname !== base) {
        url.pathname = base + (url.pathname.startsWith("/") ? "" : "/") + url.pathname;
      }
      return value.startsWith("http") ? url.href : url.pathname + url.search + url.hash;
    } catch {
      return value;
    }
  };
  const virtualLocation = new Proxy(realLocation, {
    get(target, property) {
      if (property === "pathname") return strip(target.pathname);
      if (property === "href") {
        const url = new URL(target.href);
        url.pathname = strip(url.pathname);
        return url.href;
      }
      if (property === "assign" || property === "replace") {
        return (value) => target[property](prefix(value));
      }
      const value = Reflect.get(target, property);
      return typeof value === "function" ? value.bind(target) : value;
    },
    set(target, property, value) {
      if (property === "href" || property === "pathname") {
        target[property] = prefix(String(value));
        return true;
      }
      return Reflect.set(target, property, value);
    },
  });
  Object.defineProperty(window, "__homeyIngressLocation", {
    value: virtualLocation,
    configurable: false,
    writable: false,
  });
  const pushState = history.pushState.bind(history);
  const replaceState = history.replaceState.bind(history);
  history.pushState = (state, title, url) =>
    pushState(state, title, prefix(url));
  history.replaceState = (state, title, url) =>
    replaceState(state, title, prefix(url));

  const originalFetch = window.fetch.bind(window);
  window.fetch = (input, init) => {
    if (input instanceof Request) {
      return originalFetch(new Request(prefix(input.url), input), init);
    }
    return originalFetch(prefix(input), init);
  };

  const originalOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    return originalOpen.call(this, method, prefix(url), ...rest);
  };

  const originalSetAttribute = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function(name, value) {
    const normalized = String(name).toLowerCase();
    if (
      ["src", "href", "action"].includes(normalized) ||
      normalized.endsWith(":href")
    ) {
      value = prefix(value);
    }
    return originalSetAttribute.call(this, name, value);
  };
  const originalStyleSetProperty = CSSStyleDeclaration.prototype.setProperty;
  CSSStyleDeclaration.prototype.setProperty = function(name, value, priority) {
    if (typeof value === "string" && /url\\(/i.test(value)) {
      value = value.replace(
        /url\\(\\s*(["']?)([^"')]+)\\1\\s*\\)/gi,
        (_match, quote, url) => \`url(\${quote}\${prefix(url)}\${quote})\`,
      );
    }
    return originalStyleSetProperty.call(this, name, value, priority);
  };
  for (const [Prototype, property] of [
    [HTMLImageElement.prototype, "src"],
    [HTMLScriptElement.prototype, "src"],
    [HTMLLinkElement.prototype, "href"],
    [HTMLFormElement.prototype, "action"],
  ]) {
    const descriptor = Object.getOwnPropertyDescriptor(Prototype, property);
    if (!descriptor?.get || !descriptor?.set) continue;
    Object.defineProperty(Prototype, property, {
      configurable: descriptor.configurable,
      enumerable: descriptor.enumerable,
      get: descriptor.get,
      set(value) {
        descriptor.set.call(this, prefix(value));
      },
    });
  }

  const OriginalWebSocket = window.WebSocket;
  window.WebSocket = new Proxy(OriginalWebSocket, {
    construct(Target, args) {
      args[0] = prefix(args[0]);
      return Reflect.construct(Target, args);
    },
  });

  if (window.EventSource) {
    const OriginalEventSource = window.EventSource;
    window.EventSource = new Proxy(OriginalEventSource, {
      construct(Target, args) {
        args[0] = prefix(args[0]);
        return Reflect.construct(Target, args);
      },
    });
  }

  const setReactInput = (input, value) => {
    const setter = Object.getOwnPropertyDescriptor(
      HTMLInputElement.prototype,
      "value",
    )?.set;
    setter?.call(input, value);
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  };
  const tryAutomaticLogin = async () => {
    if (strip(realLocation.pathname) !== "/web/login-local") return;
    const attemptKey = "__homeyIngressLoginAttempt";
    if (sessionStorage.getItem(attemptKey) === "1") return;
    const status = await originalFetch(prefix("/__homey_ingress_session"), {
      cache: "no-store",
    }).then((result) => result.json()).catch(() => ({ available: false }));
    if (!status.available) return;
    const username = document.querySelector(
      'input[name="username"], input[type="text"]',
    );
    const password = document.querySelector(
      'input[name="password"], input[type="password"]',
    );
    const submit = document.querySelector(
      'button[type="submit"], input[type="submit"], form button',
    );
    if (!username || !password || !submit) return false;
    sessionStorage.setItem(attemptKey, "1");
    setReactInput(username, ${JSON.stringify(replayUsername)});
    setReactInput(password, crypto.randomUUID());
    submit.click();
    return true;
  };
  let loginAttempts = 0;
  const loginTimer = setInterval(async () => {
    loginAttempts += 1;
    if ((await tryAutomaticLogin()) || loginAttempts >= 100) {
      clearInterval(loginTimer);
    }
  }, 100);
})();
`;
}

function rewriteText(body, contentType, basePath) {
  if (!basePath) return body;
  let text = body.toString("utf8");

  if (contentType.includes("text/html")) {
    const runtime =
      `<script src="/__homey_ingress_runtime.js"></script>`;
    text = text
      .replace(
        /<(head)([^>]*)>/i,
        `<$1$2>${runtime}`,
      )
      .replace(
        /\b(href|src|action)=(["'])\/(?!\/)/gi,
        `$1=$2${basePath}/`,
      );
  } else if (contentType.includes("javascript")) {
    text = text
      .replace(
        /\b(?:window|document)\.location\b/g,
        "window.__homeyIngressLocation",
      )
      .replace(
        /(["'`(])\/(socket\.io|web\/assets|web\/img|fonts|api|app)\//g,
        `$1${basePath}/$2/`,
      );
  } else if (contentType.includes("text/css")) {
    text = text.replace(
      /url\(\s*(["']?)\/(?!\/)/gi,
      `url($1${basePath}/`,
    );
  }

  return Buffer.from(text);
}

const server = http.createServer(async (request, response) => {
  if (!isAllowed(request)) {
    response.writeHead(403, { "content-type": "text/plain; charset=utf-8" });
    response.end("Forbidden");
    return;
  }

  if (request.url === "/__health") {
    const socket = net.createConnection({ host: targetHost, port: targetPort });
    let completed = false;
    const finish = (statusCode, body) => {
      if (completed) return;
      completed = true;
      socket.destroy();
      response.writeHead(statusCode, {
        "content-type": "text/plain; charset=utf-8",
        "content-length": Buffer.byteLength(body),
        "cache-control": "no-store",
      });
      response.end(body);
    };
    socket.setTimeout(3000);
    socket.once("connect", () => finish(200, "OK\n"));
    socket.once("timeout", () => finish(503, "Homey unavailable\n"));
    socket.once("error", () => finish(503, "Homey unavailable\n"));
    return;
  }

  const basePath = ingressPath(request);
  if (request.url === "/__homey_ingress_session") {
    const record = await readSession(request);
    const body = Buffer.from(JSON.stringify({
      enabled: rememberIngressUsers,
      available: record !== null,
    }));
    response.writeHead(200, {
      "content-type": "application/json; charset=utf-8",
      "content-length": String(body.length),
      "cache-control": "no-store",
    });
    response.end(body);
    return;
  }

  if (
    request.url === "/__homey_ingress_forget_session" &&
    request.method === "POST"
  ) {
    await deleteSession(request);
    response.writeHead(204, { "cache-control": "no-store" });
    response.end();
    return;
  }

  if (request.url === "/__homey_ingress_runtime.js") {
    const body = Buffer.from(
      ingressRuntime(
        basePath,
        rememberIngressUsers ? browserStorageNamespace(request) : null,
      ),
    );
    response.writeHead(200, {
      "content-type": "application/javascript; charset=utf-8",
      "content-length": String(body.length),
      "cache-control": "no-store",
    });
    response.end(body);
    return;
  }

  const isLoginRequest =
    [
      "/api/manager/users/login-local",
      "/web/login-local",
    ].includes(request.url) &&
    request.method === "POST";
  let requestBody = null;
  if (isLoginRequest) {
    try {
      requestBody = await readRequestBody(request);
    } catch (error) {
      response.writeHead(413, { "content-type": "text/plain; charset=utf-8" });
      response.end(error.message);
      return;
    }
  }

  if (requestBody && isReplayLogin(requestBody)) {
    const record = await readSession(request);
    if (!record) {
      response.writeHead(401, {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store",
      });
      response.end('{"error":"Stored Homey session unavailable"}');
      return;
    }
    const body = Buffer.from(record.body, "base64");
    const headers = {
      "content-type": record.contentType,
      "content-length": String(body.length),
      "cache-control": "no-store",
    };
    if (record.setCookie?.length) {
      headers["set-cookie"] = rewriteCookies(record.setCookie, basePath);
    }
    recentReplays.set(sessionFile(request), Date.now());
    response.writeHead(record.statusCode ?? 200, headers);
    response.end(body);
    return;
  }

  const proxyRequest = http.request(
    {
      host: targetHost,
      port: targetPort,
      method: request.method,
      path: request.url,
      headers: upstreamHeaders(request),
    },
    (proxyResponse) => {
      const headers = { ...proxyResponse.headers };
      const originalSetCookie = headers["set-cookie"] ?? [];
      if (headers.location) {
        headers.location = rewriteLocation(headers.location, basePath);
      }
      if (headers["set-cookie"]) {
        headers["set-cookie"] = rewriteCookies(headers["set-cookie"], basePath);
      }

      const contentType = String(headers["content-type"] ?? "");
      const shouldRewrite =
        contentType.includes("text/html") ||
        contentType.includes("javascript") ||
        contentType.includes("text/css");
      const shouldCaptureLogin =
        isLoginRequest &&
        (proxyResponse.statusCode ?? 500) >= 200 &&
        (proxyResponse.statusCode ?? 500) < 300 &&
        sessionFile(request) !== null;

      if (
        request.url === "/api/manager/sessions/session/me" &&
        [401, 403].includes(proxyResponse.statusCode ?? 0) &&
        Date.now() - (recentReplays.get(sessionFile(request)) ?? 0) < 30000
      ) {
        recentReplays.delete(sessionFile(request));
        deleteSession(request).catch((error) =>
          console.error("Unable to remove expired ingress session:", error),
        );
      } else if (
        request.url === "/api/manager/sessions/session/me" &&
        (proxyResponse.statusCode ?? 500) >= 200 &&
        (proxyResponse.statusCode ?? 500) < 300
      ) {
        recentReplays.delete(sessionFile(request));
      }

      if (!shouldRewrite && !shouldCaptureLogin) {
        response.writeHead(proxyResponse.statusCode ?? 502, headers);
        proxyResponse.pipe(response);
        return;
      }

      headers["cache-control"] = "no-store";
      delete headers.etag;
      delete headers["last-modified"];
      const chunks = [];
      proxyResponse.on("data", (chunk) => chunks.push(chunk));
      proxyResponse.on("end", () => {
        const upstreamBody = Buffer.concat(chunks);
        if (shouldCaptureLogin) {
          writeSession(
            request,
            proxyResponse.statusCode ?? 200,
            { ...headers, "set-cookie": originalSetCookie },
            upstreamBody,
          ).catch((error) =>
            console.error("Unable to remember ingress session:", error),
          );
        }
        const body = shouldRewrite
          ? rewriteText(upstreamBody, contentType, basePath)
          : upstreamBody;
        delete headers["transfer-encoding"];
        headers["content-length"] = String(body.length);
        response.writeHead(proxyResponse.statusCode ?? 502, headers);
        response.end(body);
      });
    },
  );

  proxyRequest.on("error", (error) => {
    if (!response.headersSent) {
      response.writeHead(502, { "content-type": "text/plain; charset=utf-8" });
    }
    response.end(`Homey upstream unavailable: ${error.message}`);
  });
  if (requestBody) {
    proxyRequest.end(requestBody);
  } else {
    request.pipe(proxyRequest);
  }
});

server.on("upgrade", (request, socket, head) => {
  if (!isAllowed(request)) {
    socket.end("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n");
    return;
  }

  const upstream = net.connect(targetPort, targetHost, () => {
    const headers = upstreamHeaders(request);
    const lines = [`${request.method} ${request.url} HTTP/${request.httpVersion}`];
    for (const [name, value] of Object.entries(headers)) {
      if (Array.isArray(value)) {
        for (const item of value) lines.push(`${name}: ${item}`);
      } else if (value !== undefined) {
        lines.push(`${name}: ${value}`);
      }
    }
    upstream.write(`${lines.join("\r\n")}\r\n\r\n`);
    if (head.length) upstream.write(head);
    socket.pipe(upstream).pipe(socket);
  });

  upstream.on("error", () => socket.destroy());
  socket.on("error", () => upstream.destroy());
});

server.listen(listenPort, "0.0.0.0", () => {
  console.log(
    `Homey ingress proxy listening on ${listenPort}, forwarding to ${targetHost}:${targetPort}`,
  );
});

function shutdown() {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 5000).unref();
}

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
