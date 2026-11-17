# Secrets

This project must never contain plaintext credentials in Git, logs, or
world-readable files.

## Required variables

| Variable | Used by |
|---|---|
| `ofmAdminPassword` | Domain creation, AdminServer scripts |
| `ofmNodemanagerPassword` | NodeManager connection and boot properties |
| `ofmJdbcRCUPassword` | RCU schema creation/drop |
| `ofmJdbcsysPassword` | RCU SYS connection |
| `ofmJDBCPassword` | JDBC datasource configuration |

The variables are intentionally empty in role defaults. Domain and JDBC roles
assert that they are non-empty before doing any work.

## Ansible Vault workflow

```bash
cp inventories/example/group_vars/vault.yml.example \
   inventories/example/group_vars/vault.yml

$EDITOR inventories/example/group_vars/vault.yml
ansible-vault encrypt inventories/example/group_vars/vault.yml

ansible-playbook OFM-domain-configure.yml --ask-vault-pass
```

For CI or automation controllers, provide the password through a credential
store and reference it with `--vault-password-file` or the controller's native
credential type. Never commit the password file.

## External secret managers

If the organization uses HashiCorp Vault, CyberArk, or a cloud secret manager,
replace the plaintext example with a lookup:

```yaml
ofmAdminPassword: "{{ lookup('community.hashi_vault.vault_kv2_get', 'ofm/admin', field='password') }}"
```

Add the required collection to `requirements.yml` and document the lookup in the
inventory README.

## Handling rules

- Every task that templates, copies, or consumes a secret uses `no_log: true`.
- Secret files are `0600`; secret directories are `0700`.
- Use `block`/`always` so failed tasks remove temporary secret files.
- Prefer stdin over temporary password files where the Oracle tool supports it.
- Rotate secrets after any suspected exposure and update the vault.
- Do not print secrets with `debug`, `-vvv`, or task names.

## Validation

```bash
# No historical default password should remain in roles or templates.
grep -R "the old default password" roles || true

# Confirm no secret file is world-readable.
find roles -type f \( -name '*.rsp' -o -name 'boot.properties' \) -perm -004
```

See [ROADMAP.md](ROADMAP.md) Phase 2 for the remaining hardening work.
