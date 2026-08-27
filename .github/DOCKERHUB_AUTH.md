# Optional Docker Hub authentication for Update Apps

The updater first queries Docker Hub anonymously. If Docker Hub returns HTTP
401 or 403 and both repository Actions secrets are configured, it obtains a
short-lived access token and retries the request once with authentication:

- `DOCKERHUB_USERNAME`: Docker Hub account name.
- `DOCKERHUB_TOKEN`: Docker Hub personal access token (read-only access is enough
  for reading image metadata). Do not use the account password.

Configure these under repository **Settings → Secrets and variables → Actions**.
Both are optional. Missing or incomplete credentials leave anonymous behavior
unchanged. A denied authenticated request remains a visible per-app failure;
other apps continue. Credentials and token responses are never printed.

The updater reads the configured tracking tag directly, then scans recent tag
pages until it finds a numeric version sharing a manifest or platform digest.
It does not silently choose an unrelated version when a channel match is missing.
This normally avoids Docker Hub's anonymous pagination limit.

The login uses Docker Hub's documented `POST /v2/auth/token` endpoint with
`identifier` and `secret`, followed by a Bearer access token.

Reference: [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/).

These secrets are only used by the updater, not passed to app containers or
Docker image builds. They are unrelated to the GHCR publishing credentials.
