# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `ansible.cfg` with deterministic inventory, collections, and validation defaults.
- Pinned Ansible/collection dependencies in `requirements.yml` and `requirements-dev.txt`.
- Example inventory with `ofm_admin`, `ofm_managed`, `ofm_forms`, and `ofm_ohs` groups.
- Lint/format configuration: `.ansible-lint`, `.yamllint`, `.editorconfig`, `.gitignore`.
- `Makefile` targets for setup, syntax, lint, yamllint, and tests.
- GitHub Actions validation workflow.
- Rewritten README with support matrix, inventory, secrets, and playbook reference.
- Implementation checklist in `ROADMAP.md` and detailed assessment in `docs/roadmap-details.md`.

### Changed

- Playbooks now target inventory groups instead of requiring `targetHosts`/`unpackHosts` extra vars.

## [0.1.0] - 2026-11-17

### Added

- Initial modernization baseline.

[Unreleased]: https://example.invalid/ansible-oracle-fusion-middleware/compare/v0.1.0...HEAD
[0.1.0]: https://example.invalid/ansible-oracle-fusion-middleware/releases/tag/v0.1.0
