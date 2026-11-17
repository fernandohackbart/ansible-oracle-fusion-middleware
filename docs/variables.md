# Variables

## Installation

| Variable | Default | Purpose |
|---|---|---|
| `ofm_release` | `12.2.1.2` | Selects the software catalog entry |
| `ofmVersion` | catalog | FMW version used in paths and templates |
| `oracleHome` | `/u01/oracle/product/{{ ofmVersion }}/ofm` | Oracle home |
| `javaHome` | catalog | JDK home |
| `ofmInstallationMedia` | catalog | Product archive |
| `ofmInstallationFile` | catalog | Product installer |
| `ofmInstallationMediaChecksum` | catalog | `sha256:...` checksum |
| `ofm_validate_certs` | `true` | TLS verification for downloads |
| `ofm_decline_security_updates` | `true` | Installer security-update prompt |
| `ofm_ignore_sys_prereqs` | `false` | Opt-in installer prerequisite bypass |

## Domain

| Variable | Default | Purpose |
|---|---|---|
| `ofmDomainName` | `XPTO001` | Domain name |
| `ofmDomainHome` | `/u01/oracle/config/domains/{{ ofmDomainName }}` | Domain home |
| `ofmAdminserverName` | `AdminServer` | AdminServer name |
| `ofmAdminserverPort` | `12001` | AdminServer port |
| `ofmNodemgrPort` | `12000` | NodeManager port |
| `ofmAdminserverMachine` | inventory-derived | AdminServer/NodeManager host |
| `ofmRestrictedJRF` | `true` | Use restricted JRF (no RCU) |
| `ofmJdbcRCUSchemaPrefix` | domain name | RCU schema prefix |
| `ofmJdbcRCUPassword` | empty | RCU schema password |
| `ofmJdbcsysPassword` | empty | Database SYS password |
| `ofmAdminPassword` | empty | AdminServer password |
| `ofmNodemgrPassword` | empty | NodeManager password |

## Forms, OHS, JDBC, LDAP

| Variable | Purpose |
|---|---|
| `ofmFRMextmachines` | Forms managed-server hosts |
| `ofmFRMextmsport` | Forms managed-server port |
| `ofmFRMextclustername` | Forms cluster name |
| `ofmJDBCDATASOURCENAME` | JDBC datasource name |
| `ofmJDBCURL` | JDBC URL (`host:port/service`) |
| `ofmJDBCSchema` | JDBC schema/user |
| `ofmJDBCPassword` | JDBC password |
| `ofmLDAPProviderName` | LDAP provider name |
| `ofmLDAPHostName` / `ofmLDAPHostPort` | LDAP endpoint |
| `ofmLDAPBaseDN` | LDAP base DN |

## Destructive operations

| Variable | Default | Purpose |
|---|---|---|
| `ofm_confirm_destroy` | `false` | Required for clean/uninstall |
| `ofm_confirm_destroy_prod` | `false` | Required in `ppe`/`prod` |
| `ofm_require_domain_backup` | `true` | Require a packed domain before clean |

## Naming

Legacy camelCase names are retained for compatibility. New code should use
snake_case; the migration is tracked in [ROADMAP.md](../ROADMAP.md) Phase 5.
