# Backup, Restore, and Rollback

## What is backed up

`OFM-domain-pack.yml` produces two artifacts:

- `Pack-<domain>.jar` — the WebLogic domain template.
- `<domain>-nodemanager.tgz` — the domain's NodeManager home.

They are fetched to `artifacts/<admin-host>/` on the controller.

## Retention

- Keep at least one backup from before every change window.
- Keep the last successful pre-upgrade backup until the new version has passed
  application acceptance.
- Store production artifacts in an approved repository with access control and
  an explicit retention period.
- Record the artifact checksum and the `ofm_release` used to create it.

## Before a destructive change

```bash
ansible-playbook OFM-domain-pack.yml --limit ofm-admin-01
```

`OFM-domain-clean.yml` refuses to run unless a packed domain exists, unless
`ofm_require_domain_backup=false` is set for a non-production environment.

## Restore a domain

1. Ensure the target host has the same FMW version and JDK as the backup.
2. Confirm the artifacts are present under `artifacts/<admin-host>/`.
3. Run:

```bash
ansible-playbook OFM-domain-unpack.yml --limit ofm-ms-01
```

4. Validate:

```bash
ansible-playbook OFM-validate.yml --limit ofm-ms-01
```

## Roll back an upgrade

1. Stop the new domain.
2. Keep the new Oracle home and logs for analysis.
3. Restore the packed domain and NodeManager archive.
4. Start the restored domain and run `OFM-validate.yml`.
5. Confirm datasources, LDAP, Forms, OHS, and application deployments.

## Roll back an installation

`OFM-installation-clean.yml` detaches and removes an Oracle home. It does not
restore a previous home. To roll back an installation:

1. Restore the previous Oracle home from the infrastructure backup or reinstall
   the previous media.
2. Restore the matching domain backup.
3. Run validation.

## Test the restore path

At least once per quarter, restore a non-production domain from artifacts and
run `OFM-validate.yml`. Record the result and the elapsed time.
