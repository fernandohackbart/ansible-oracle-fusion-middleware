# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the project uses [Semantic Versioning](https://semver.org/). See
[docs/release-policy.md](docs/release-policy.md).

## [Unreleased]

### Added

- `ansible.cfg` with deterministic inventory, collections, and validation defaults.
- Pinned Ansible/collection dependencies in `requirements.yml` and
  `requirements-dev.txt`.
- Example inventory with `ofm_admin`, `ofm_managed`, `ofm_forms`, and `ofm_ohs`
  groups.
- Lint/format configuration: `.ansible-lint`, `.yamllint`, `.editorconfig`,
  `.gitignore`.
- `Makefile` targets for setup, syntax, lint, yamllint, molecule, EE, and tests.
- GitHub Actions CI with an ansible-core 2.20/2.21/2.22 matrix.
- Rewritten README and documentation set: architecture, prerequisites,
  inventory, variables, secrets, runbooks, troubleshooting, upgrade, EE, and
  release policy.
- Implementation checklist in `ROADMAP.md` and detailed assessment in
  `docs/roadmap-details.md`.
- OS preparation role (`ofm_os_prepare`) for packages, users, limits, sysctl,
  directories, firewall, SELinux, and `/etc/oraInst.loc`.
- Software catalog for FMW 12.2.1.2, 12.2.1.4, and 14.1.2, including JDK and
  response-file selection.
- `ofm_validate` role and `OFM-validate.yml` playbook.
- `meta/argument_specs.yml` for every role.
- Molecule syntax scenario and Docker `os_prepare` scenario scaffold.
- Execution Environment and ansible-navigator configuration.
- Install/domain/extension markers for auditability.
- Restart handlers for the AdminServer and NodeManager.

### Changed

- Playbooks target inventory groups instead of requiring `targetHosts`/
  `unpackHosts` extra vars.
- All module actions use fully qualified collection names.
- Legacy `with_*` loops were replaced with `loop`.
- Command/shell tasks declare `changed_when`, and long commands use folded
  scalars.
- Booleans and conditionals were normalized.
- Play keywords use `remote_user` and parameterized `become_user`.
- Secrets are vault-driven; default passwords were removed.
- Secret-bearing tasks use `no_log`; RCU/boot/WLST files are secured and cleaned
  up on failure.
- Downloads use checksum variables, retries, timeouts, and TLS options.
- Destructive operations require explicit confirmation and a domain backup.
- Broad `pkill -9` was replaced with a graceful, domain-scoped stop.
- Domain pack/unpack uses a controller-side artifact repository and restores the
  NodeManager home.
- WLST wait scripts are bounded and fail after 60 attempts.
- Disk checks fail explicitly when a mount is missing.
- RCU and clean operations run once; clean/unpack use `serial`.
- Domain extension and WLST create operations are idempotent.
- Unused variables, templates, and commented code were removed.

### Deprecated

- `OFM-oem-configure.yml` is an alias for `OFM-domain-oem.yml`.
- camelCase variable names remain for compatibility; snake_case is the target.
- The `ofm-java-8` role name remains while the versioned Java catalog is adopted.

### Security

- Removed hardcoded default passwords.
- Added `no_log` coverage and restrictive file modes.
- Added checksum verification hooks and gated installer bypass flags.
- Added confirmation guards for clean/uninstall.

## [0.1.0] - 2026-11-17

### Added

- Initial modernization baseline.

[Unreleased]: https://example.invalid/ansible-oracle-fusion-middleware/compare/v0.1.0...HEAD
[0.1.0]: https://example.invalid/ansible-oracle-fusion-middleware/releases/tag/v0.1.0
