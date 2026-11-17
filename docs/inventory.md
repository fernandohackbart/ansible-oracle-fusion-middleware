# Inventory

The example inventory is at `inventories/example/hosts.yml`.

```yaml
all:
  children:
    ofm_admin:
      hosts:
        ofm-admin-01:
          ansible_host: 192.0.2.10
          ofm_admin_host: 192.0.2.10
    ofm_managed:
      hosts:
        ofm-ms-01:
          ansible_host: 192.0.2.11
          ofm_managed_host: 192.0.2.11
```

## Required group variables

| Variable | Purpose |
|---|---|
| `ansible_user` | SSH login user |
| `ansible_python_interpreter` | Python 3.9+ on the target |
| `ofm_environment` | `dev`, `test`, `ppe`, or `prod` |
| `ofm_release` | `12.2.1.2`, `12.2.1.4`, or `14.1.2` |
| `ofm_media_source` | `webserver` or `filesystem` |
| `ofm_media_url` | Artifact repository base URL |
| `ofm_user` | Oracle OS user (default `oracle`) |
| `ofm_user_home` | Oracle OS home (default `/home/oracle`) |

## Secrets

Put secrets in `group_vars/<environment>/vault.yml` and encrypt the file. Never
put them in `group_vars/all.yml`.

## Targeting

Use `--limit` for a single host:

```bash
ansible-playbook OFM-domain-configure.yml --limit ofm-admin-01
```

The playbooks no longer require `-e targetHosts=...` or `-e unpackHosts=...`.

## Groups

- `ofm_admin`: RCU, domain creation, AdminServer, WLST.
- `ofm_managed`: managed servers and domain unpack.
- `ofm_forms`: Forms installation and extension.
- `ofm_ohs`: Oracle HTTP Server.

## RHEL 7 exception

RHEL 7 is not a supported ansible-core 2.21 target. If it must remain
temporarily, install Python 3.9+ and set `ansible_python_interpreter`. Record the
exit date in the environment README.
