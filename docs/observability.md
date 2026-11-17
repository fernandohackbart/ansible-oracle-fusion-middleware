# Observability and Health Checks

## Ports

| Service | Default | Variable |
|---|---:|---|
| AdminServer | 12001 | `ofmAdminserverPort` |
| NodeManager | 12000 | `ofmNodemgrPort` |
| OHS | 7777 | `ofm_validate_ohs_port` |
| Database listener | 1521 | `ofmJdbcURLrcu` |

## Log locations

| Log | Path |
|---|---|
| AdminServer | `{{ ofmDomainLogsHome }}/AdminServer/AdminServer.log` |
| Managed server | `{{ ofmDomainLogsHome }}/<server>/<server>.log` |
| NodeManager | `{{ ofmDomainLogsHome }}/nodemanager/` |
| Domain pack | `{{ ofmDomainLogsHome }}/Pack-<domain>.log` |
| Domain unpack | `{{ ofmDomainLogsHome }}/Unpack-<domain>.log` |
| Installer | Console output; retain the Ansible log |
| RCU | Oracle home RCU logs |

## Automated validation

```bash
ansible-playbook OFM-validate.yml --limit ofm-admin-01
```

The role checks:

- Oracle home exists.
- Java executable exists.
- Domain `config/config.xml` exists.
- AdminServer port is listening (admin host).
- NodeManager port is listening.
- OHS port is listening when `ofm_validate_check_ohs=true`.

## Manual checks

```bash
ss -lntp | grep -E '12000|12001|7777'
curl -k -I https://<admin-host>:12001/console/
```

For a WLST check:

```bash
$ORACLE_HOME/oracle_common/common/bin/wlst.sh
connect('weblogic', '<password>', 't3://<admin-host>:12001')
domainRuntime()
cd('/ServerRuntimes')
ls()
```

Do not put passwords in shell history. Use the generated credential files or a
vault-backed wrapper.

## Suggested alerts

- AdminServer port down for more than 5 minutes.
- NodeManager port down for more than 5 minutes.
- Domain log error rate above baseline.
- Disk usage above 85% on `/u01`.
- Backup artifact missing or older than the retention target.

## Validation tags

`OFM-validate.yml` is tagged `validate`. It is safe to run without install or
configure tags.
