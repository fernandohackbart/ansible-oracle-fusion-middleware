# Upgrade Path: Fusion Middleware 12c to 14.1.2

This runbook is a scaffold. The 14.1.2 path is selectable through the software
catalog, but it has **not** been validated against licensed media or a lab
environment. Treat every step as requiring a change window and a tested backup.

## Why upgrade

- Oracle Fusion Middleware 12c Premier Support ends in **December 2026**;
  Extended Support ends in **December 2027**.
- Fusion Middleware **14.1.2** is the current LTS suite release, with Premier
  Support planned through 2030 and Extended Support through 2033.
- 14.1.2 is certified with JDK 17 and 21 and supports Jakarta EE 8.
- WebLogic Server 15.1.1 is a separate standalone LTS release; it is not a
  drop-in replacement for the full FMW 14.1.2 suite.

## Before you start

1. Confirm the application certification for 14.1.2 (ADF, Forms, OHS, SOA, etc.).
2. Confirm whether Forms and Reports is available in 14.1.2 for your entitlement.
   If not, keep Forms on 12.2.1.19 and plan for the next FMW suite release.
3. Obtain licensed 14.1.2 media and the matching RCU distribution.
4. Populate the software catalog in
   `roles/ofm-installation-defaults/defaults/main.yml`:
   - `ofm_software_catalog["14.1.2"].infrastructure.archive`
   - `.installer`, `.response_file`, `.sha256`
   - `forms` and `ohs` entries as applicable
   - `java.version`, `java.release`, `java.file`, `java.sha256`
5. Set `ofm_release: "14.1.2"` in the environment inventory.
6. Provision a lab host and a database for RCU. Do not upgrade production first.

## Upgrade sequence

### 1. Prepare the OS

```bash
ansible-playbook OFM-os-prepare.yml --limit ofm-admin-01
```

Validate that the Oracle user, limits, sysctl, directories, and
`/etc/oraInst.loc` are present.

### 2. Install JDK 17 or 21

```bash
ansible-playbook OFM-java-install.yml --limit ofm-admin-01
```

Confirm `java -version` reports the certified build. Do not reuse the 12c JDK.

### 3. Back up the 12c domain

```bash
ansible-playbook OFM-domain-pack.yml --limit ofm-admin-01
```

Store the packed domain and NodeManager archive in the controller artifact
repository. Record the checksums and retention period.

### 4. Install 14.1.2 Infrastructure

```bash
ansible-playbook OFM-infrastructure-install.yml --limit ofm-admin-01
```

The installer must target an empty Oracle home. Do not install 14.1.2 over a
12c Oracle home.

### 5. Create the 14.1.2 RCU schemas

Use the 14.1.2 RCU distribution and the matching response files. Validate the
component list against the 14.1.2 documentation before running.

### 6. Create or extend the domain

```bash
ansible-playbook OFM-domain-configure.yml --limit ofm-admin-01
```

Use a new domain name or a new domain home for the first validation. Keep the
12c domain intact until the 14.1.2 domain passes application testing.

### 7. Forms and OHS

- OHS: install the 14.1.2 OHS distribution if it is part of your entitlement.
- Forms: confirm availability in 14.1.2. If Forms remains on 12.2.1.19, document
  the mixed-version support boundary and the network topology.

### 8. Validate

```bash
ansible-playbook OFM-validate.yml --limit ofm-admin-01
```

Check the AdminServer, NodeManager, application deployments, datasources, LDAP,
and OHS endpoints.

### 9. Roll back if needed

1. Stop the 14.1.2 domain.
2. Restore the packed 12c domain and NodeManager archive.
3. Start the 12c domain and run `OFM-validate.yml`.
4. Keep the 14.1.2 Oracle home and logs for analysis.

## Known gaps

- The 14.1.2 response files in this repository are scaffolds copied from the
  12c layout. Validate every field against the 14.1.2 installer.
- RCU component names and the domain template version must be confirmed for
  14.1.2.
- WLST scripts remain Jython/Python-2 style. Validate them against the 14.1.2
  WebLogic WLST before converting anything to Python 3.
- No 14.1.2 media or checksum is committed. Populate the catalog from the
  licensed distribution.
- Forms 14.1.2 availability is not assumed. Check Oracle certification first.

See [ROADMAP.md](ROADMAP.md) items 4.4 and 4.5 for status.
