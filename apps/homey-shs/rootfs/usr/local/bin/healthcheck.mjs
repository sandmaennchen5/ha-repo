import http from 'node:http';
import fs from 'node:fs';

let port = process.env.PORT_SERVER_HTTP ?? '4859';

try {
  const options = JSON.parse(fs.readFileSync('/data/options.json', 'utf8'));
  port = String(options.port_server_http ?? port);
} catch {
  // Keep the environment/default port if the options file is unavailable.
}

const request = http.get(`http://127.0.0.1:${port}/`, (response) => {
  response.resume();
  process.exit(response.statusCode < 500 ? 0 : 1);
});

request.setTimeout(8000, () => {
  request.destroy();
  process.exit(1);
});

request.on('error', () => {
  process.exit(1);
});
