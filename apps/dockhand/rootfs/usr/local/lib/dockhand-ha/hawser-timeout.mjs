// Override Undici's independent 300-second limits only for Hawser stack requests.
// Delegate to the active dispatcher to retain Dockhand's DNS, proxy and TLS setup.
export function withHawserComposeTimeout(fetch, getDispatcher, timeoutMs) {
  if (!Number.isSafeInteger(timeoutMs) || timeoutMs <= 0) {
    throw new Error('COMPOSE_TIMEOUT must be a positive whole number of seconds');
  }
  return function(input, init) {
    const url = new URL(input instanceof Request ? input.url : String(input));
    const method = String(init?.method ?? (input instanceof Request ? input.method : 'GET')).toUpperCase();
    if (method !== 'POST' || url.pathname !== '/_hawser/compose') {
      return fetch(input, init);
    }
    return fetch(input, {
      ...init,
      dispatcher: {
        dispatch(options, handler) {
          const dispatcher = init?.dispatcher ?? getDispatcher();
          return dispatcher.dispatch({
            ...options, headersTimeout: timeoutMs, bodyTimeout: timeoutMs
          }, handler);
        }
      }
    });
  };
}
