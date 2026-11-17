# Release and Deprecation Policy

## Versioning

The project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes to role names, variable names, playbook names, or
  required inventory structure.
- **MINOR** — new roles, new supported FMW/JDK releases, new playbooks, or
  backward-compatible features.
- **PATCH** — bug fixes, documentation, lint/style, and security fixes that do
  not change the interface.

## Planned milestones

| Version | Content |
|---|---|
| `v0.1.0` | Baseline modernization scaffolding |
| `v0.2.0` | Ansible 14 compatibility, FQCN, loops, inventory |
| `v0.3.0` | Secrets, file modes, download hardening, destructive guards |
| `v0.4.0` | Idempotency, pack/unpack, bounded waits, multi-host safety |
| `v1.0.0` | FMW 12.2.1.4 on RHEL 8/9, lab validated |
| `v2.0.0` | FMW 14.1.2 with JDK 17/21, lab validated |

## Deprecation

- Deprecated items remain functional for **one major release**.
- Deprecations are documented in `CHANGELOG.md` and the relevant guide.
- Remove deprecated items only in the next major release.
- Current deprecations:
  - `OFM-oem-configure.yml` is an alias for `OFM-domain-oem.yml`.
  - camelCase variable names are retained while the snake_case migration runs.
  - The `ofm-java-8` role name is retained while the versioned Java catalog is
    adopted.

## Release checklist

1. `make syntax`
2. `make lint`
3. `make yamllint`
4. `make molecule`
5. Lab validation for the supported FMW/JDK/OS combination.
6. Update `CHANGELOG.md` and the support matrix in `README.md`.
7. Update `ROADMAP.md` checkboxes and progress log.
8. Tag the release: `git tag -a vX.Y.Z -m "vX.Y.Z"`.
9. Push the tag and publish the release notes.

## Support matrix updates

A release that adds or removes an FMW, JDK, or OS version must update:

- `README.md` support matrix.
- `docs/prerequisites.md`.
- `roles/ofm-installation-defaults/defaults/main.yml` software catalog.
- `CHANGELOG.md`.
- The CI matrix, if the controller or target Python changes.
