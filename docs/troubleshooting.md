# Troubleshooting

## Secrets fail immediately

The domain/JDBC roles assert that passwords are non-empty. Provide them through
Ansible Vault or an external secret manager. See [secrets.md](secrets.md).

## Download fails

- Confirm `ofm_media_url` and the catalog archive names.
- Confirm the SHA256 checksum is set; an empty checksum omits verification.
- Check `ofm_validate_certs` and `ofm_ca_path` for an internal CA.
- Confirm the controller can reach the artifact repository.

## Installer refuses the Oracle home

Oracle installers require an empty Oracle home. Do not install 12.2.1.4 or
14.1.2 over a 12.2.1.2 home. Use a new `oracleHome` and keep the old one until
validation completes.

## RCU fails

- Confirm the database is reachable with `ofmJdbcURLrcu`.
- Confirm the SYS password and role.
- Confirm the component list for the selected FMW release.
- Check the RCU log under the Oracle home.

## Domain creation hangs

The wait scripts are capped at 60 attempts (10 seconds each). Check:

- AdminServer log: `{{ ofmDomainLogsHome }}/AdminServer/AdminServer.log`.
- NodeManager log: `{{ ofmDomainLogsHome }}/nodemanager/`.
- `ofmAdminserverMachine` and port values.
- Credential files under `{{ ofmInstallUserHomeDir }}/bin/`.

## NodeManager will not start

- Confirm `nodemanager.properties` and `nodemanager.domains`.
- Confirm the SSL configuration matches the domain.
- Confirm the port is open and not used by another process.
- Check `NODEMGR_HOME` and `JAVA_HOME`.

## Validation fails on a port

`OFM-validate.yml` checks the AdminServer, NodeManager, and optionally OHS. Start
the services or adjust `ofm_validate_*` ports. Set `ofm_validate_check_ohs=true`
only on OHS hosts.

## Clean refuses to run

Set `ofm_confirm_destroy=true`. In `ppe`/`prod`, also set
`ofm_confirm_destroy_prod=true`. Run `OFM-domain-pack.yml` first, or set
`ofm_require_domain_backup=false` in a non-production environment.

## Lint or syntax fails

```bash
make syntax
make lint
make yamllint
```

Ensure `community.general` and `ansible.posix` are installed from
`requirements.yml`. `archive` is not a builtin module.
