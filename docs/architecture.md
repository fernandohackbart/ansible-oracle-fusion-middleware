# Architecture

## Control plane

- **Ansible control node:** Ansible 14.6 / ansible-core 2.21.6 on Python 3.12+.
- **Inventory:** environment-specific YAML inventories with `ofm_admin`,
  `ofm_managed`, `ofm_forms`, and `ofm_ohs` groups.
- **Artifacts:** packed domains and NodeManager archives are fetched to the
  controller under `artifacts/<admin-host>/`.

## Target hosts

| Group | Responsibility |
|---|---|
| `ofm_admin` | AdminServer, RCU, domain creation, WLST configuration |
| `ofm_managed` | Managed servers, domain unpack, NodeManager |
| `ofm_forms` | Forms and Reports installation and extension |
| `ofm_ohs` | Oracle HTTP Server |

## Role flow

```text
ofm_os_prepare
  └── ofm_java_8
        └── ofm_infra_122
              ├── ofm_forms_122
              ├── ofm_ohs_122
              └── ofm_domain_base_122
                    ├── ofm_domain_managedserver
                    ├── ofm_domain_forms_122
                    ├── ofm_domain_oem_122
                    ├── ofm_jdbc_datasource
                    ├── ofm_ldap_integration
                    ├── ofm_domain_pack
                    ├── ofm_domain_unpack
                    ├── ofm_domain_clean
                    └── ofm_installation_clean
ofm_validate
```

## State markers

Installations and extensions write JSON markers:

- `{{ oracleHome }}/.ofm-install-infrastructure.json`
- `{{ oracleHome }}/.ofm-install-forms.json`
- `{{ oracleHome }}/.ofm-install-ohs.json`
- `{{ javaHome }}/.ofm-install-java.json`
- `{{ ofmDomainHome }}/.ofm-domain.json`
- `{{ ofmDomainHome }}/.ofm-extended-forms`
- `{{ ofmDomainHome }}/.ofm-extended-oem`

Use these markers for audits and future idempotency checks. The current
folder-existence checks remain for backward compatibility.
