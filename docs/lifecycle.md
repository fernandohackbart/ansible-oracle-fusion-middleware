# Lifecycle Review

## Cadence

Review this project quarterly, and before every major change window.

## Checklist

- [ ] Ansible community package and ansible-core are on a supported release.
- [ ] Collections are pinned and updated to tested versions.
- [ ] `ansible-lint`, `yamllint`, and Molecule are green.
- [ ] The CI matrix covers the supported Python and ansible-core versions.
- [ ] The Execution Environment builds and runs the validation playbook.
- [ ] FMW 12c support dates are tracked (Premier Dec 2026, Extended Dec 2027).
- [ ] FMW 14.1.2 certification and patch levels are reviewed.
- [ ] The next FMW suite release (planned 2027) is on the roadmap.
- [ ] JDK 17/21 patch levels are current for 14.1.2.
- [ ] RHEL 8/9/10 support and Python versions are reviewed.
- [ ] Secrets are rotated and vault access is reviewed.
- [ ] Destructive job approvals and RBAC are reviewed.
- [ ] Backup/restore has been tested in the last quarter.
- [ ] Deprecated variables/roles are on schedule for removal.

## Owners

| Area | Owner |
|---|---|
| Ansible tooling and CI | Platform automation |
| Oracle Fusion Middleware | Middleware engineering |
| OS and JDK | Linux platform |
| Secrets and access | Security/identity |
| Backup and recovery | Operations |

## Decision log

Record decisions that affect the support matrix:

| Date | Decision | Owner | Notes |
|---|---|---|---|
| 2026-11-17 | Target Ansible 14.6 / ansible-core 2.21.6 | Platform automation | Ansible 15 tracked for the next cycle |
| 2026-11-17 | Tactical FMW target 12.2.1.4 | Middleware engineering | 12c Premier ends Dec 2026 |
| 2026-11-17 | Strategic FMW target 14.1.2 | Middleware engineering | Lab validation pending |
| 2026-11-17 | RHEL 8/9 floor | Linux platform | RHEL 7 exception requires an exit date |
