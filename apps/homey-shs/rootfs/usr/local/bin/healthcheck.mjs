import http from 'node:http';

const request = http.get('http://127.0.0.1:4859/', (response) => {
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
