# Prerequisites

## Control node

- Python 3.12–3.14.
- Ansible 14.6.0 / ansible-core 2.21.6.
- Collections from `requirements.yml`.
- SSH access and sudo rights to the target hosts.
- Network access to the artifact repository or media URL.
- Ansible Vault password or an external secret-manager credential.

## Target nodes

- RHEL/Oracle Linux 8.10 or 9.x (RHEL 10 after validation).
- Python 3.9–3.14. RHEL 8 requires a Python 3.9+ app stream.
- `sudo` for the login user.
- An `oracle` user and `oinstall`/`dba` groups (created by
  `OFM-os-prepare.yml`).
- Sufficient disk space:
  - Infrastructure: ~10 GiB.
  - Forms: ~15 GiB.
  - OHS: ~4 GiB.
  - Domain configuration: ~5 GiB.
  - Temporary/stage: ~5 GiB.
- Required kernel parameters, limits, and `/etc/oraInst.loc` (created by
  `OFM-os-prepare.yml`).

## Oracle media

Licensed media is **not** included. Populate the catalog in
`roles/ofm-installation-defaults/defaults/main.yml`:

- Infrastructure archive, installer, response file, SHA256.
- Forms and OHS entries as applicable.
- JDK archive, release, SHA256.

Set `ofm_release` to `12.2.1.2`, `12.2.1.4`, or `14.1.2`.

## Secrets

See [secrets.md](secrets.md). The domain and JDBC roles fail if required secrets
are empty.

## Validation

```bash
make syntax
make lint
make yamllint
make molecule
```
