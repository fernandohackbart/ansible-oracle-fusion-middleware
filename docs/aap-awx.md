# Ansible Automation Platform / AWX

## Execution Environment

Build and push the image from [execution-environment.yml](../execution-environment.yml):

```bash
make ee
podman tag ofm-ee:latest <registry>/ofm-ee:<tag>
podman push <registry>/ofm-ee:<tag>
```

Register the image as the Execution Environment for the project in AAP/AWX.

## Inventory

Create an inventory with the groups used by the playbooks:

- `ofm_admin`
- `ofm_managed`
- `ofm_forms`
- `ofm_ohs`

Set `ansible_user`, `ansible_python_interpreter`, `ofm_environment`,
`ofm_release`, `ofm_media_source`, and `ofm_media_url` as inventory or group
variables.

## Credentials

| Credential | Type | Purpose |
|---|---|---|
| Machine | SSH | Login to target hosts |
| Vault | Ansible Vault | Decrypt `vault.yml` |
| Source control | SCM | Clone this repository |
| Registry | Container registry | Pull the EE image |
| Secret manager | Custom/external | Optional external secret lookup |

Do not store plaintext passwords in surveys or job templates.

## Job templates

Create one job template per playbook:

| Template | Playbook | Tags |
|---|---|---|
| OS prepare | `OFM-os-prepare.yml` | `prepare` |
| Java install | `OFM-java-install.yml` | `install` |
| Infrastructure install | `OFM-infrastructure-install.yml` | `install` |
| Forms install | `OFM-forms-install.yml` | `install` |
| OHS install | `OFM-ohs-install.yml` | `install` |
| Domain configure | `OFM-domain-configure.yml` | `configure` |
| Domain extend | `OFM-domain-oem.yml` | `extend` |
| Domain pack | `OFM-domain-pack.yml` | `pack` |
| Domain unpack | `OFM-domain-unpack.yml` | `unpack` |
| Validate | `OFM-validate.yml` | `validate` |
| Domain clean | `OFM-domain-clean.yml` | `clean,never` |
| Installation clean | `OFM-installation-clean.yml` | `clean,never` |

## Surveys

Use surveys for:

- `ofm_release` (choices: `12.2.1.2`, `12.2.1.4`, `14.1.2`).
- `ofm_confirm_destroy` (boolean, default false).
- `ofm_confirm_destroy_prod` (boolean, default false).
- `ofm_require_domain_backup` (boolean, default true).
- `ofm_validate_check_ohs` (boolean, default false).

## RBAC and approvals

- Restrict clean/uninstall templates to a platform-admin team.
- Require an approval node before destructive jobs in `ppe`/`prod`.
- Give application teams access to `OFM-validate.yml` and read-only inventories.
- Use `--limit` in the job template or a survey to scope a host.

## Logs

AAP job output contains the Ansible log. Forward it to the central log platform
and retain it for the same period as the change record.
