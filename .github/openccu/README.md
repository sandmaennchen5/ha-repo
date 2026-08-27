# OpenCCU original tracking with login overlay

The update feed is **OpenCCU/OpenCCU**, not the fork. `sync_openccu.py`
reads the four original app configurations at a single resolved master commit.
Stable resolves the release source, snapshot its build commit; proxy and helper
track their own app versions. Every original multi-architecture image is pinned
by digest. Original entrypoints, libraries, hardware permissions and mounts remain.

## Reviewed patch provenance

- Fork: https://github.com/sandmaennchen5/fork_OpenCCU/tree/ingress-loginsave
- Fixed patch commit: `4a84f7aa7c69ac93685080a02f40832fc63fcbfa`
- Modern baseline: OpenCCU `acf6acfd90dba9351b06fee2ccd314fbcc54b546`
- Stable backport baseline: OpenCCU tag `3.89.8.20260719`
- `overlay/` is based on the two proxy files from that fork commit, with the
  local re-login corrections: login-form detection at `/index.htm` (ha2),
  WebUI form login with session verification and a per-user server-side
  attempt limit independent of browser storage (ha3).
- `modern/` contains the corresponding original files; `stable/` contains the
  older released proxy. The stable diff includes prerequisite upstream cookie,
  timeout and URL-handling changes present in the reviewed fork.
- Copyright headers are retained. See each app's `LICENSE.upstream`.

For a patch update, review the fork diff, update the vendored files and
`PATCH_COMMIT`, then run all tests. Never automatically follow the patch branch.

## Gates and publication

1. Generate an exact-context unified patch; require `git apply --check`.
2. Check JavaScript syntax and require both upstream image architectures.
3. Build on the pinned original image. Require its original proxy SHA-256 to
   match the source before replacement and check the replacement SHA-256.
4. Publish version-specific images for all changed apps, both architectures.
5. Only after **all** builds succeed, commit the new HA app versions.

The dedicated `OpenCCU Update` workflow runs daily and manually. The generic
updater skips these apps because it commits versions before building images.
A failed job leaves existing advertised versions untouched. A partially uploaded
new tag may remain in GHCR, but is not advertised in HA and does not replace
`latest`. Concurrent repository changes abort the final commit; rerun the workflow.
No CI workflow is executed merely by creating these files locally.

The first publication can be built with the existing manual HA App Build workflow;
subsequent original updates use the dedicated workflow. Initial source publication
must be coordinated with initial image builds before users install the apps.

## Local checks

```text
python -m unittest discover -s .github/tests -p "test_openccu*.py"
node --test .github/tests/openccu-proxy.test.cjs
python .github/scripts/schema_validator.py
python .github/scripts/sync_openccu.py --export
```

The tests use isolated temporary stores, not a running CCU. They do not validate
RF hardware, HA Supervisor, full WebUI login or container boot. Those require
integration tests on a non-production CCU before enabling unattended upgrades.

### Initial verification (2026-08-27)

- Six updater/patch tests and six session/encryption tests passed.
- All four AMD64 overlay images built against the pinned originals. Original
  proxy checksums matched the release, snapshot and proxy images.
- The three patched ingress listeners started and responded in isolated
  `--network none` containers, using the original image dependencies. CCU init
  and radio services were not started. The helper passed Bash syntax validation.
- Repeated upstream generation returned no changes; repository schemas and
  the new workflow YAML parsed successfully.
- ARM64 manifests exist and CI builds both architectures; ARM64 builds have not
  been run locally. Nothing has been pushed or published by this implementation.

## Security

Both retention options default to false. Credential retention requires session
retention and stores recoverable AES-256-GCM credentials, not password hashes.
The encryption key is next to the records, so a backup containing both can decrypt
them. Do not describe this as protection against filesystem/backup access.
The fork keeps sessions alive, weakening normal idle expiry by design. Disabling
options stops using stored values; it does not automatically erase existing files.
The fork's session storage is retained; automatic login uses the local corrections
above. This is not a security audit. After installing ha3, enable both remember
options and log in manually once if credentials have not yet been stored. Test a
CCU restart without explicitly logging out: logout intentionally deletes the
stored credentials. Automated tests simulate WebUI responses; a real CCU reboot
and login must still be verified on the target installation.
