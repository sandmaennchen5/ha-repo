import { createRequire } from 'node:module';
import { withHawserComposeTimeout } from './hawser-timeout.mjs';

// Resolve the dependency supplied by the upstream Dockhand image.
const require = createRequire('/app/package.json');
const { getGlobalDispatcher } = require('undici');
const timeoutMs = Number(process.env.COMPOSE_TIMEOUT || 900) * 1000;
globalThis.fetch = withHawserComposeTimeout(globalThis.fetch, getGlobalDispatcher, timeoutMs);
