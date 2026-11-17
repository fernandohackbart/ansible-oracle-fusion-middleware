# Oracle Fusion Middleware Ansible Automation

Ansible playbooks and roles for installing, configuring, packing, unpacking, and cleaning Oracle Fusion Middleware 12c/14c domains on Linux.

> **Project status:** active modernization. The playbooks are being migrated from a 2017-era Ansible 2.x baseline to Ansible 14.6 / ansible-core 2.21.6. Track progress and known gaps in [ROADMAP.md](ROADMAP.md).

## Supported matrix

| Component | Current/validated | Target |
|---|---|---|
| Controller | Python 3.12+, ansible-core 2.21.6 | Ansible 14.6.0 |
| Managed nodes | RHEL/Oracle Linux 8/9, Python 3.9+ | RHEL 8.10 / 9.x |
| Oracle Fusion Middleware | 12.2.1.2 (legacy baseline) | 12.2.1.4 → 14.1.2 |
| Java | JDK 8 (latest certified 8u) | JDK 17/21 for FMW 14.1.2 |
| Collections | `community.general` 14.0.1, `ansible.posix` 2.2.2 | Pinned in `requirements.yml` |

RHEL 7 is **not** a supported target for ansible-core 2.21 (it requires Python 3.9–3.14 on managed nodes). If RHEL 7 must remain temporarily, install Python 3.9+ and set `ansible_python_interpreter`; document it as an exception with an exit date.

## Prerequisites

- A control node with Python 3.12–3.14.
- Ansible 14.6.0 and the pinned collections.
- SSH access to the target hosts and a sudo-capable login user.
- An `oracle` user and the required OS prerequisites on the targets (see [ROADMAP.md](ROADMAP.md), Phase 4).
- Oracle media (licensed; not included) reachable through an artifact repository or local path.
- Vaulted secrets for the AdminServer, NodeManager, RCU, and database passwords.

## Quick start

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
ansible-galaxy collection install -r requirements.yml

# Review and edit the example inventory.
$EDITOR inventories/example/hosts.yml
$EDITOR inventories/example/group_vars/all.yml

# Validate without connecting to hosts.
make syntax
make lint
```

Run a playbook:

```bash
ansible-playbook OFM-java-install.yml
ansible-playbook OFM-infrastructure-install.yml
ansible-playbook OFM-domain-configure.yml
```

Use `--limit` to target a subset:

```bash
ansible-playbook OFM-domain-configure.yml --limit ofm-admin-01
```

## Inventory

The example inventory separates hosts by responsibility:

| Group | Purpose |
|---|---|
| `ofm_admin` | AdminServer host; domain creation and WLST configuration |
| `ofm_managed` | Managed-server hosts; domain unpack and managed-server configuration |
| `ofm_forms` | Forms and Reports hosts |
| `ofm_ohs` | Oracle HTTP Server hosts |

At minimum, set `ansible_host`, `ansible_user`, and the Oracle user home variables for each host. Secrets belong in `group_vars/<environment>/vault.yml`, never in `group_vars/all.yml`.

## Secrets

```bash
cp inventories/example/group_vars/vault.yml.example inventories/example/group_vars/vault.yml
$EDITOR inventories/example/group_vars/vault.yml
ansible-vault encrypt inventories/example/group_vars/vault.yml
ansible-playbook OFM-domain-configure.yml --ask-vault-pass
```

The expected secret variables are:

- `ofmAdminPassword`
- `ofmNodemanagerPassword`
- `ofmJdbcRCUPassword`
- `ofmJdbcsysPassword`
- `ofmJDBCPassword`

Do not commit decrypted vault files or vault password files. `no_log` and restrictive file modes are required for every task that handles these values.

## Playbooks

| Playbook | Purpose |
|---|---|
| `OFM-java-install.yml` | Install/manage the JDK |
| `OFM-infrastructure-install.yml` | Install FMW Infrastructure |
| `OFM-forms-install.yml` | Install Forms and Reports |
| `OFM-ohs-install.yml` | Install Oracle HTTP Server |
| `OFM-domain-configure.yml` | Create the base domain and RCU schemas |
| `OFM-domain-oem.yml` | Extend the domain with Enterprise Manager |
| `OFM-forms-configure.yml` | Extend the domain with Forms |
| `OFM-domain-JDBC.yml` | Configure a JDBC datasource |
| `OFM-domain-LDAP.yml` | Configure LDAP integration |
| `OFM-domain-addmanagedserver.yml` | Create managed servers |
| `OFM-domain-pack.yml` | Pack a domain template and NodeManager home |
| `OFM-domain-unpack.yml` | Unpack a domain template on a target |
| `OFM-domain-clean.yml` | Stop processes, drop RCU schemas, remove domain files |
| `OFM-installation-clean.yml` | Detach/remove the Oracle home |

`OFM-oem-configure.yml` is retained as a duplicate of `OFM-domain-oem.yml` during the migration and will be removed in a future release.

## Validation

```bash
make syntax   # ansible-playbook --syntax-check for every playbook
make lint     # ansible-lint with the committed profile
make yamllint # YAML style checks
make test     # syntax + lint + yamllint
```

The current `ansible-lint` configuration starts at profile `basic` and temporarily warns on rules scheduled for Phase 1/3. See [ROADMAP.md](ROADMAP.md) for the target profile and exit criteria.

## Roadmap

The implementation checklist, prioritized backlog, known defects, and Oracle lifecycle notes are in [ROADMAP.md](ROADMAP.md). The detailed assessment is in [docs/roadmap-details.md](docs/roadmap-details.md).

## License

See [LICENSE](LICENSE). Oracle software media is licensed separately and is not distributed with this repository.
