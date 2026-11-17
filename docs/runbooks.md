# Runbooks

## 1. Prepare the OS

```bash
ansible-playbook OFM-os-prepare.yml --limit ofm-admin-01
```

## 2. Install Java

```bash
ansible-playbook OFM-java-install.yml --limit ofm-admin-01
```

## 3. Install Infrastructure

```bash
ansible-playbook OFM-infrastructure-install.yml --limit ofm-admin-01
```

## 4. Create the domain

```bash
ansible-playbook OFM-domain-configure.yml --limit ofm-admin-01
```

This creates the RCU schemas (unless restricted JRF) and the base domain.

## 5. Extend the domain

```bash
ansible-playbook OFM-domain-oem.yml --limit ofm-admin-01
ansible-playbook OFM-forms-configure.yml --limit ofm-admin-01
```

## 6. Configure JDBC or LDAP

```bash
ansible-playbook OFM-domain-JDBC.yml --limit ofm-admin-01
ansible-playbook OFM-domain-LDAP.yml --limit ofm-admin-01
```

## 7. Pack a domain

```bash
ansible-playbook OFM-domain-pack.yml --limit ofm-admin-01
```

Artifacts are written to `artifacts/<admin-host>/` on the controller.

## 8. Unpack a domain

```bash
ansible-playbook OFM-domain-unpack.yml --limit ofm-ms-01
```

The unpack host must have the same FMW version and JDK.

## 9. Validate

```bash
ansible-playbook OFM-validate.yml --limit ofm-admin-01
```

## 10. Clean a domain

```bash
ansible-playbook OFM-domain-pack.yml --limit ofm-admin-01
ansible-playbook OFM-domain-clean.yml --limit ofm-admin-01 \
  -e ofm_confirm_destroy=true
```

The clean playbook refuses to run without confirmation and a packed domain
backup. For `ppe`/`prod`, also pass `-e ofm_confirm_destroy_prod=true`.

## 11. Remove the Oracle home

```bash
ansible-playbook OFM-installation-clean.yml --limit ofm-admin-01 \
  -e ofm_confirm_destroy=true
```

## Tags

- `install`, `configure`, `extend`, `pack`, `unpack`, `validate`, `clean`.
- Clean playbooks are tagged `never`; run them explicitly with
  `--tags clean,never` or by playbook name.
