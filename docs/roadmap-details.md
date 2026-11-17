# ROADMAP — Oracle Fusion Middleware Ansible Project

> **Historical assessment.** This document records the initial analysis and
> rationale. For the live checklist and current status, see
> [../ROADMAP.md](../ROADMAP.md).

**Status:** Draft for review  
**Last updated:** 2026-11-17  
**Repository:** `ansible-oracle-fusion-middleware`  
**Scope:** Modernize the playbooks/roles to current Ansible, harden secrets and destructive operations, make the automation idempotent and testable, and provide a supported path from Oracle Fusion Middleware 12.2.1.2 to 12.2.1.4 and 14.1.2.

> **Executive summary**
>
> The codebase is syntactically closer to modern Ansible than its age suggests: all 15 playbooks pass `ansible-playbook --syntax-check` on **ansible-core 2.21.6** once `community.general` is installed and inventory variables are supplied. The real risk is operational, not syntax: plaintext passwords, non-idempotent `command`/`shell` tasks, no inventory/CI/tests, hardcoded hosts and versions, unsafe clean-up, and an unsupported OS/JDK/FMW baseline.
>
> The plan has two platform tracks:
>
> 1. **Tactical:** FMW **12.2.1.4** (or Forms **12.2.1.19**) on **RHEL 8/9** with the latest certified **JDK 8**, because 12c Premier Support ends in **December 2026**.
> 2. **Strategic:** FMW **14.1.2** with **JDK 17/21**, supported through 2030/2033, with a plan for the next FMW release expected in 2027.
>
> Target tooling: **Ansible 14.6.0 / ansible-core 2.21.6**, controller Python **3.12–3.14**, target Python **3.9–3.14**, `ansible-lint` 26.x, pinned collections, CI on every change.

---

## 1. Current state (verified)

| Dimension | Current state | Assessment |
|---|---|---|
| Top-level playbooks | 15 `OFM-*.yml` files | Functional but overlapping responsibilities |
| Roles | 17 under `roles/` | Version suffix `-122`; hyphenated names fail lint |
| Templates | 42 WLST/response/nodemanager files | Mostly Python 2-style WLST (expected for 12c) |
| YAML volume | ~2,042 lines | Significant trailing-whitespace/style debt |
| Target FMW | 12.2.1.2 | Outdated; 12c support clock is running out |
| JDK | 8u101 (2016) | Below the 8u211 minimum for 12.2.1.4; security risk |
| Target OS | RHEL 7 or equivalent | RHEL 7 reached EOL in June 2024 |
| Ansible style | 2017-era Ansible 2.x | `with_*`, short module names, free-form args |
| Secrets | Plaintext defaults and templates | 5 hardcoded `the old default password` values |
| Inventory | None | `targetHosts` / `unpackHosts` must be passed as extra vars |
| Tests / CI | None | No syntax, lint, molecule, or integration gate |
| Config | No `ansible.cfg`, `requirements.yml`, `.ansible-lint` | Behavior depends on the operator's environment |

### Verification performed

Validated in a throwaway Python 3.12.13 virtual environment with:

- `ansible-core 2.21.6`
- `ansible-lint 26.11.0`
- `community.general 14.0.1`

Results:

- **15/15 playbooks** pass `--syntax-check` with an example inventory defining `targetHosts`, `unpackHosts`, `targetUser`, and `serverEnvironment`.
- Without `community.general`, **`OFM-domain-pack.yml` fails**: `couldn't resolve module/action 'archive'`. `archive` is provided by `community.general`, not `ansible-core`.
- Without inventory variables, **14/15 playbooks fail** with `'targetHosts' is undefined` or `'unpackHosts' is undefined`.
- `ansible-lint` reports **1,385 findings**:

| Rule | Count | Meaning |
|---|---:|---|
| `yaml[...]` | 618 | Trailing spaces, truthy values, indentation, line length, comments |
| `fqcn[action-core]` | 209 | Short module names instead of `ansible.builtin.*` |
| `var-naming[pattern]` | 155 | camelCase and uppercase variable names |
| `name[template]` | 154 | Jinja embedded mid-string in task names |
| `no-changed-when` | 40 | `command`/`shell` tasks always report changed |
| `jinja[spacing]` | 30 | Jinja whitespace style |
| `yaml[truthy]` | 24 | `yes`/`no` instead of `true`/`false` |
| `literal-compare` | 22 | `== False` comparisons |
| `ignore-errors` | 20 | Hidden failures |
| `role-name` | 16 | Hyphenated/versioned role names |
| `no-free-form` | 12 | `stat: path=...` style |
| `risky-file-permissions` | 9 | Files created without explicit modes |

**Interpretation:** syntax compatibility is not the main problem. The main problem is safety, idempotency, operability, and lifecycle.

---

## 2. Target state

| Component | Current | Target now | Target next | Rationale |
|---|---|---|---|---|
| Ansible community package | Unpinned/2.x era | **14.6.0** | 15.x when GA | 14.6.0 is the current stable release (2026-11-04) |
| ansible-core | Unpinned/2.x era | **2.21.6** | **2.22.x** (test), 15.x later | 2.21 is the core shipped with Ansible 14 |
| Controller Python | 3.6 on this workstation | **3.12–3.14** | 3.13/3.14 | ansible-core 2.21 control-node requirement |
| Target Python | 2.7/3.6 on RHEL 7 | **3.9–3.14** | 3.12+ | ansible-core 2.21 managed-node requirement |
| Target OS | RHEL 7 | **RHEL 8.10 / 9.x** | RHEL 10 | RHEL 7 is EOL; RHEL 8/9 are supported |
| FMW suite | 12.2.1.2 | **12.2.1.4** | **14.1.2** | 12c Premier ends Dec 2026; 14.1.2 is LTS |
| Forms & Reports | 12.2.1.2 | **12.2.1.19** | FMW 27 (2027) | 12.2.1.19 is the current 12c Forms release |
| OHS | 12.2.1.2 | **12.2.1.4** | 14.1.2 / FMW 27 | Collocated OHS with FMW Infrastructure |
| JDK | 8u101 | Latest certified **8u** (>= 8u211) | **17.0.12+ / 21.0.4+** | 12.2.1.4 certifies JDK 8; 14.1.2 certifies 17/21 |
| Collections | None pinned | `community.general` 14.x, `ansible.posix` 2.x | Review with each Ansible major | `archive`, `sysctl`, `mount`, `firewalld` live outside core |
| Lint | None | `ansible-lint` 26.x, profile `basic` | Profile `production` | Prevent regressions and style drift |
| Tests | None | Syntax + lint + molecule for non-Oracle roles | Full lab integration | Oracle media is licensed; test logic without media |

### Lifecycle notes

- **RHEL 7:** end of maintenance was **June 2024**. ansible-core 2.21 targets Python **3.9–3.14**; RHEL 7's default Python 3.6 is not supported. If RHEL 7 must remain temporarily, install Python 3.9+ and set `ansible_python_interpreter`, but treat it as a documented exception with an exit date. The strategic answer is RHEL 8/9.
- **FMW 12.2.1.4:** Premier Support ends **December 2026**; Extended Support ends **December 2027**. Start the upgrade now.
- **FMW 14.1.2:** released **December 2024**; Oracle plans Premier Support through **2030** and Extended Support through **2033**. It is the long-term suite foundation.
- **WebLogic Server 15.1.1:** released **October 2025**, LTS, JDK 17/21, Jakarta EE 9.1. It is a standalone WebLogic release; FMW suite customers should plan around 14.1.2 and the next suite release.
- **Forms & Reports:** 12.2.1.19 is the current 12c release. Confirm Forms availability in the 14.1.2 suite before committing to a Forms upgrade; Oracle's Statement of Direction positions Forms in the next FMW release (planned 2027). Do not assume Forms 14.1.2 exists without checking the certification matrix.
- **Ansible 15 / ansible-core 2.22:** ansible-core 2.22.0 is already available; Ansible 15 is in development. Target 14.6.0 for production stability and add 2.22 to the CI matrix to prepare.

---

## 3. Guiding principles

1. **Pin everything.** Ansible, collections, lint, Python, FMW media, JDK, and response files. No floating `latest`.
2. **Idempotent by default.** Every task must either be module-based or declare `creates`, `changed_when`, or `failed_when`.
3. **Secrets never touch Git or logs.** Vault/external secret manager, `no_log`, `0600`/`0700` modes, and cleanup on failure.
4. **Inventory-driven.** No required `targetHosts` extra var; use groups (`ofm_admin`, `ofm_managed`, `ofm_ohs`, `ofm_forms`) and `--limit`.
5. **No destructive action without a guard.** Explicit confirmation, environment checks, backups, and a dry-run path.
6. **Small, composable roles.** Explicit imports, `meta/argument_specs.yml`, and documented inputs/outputs.
7. **Everything is validated.** Syntax, lint, molecule, and lab integration on every change.
8. **One supported path forward.** Document the current supported FMW/OS/JDK combination and deprecate old ones deliberately.

---

## 4. Phases

### Phase 0 — Baseline and guardrails (P0, ~1 week)

**Goal:** make the repository reproducible and measurable before changing behavior.

Deliverables:

- `ansible.cfg` with inventory, roles path, collections path, host-key checking, retry files disabled, interpreter discovery, and deprecation warnings enabled.
- `requirements.yml` pinning collections (at minimum `community.general` and `ansible.posix`).
- `requirements-dev.txt` pinning `ansible==14.6.0`, `ansible-lint`, `yamllint`, `molecule`, `ansible-builder`, `pre-commit`.
- `.ansible-lint` (start at `profile: basic`, raise over time), `.yamllint`, `.editorconfig`, `.gitignore`, `pre-commit` hooks.
- `inventories/example/` with `hosts.yml`, `group_vars/all.yml`, and `group_vars/vault.yml.example`; skeleton environments for dev/test/prod.
- `docs/` structure and a rewritten `README.md` with prerequisites, supported matrix, inventory example, and runbook.
- `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`.
- CI skeleton: syntax-check, lint, yamllint on every pull request.
- Normalize file hygiene: remove trailing whitespace, fix indentation, remove executable bits from YAML files.

Acceptance:

- Fresh clone + documented setup produces a working `ansible --version` and `ansible-lint --version`.
- All 15 playbooks pass `--syntax-check` using the example inventory, with no `targetHosts is undefined`.
- CI is green at lint profile `basic` (temporary waivers allowed, recorded in `.ansible-lint` with owners and expiry).
- The README no longer ends mid-sentence.

---

### Phase 1 — Ansible 14 compatibility (P0, ~1–2 weeks)

**Goal:** run cleanly on Ansible 14.6 / ansible-core 2.21.6, with no unresolved modules or deprecated syntax.

Migration table:

| Current pattern | Target pattern | Occurrences | Notes |
|---|---|---:|---|
| `archive:` | `community.general.archive:` or `ansible.builtin` equivalent if one exists | 1 | **Hard blocker** with core-only installs |
| Short module names (`file`, `template`, `stat`, ...) | `ansible.builtin.*` / FQCN | 209 | Use `ansible-lint --fix` then review |
| `with_items` / `with_indexed_items` | `loop` + `loop_control.index_var` | 22 | Legacy but still supported; migrate for clarity |
| `stat: path=...` | `ansible.builtin.stat: { path: ... }` | 12 | Free-form args |
| `ignore_errors: yes` | `failed_when` / `block` + `rescue` | 20 | Do not hide real failures |
| `when: x == False` | `when: not x` | 22 | Literal comparison |
| `yes` / `no` | `true` / `false` | 24 | YAML truthiness |
| `user:` play keyword | `remote_user:` | 15 playbooks | `user` is still accepted but not the canonical keyword |
| `become_method: sudo` | `ansible.builtin.sudo` or omit | 15 playbooks | Lint schema prefers FQCN |
| `unarchive: copy: no` | `remote_src: true` | 3 | Clearer intent |
| `command` / `shell` | `ansible.builtin.command` with `argv`, or modules | 40 | Also add `creates`/`changed_when` |
| `ansible_*` facts | `ansible_facts.*` | As found | Modern fact access |
| `yum` | `ansible.builtin.dnf` | When OS prep is added | RHEL 8+ uses dnf |

Additional tasks:

- Verify the playbooks against `ansible-core` 2.20, 2.21, and 2.22 in CI. 2.22 catches the upcoming “failure inference from non-zero rc” deprecation early.
- Remove reliance on the removed `paramiko` connection plugin; use `ssh`.
- If using an internal Galaxy, confirm it supports the Galaxy v3 API (v2 was removed).
- Run `ansible-lint --fix` in a dedicated commit, then manually review every change.

Acceptance:

- `ansible-playbook --syntax-check` passes for all playbooks with only `ansible-core` + pinned collections.
- No deprecation warnings on 2.21.6.
- Lint profile `basic` passes; `no-free-form`, `fqcn`, `yaml[truthy]`, and `literal-compare` are at zero or explicitly waived.
- CI matrix covers 2.20/2.21/2.22.

**Important:** `with_items`, `ignore_errors`, and the `user:` keyword still function in 2.21. They are not blockers, but they are lint findings and modernization debt. The only hard Ansible 14 blocker found is the unqualified `archive` module.

---

### Phase 2 — Security and secrets (P0, ~1–2 weeks)

**Goal:** no plaintext credentials in the repository, logs, or world-readable files.

Current exposure:

- `roles/ofm-domain-defaults/defaults/main.yml` hardcodes `the old default password` for the SYS password, RCU password, NodeManager password, and AdminServer password.
- `roles/ofm-jdbc-datasource/defaults/main.yml` hardcodes `the old default password`.
- `boot.properties` renders the AdminServer password.
- RCU password files and `boot.properties` are created with `mode: "{{ mode }}"` (**0755**).
- Zero `no_log` tasks.
- WLST credential/key files are created via `storeUserConfig` without an explicit umask or mode.
- Downloads have no checksums.
- `-ignoreSysPrereqs` and `DECLINE_SECURITY_UPDATES=true` are used unconditionally.
- `pkill -9 -f {{ ofmDomainName }}` can kill unrelated processes.

Work items:

1. **Remove hardcoded passwords.** Replace them with required variables; fail fast in `prod`/`ppe` if they are unset. Example:
   - `ofm_admin_password`
   - `ofm_nodemanager_password`
   - `ofm_rcu_schema_password`
   - `ofm_db_sys_password`
   - `ofm_jdbc_password`
2. **Adopt Ansible Vault** (or an external secret manager) for environment secrets:
   - `group_vars/<env>/vault.yml` encrypted.
   - `vault_password_file` or `--vault-password-file` from CI/credential store, never committed.
   - `.gitignore` entries for vault password files, `.env`, artifacts, and media.
3. **Add `no_log: true`** to every task that templates, copies, or consumes a secret. Include `block/always` cleanup so failed tasks do not leave secret files behind.
4. **Prefer stdin over files for RCU.** Use `ansible.builtin.command` with `stdin` for the two RCU passwords; if a response file is unavoidable, set `0600`, own it by the Oracle user, and delete it in `always`.
5. **Fix file modes:**
   - `boot.properties`: `0600`.
   - `servers/<AdminServer>/security`: `0700`.
   - RCU response/password files: `0600`.
   - WLST `cred.secure` / `key.secure` / `nodemanager.config`: `0600`.
   - Stage directories: `0750`; media: `0640`; logs: `0750`.
   - Add `umask 077` to generated shell wrappers and WLST invocation environments.
6. **Add checksum verification** to every `get_url`: `checksum: "sha256:{{ ... }}"`, `timeout`, `retries`, `until`, and explicit `validate_certs`/`ca_path`.
7. **Remove or gate bypass flags:** `-ignoreSysPrereqs` and `DECLINE_SECURITY_UPDATES=true` should be opt-in variables, not defaults. Document the risk.
8. **Destructive-operation guards:**
   - `ofm_confirm_destroy: false` by default; clean playbooks assert it is `true`.
   - Refuse destructive runs unless `ofm_environment` is explicitly allowed.
   - Back up the domain (pack) and configuration before any clean/unpack.
   - Replace `pkill -9 -f` with a graceful NodeManager/AdminServer stop, a bounded wait, then a targeted kill using `pgrep -f` with an exact match.
9. **TLS and hostname verification:** the WLST script uses `SSLWLSWildcardHostnameVerifier` and disables two-way SSL. Keep the current behavior only if required; make it configurable and document the security trade-off.
10. **Secret handling design:** document that Vault protects data at rest, but decrypted values can still appear in temp files, process environments, or logs. `no_log` and cleanup are mandatory.

Acceptance:

- `grep -R "the old default password"` returns nothing.
- `grep -R "no_log" roles` shows coverage for every secret-bearing task.
- A `-vvv` run does not print passwords.
- `ansible-lint` `safety` profile passes (or waivers are documented).
- Clean playbooks refuse to run without explicit confirmation.
- No downloaded artifact is installed without a checksum.

---

### Phase 3 — Correctness, idempotency, and reliability (P1, ~2–3 weeks)

**Goal:** second runs are safe, predictable, and fast; failures are visible.

Work items:

1. **Fix verified defects** (see section 7):
   - Undefined `ofmMGDSRVexttemplate`.
   - OEM stage directory mismatch.
   - Pack/unpack artifact paths and missing NodeManager archive restore.
   - `ansible_env.HOME` under `become` (writes scripts to `/root/bin` when connecting as root).
   - Hardcoded `ofmAdminserverMachine`.
   - Infinite wait loops.
   - Trailing space in the `OFM-waitNodeManager.py` cleanup path.
   - Duplicate OEM playbooks.
2. **Install/domain markers.** Stop using “does the directory exist?” as the only check. Write a marker (for example `{{ oracleHome }}/.ofm-install.json`) containing product, version, patch level, media SHA256, and install timestamp. Verify the actual binary (`oracle_common/bin/rcu`, `bin/startWebLogic.sh`) as well.
3. **Multi-host orchestration.** `hosts: "{{ targetHosts }}"` is unsafe for domain creation:
   - RCU repository creation must run once (`run_once` or `delegate_to` the admin host).
   - Domain creation must run on the admin host only.
   - Managed-server creation must target each managed host with its own address.
   - Use inventory groups rather than a single `targetHosts`.
   - Add `serial: 1` for rolling restarts and `any_errors_fatal` where appropriate.
4. **Idempotent WLST.** Before `createServer`, `createMachine`, `createJDBCSystemResource`, or `createJDBCSystemResource`, check `getMBean(...)`. Re-running extension/configuration scripts must not fail on existing objects.
5. **Process lifecycle.** Replace `nohup ... &` shell wrappers with systemd units where possible, or use `async`/`poll: 0` plus `wait_for`. Add handlers for restart-on-change.
6. **Bounded waits.** The WLST wait scripts loop forever. Add a maximum attempt count and exit non-zero, or run them with `timeout` and `until`/`retries`. Fail with a clear message and log path.
7. **Pack/unpack round trip.**
   - Fetch the packed JAR and the NodeManager tarball to a controller-side artifacts directory (for example `{{ playbook_dir }}/artifacts/{{ inventory_hostname }}/`).
   - Do not use remote paths as controller paths.
   - Copy both artifacts to the target, unarchive the NodeManager tarball, and template `nodemanager.properties` / `nodemanager.domains`.
   - Verify the unpacked domain starts before considering the operation successful.
8. **Disk checks.** Replace `with_items` + `when: item.mount == ...` with a `selectattr` lookup and an explicit failure if the mount is absent. Update the required-space values to realistic product sizes; the current 2,095,005,696 bytes (~2 GB) is too low for a full FMW Infrastructure install.
9. **Check mode and tags.**
   - Add tags: `install`, `configure`, `extend`, `pack`, `unpack`, `clean`, `validate`, and `never` for destructive tasks.
   - Mark tasks that cannot support check mode with `check_mode: false`.
   - Add `--check` support for OS/Java/directory roles first.
10. **Remove dead code and duplicate logic.**
    - `OFM-env-domain` is unused.
    - `nodemanager.domains` / `nodemanager.properties` templates are unused.
    - Coherence variables are unused; the Coherence code is commented out.
    - `stageRequiredSpace` is unused.
    - Forms has duplicate `set_fact` branches that both set `Oracle Forms`.
    - `OFM-domain-oem.yml` and `OFM-oem-configure.yml` are identical.

Acceptance:

- A second run of install/configure reports `changed=0` (excluding unavoidable Oracle restarts, which are documented).
- Pack → fetch → unpack → start works on a clean lab host.
- Wait tasks fail within a bounded time with the relevant log path.
- `ansible-lint` profile `moderate` passes.
- No task silently skips a disk-space or preflight check.

---

### Phase 4 — Oracle platform modernization (P1/P2, ~3–5 weeks)

**Goal:** a supported, versioned Oracle platform with explicit prerequisites.

#### 4.1 Add an OS preparation role

The project currently assumes that the Oracle user, groups, packages, kernel parameters, limits, directories, and inventory pointer already exist. Add `ofm_os_prepare` (or `ofm_common`) covering:

- OS family/version assertion (RHEL/Oracle Linux 8/9/10).
- Required packages (for example `libaio`, `libnsl`, `ksh`, `make`, `gcc`, `glibc-devel`, `libstdc++-devel`, `sysstat`, `unzip`, `tar`, `curl`; adjust per FMW release).
- `oinstall`/`dba` groups and the `oracle` user with a controlled home and shell.
- `security/limits.d` entries (`nofile`, `nproc`, `stack`, `memlock`).
- `sysctl` values (`kernel.shmmax`, `kernel.shmall`, `kernel.sem`, `fs.file-max`, `net.core.rmem_max`, `net.ipv4.ip_local_port_range`).
- SELinux mode/booleans and firewalld ports, configurable.
- `/etc/hosts` entries for admin/managed hosts.
- Directory creation: `/u01/oracle/{product,config,log,transaction,stage}`, `/u01/oraInventory`, with ownership/modes.
- `/etc/oraInst.loc` and the central inventory pointer. **This is currently missing:** `oraInvPointer`, `orainvPointerTemplate`, and `oraInvDir` are defined but no template or task exists.
- Optional `/u01` mount handling via `ansible.posix.mount`.

#### 4.2 Add a versioned Java role

- Replace `ofm-java-8` with `ofm_java` or keep `ofm_java_8` and add `ofm_java_17`.
- Variables: `ofm_java_version`, `ofm_java_release`, `ofm_java_archive`, `ofm_java_sha256`, `ofm_java_home`.
- Install from a checksummed archive, set alternatives/profile.d, and validate `java -version`.
- For 12.2.1.4: latest certified 8u (8u211+ minimum).
- For 14.1.2: JDK 17.0.12+ or 21.0.4+ as certified.

#### 4.3 Introduce a software catalog

Replace hardcoded media names and versions with a versioned catalog:

```yaml
ofm_release: "12.2.1.4"
ofm_rcu_version: "12.2.1.4.0"
ofm_media:
  infrastructure:
    archive: "<media-zip-name>.zip"
    installer: "fmw_12.2.1.4.0_infrastructure.jar"
    sha256: "<sha256>"
  forms:
    archive: "<media-zip-name>.zip"
    installer: "fmw_12.2.1.4.0_fr_linux64.bin"
    sha256: "<sha256>"
  ohs:
    archive: "<media-zip-name>.zip"
    installer: "fmw_12.2.1.4.0_ohs_linux64.bin"
    sha256: "<sha256>"
```

- Parameterize RCU response file names, WLST script names, and install response file names by `ofm_release`.
- Remove hardcoded `12.2.1.2` strings from templates, defaults, task names, and response files.
- Add a `mediasource: filesystem` branch that copies from a local artifact repository with checksum; the current code only implements `webserver`.

#### 4.4 Tactical upgrade: 12.2.1.2 → 12.2.1.4

- Validate 12.2.1.4 media and response files.
- Upgrade to the latest certified JDK 8.
- Confirm RCU components and Forms 12.2.1.19 compatibility.
- Test on RHEL 8.10 and RHEL 9.x.
- Document the 12c end-of-support timeline (Premier Dec 2026, Extended Dec 2027).
- Decide whether Forms remains on 12.2.1.19 until the next FMW suite release.

#### 4.5 Strategic upgrade: 14.1.2

- Create a versioned role path (for example `ofm_infra_1412`) or a single role that loads `vars/12.2.1.4.yml` / `vars/14.1.2.yml`.
- Validate WLST/Jython compatibility. Do not convert WLST scripts to Python 3 unless the target WebLogic release certifies it.
- Validate RCU 14.1.2 components and response files.
- Use JDK 17/21 as certified.
- Confirm Forms/OHS availability in 14.1.2 before committing; otherwise plan Forms for the next FMW release.
- Add a migration runbook and a rollback plan using domain pack/unpack.

Acceptance:

- OS preparation is idempotent and passes `--check`.
- A clean RHEL 8/9 host can install 12.2.1.4 end-to-end from the catalog.
- No hardcoded version or host remains in defaults/tasks/templates.
- 14.1.2 proof-of-concept succeeds in the lab (or a documented gap list with dates).
- The support matrix in the README matches the tested combinations.

---

### Phase 5 — Engineering quality and CI (P2, continuous)

**Goal:** make the project maintainable by more than one person.

Work items:

1. **Role contracts.** Add `meta/argument_specs.yml` to all 17 roles: types, required flags, defaults, choices. This catches bad inventory early.
2. **Role naming.** Rename roles to snake_case without version suffixes where possible:
   - `ofm-domain-base-122` → `ofm_domain_base` (or `ofm_domain_base_122` if the version must remain).
   - `ofm-java-8` → `ofm_java_8`.
   - `defaults` → `ofm_common`.
   - Update all dependencies and playbooks. If renaming is too disruptive, temporarily waive `role-name` in `.ansible-lint` with an owner and expiry.
3. **Variable naming.** Move to snake_case (`ofm_domain_name`, `ofm_admin_password`, `ofm_media_url`, `ofm_dir_mode`, `ofm_environment`). Provide a compatibility layer for one major release:
   - New canonical vars in defaults.
   - Old camelCase names mapped as aliases where feasible.
   - `docs/variable-migration.md` with the full mapping.
   - Remove aliases in v2.0.
4. **Molecule scenarios:**
   - `os_prepare`, `java`, `lint`, `syntax` on `rockylinux9`/`ubi9` containers.
   - Mock Oracle media and response files for role-logic tests.
   - A `--check` scenario for idempotent roles.
   - Keep licensed Oracle integration tests on a self-hosted lab runner with read-only media mounts.
5. **CI matrix:**
   - ansible-core 2.20, 2.21, 2.22.
   - Python 3.12/3.13 on the controller.
   - `ansible-lint` profile `basic` → `moderate` → `production` over time.
   - `yamllint`, `pre-commit`, `detect-secrets`, `check-added-large-files`.
   - Syntax-check every playbook with the example inventory.
6. **Execution Environment:**
   - `execution-environment.yml` built with `ansible-builder`.
   - Pin ansible-core, collections, Python, and system dependencies.
   - `ansible-navigator.yml` for local runs.
   - Never bake licensed Oracle media into the EE.
7. **Documentation:**
   - `README.md`: purpose, support matrix, prerequisites, quick start, inventory, variables, secrets, runbooks.
   - `docs/architecture.md`, `docs/prerequisites.md`, `docs/inventory.md`, `docs/variables.md`, `docs/secrets.md`, `docs/runbooks.md`, `docs/troubleshooting.md`, `docs/upgrade-12c-to-14c.md`.
   - `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`.
8. **Release management:**
   - SemVer tags: `v0.1` baseline, `v0.2` Ansible 14 compatible, `v0.3` secure, `v0.4` idempotent, `v1.0` 12.2.1.4/RHEL 8-9, `v2.0` 14.1.2/JDK 17-21.
   - Changelog entries for breaking variable/role changes.
   - Deprecation policy: one major release of overlap.

Acceptance:

- CI green on the supported matrix.
- Molecule scenarios pass.
- `ansible-lint` profile `production` passes for v2.0.
- Docs let a new engineer run the example inventory without reading the code.
- EE builds reproducibly.

---

### Phase 6 — Operations and lifecycle (P2/P3, ongoing)

- **Backup and rollback:** pack the domain before changes, store artifacts with retention, test restore, and document the rollback procedure.
- **Observability:** health checks for AdminServer (`/management` or console), NodeManager port (`wait_for`), OHS (`uri`/`curl`); log locations and troubleshooting commands.
- **AAP/AWX:** use inventories, credentials, surveys, RBAC, and the EE; remove the `targetHosts` extra-var pattern.
- **Lifecycle cadence:** review Ansible/collections quarterly; plan Ansible 15/core 2.22, FMW 27, Java 25, and RHEL 10.
- **Deprecation:** remove old variable aliases and roles in v2.0; publish the migration guide.

---

## 5. Prioritized backlog

Effort is indicative for one experienced Ansible/Oracle engineer, including review and documentation.

| ID | Work item | Priority | Phase | Effort |
|---|---|---|---|---:|
| P0-01 | Scaffolding: `ansible.cfg`, `requirements.yml`, inventory example, CI skeleton, README | P0 | 0 | 2–3 d |
| P0-02 | Secrets: vault, `no_log`, file modes, RCU stdin, cleanup | P0 | 2 | 4–5 d |
| P0-03 | Destructive-operation guards, backups, replace `pkill -9` | P0 | 2 | 2–3 d |
| P0-04 | `archive` collection/FQCN fix; core-only syntax gate | P0 | 1 | 2–3 d |
| P1-01 | Loops, free-form args, booleans, literal compares, `remote_user`, become | P1 | 1 | 3–4 d |
| P1-02 | Make 40 `command`/`shell` tasks idempotent (`argv`, `creates`, `changed_when`) | P1 | 3 | 5–8 d |
| P1-03 | Handlers, systemd/async lifecycle, bounded waits | P1 | 3 | 4–6 d |
| P1-04 | Fix known defects (undefined var, OEM stage, HOME, admin host, trailing space) | P1 | 3 | 5–8 d |
| P1-05 | Multi-host orchestration: groups, `run_once`, `delegate_to`, `serial` | P1 | 3 | 4–6 d |
| P1-06 | Pack/unpack round trip and artifact handling | P1 | 3 | 3–4 d |
| P2-01 | `ofm_os_prepare` role (packages, users, limits, sysctl, dirs, `oraInst.loc`) | P1 | 4 | 5–7 d |
| P2-02 | Versioned Java role and software catalog | P1 | 4 | 3–4 d |
| P2-03 | 12.2.1.4 tactical upgrade and RHEL 8/9 validation | P1 | 4 | 5–8 d |
| P2-04 | 14.1.2 design and proof of concept | P2 | 4 | 15–20 d |
| P2-05 | Forms/OHS upgrade plan and validation | P2 | 4 | 5–10 d |
| P3-01 | `meta/argument_specs.yml` for all roles | P2 | 5 | 3–4 d |
| P3-02 | Role/variable rename with compatibility layer | P2 | 5 | 5–8 d |
| P3-03 | Molecule scenarios and mock media fixtures | P2 | 5 | 5–8 d |
| P3-04 | CI matrix and Execution Environment | P2 | 5 | 3–5 d |
| P3-05 | Documentation set, README, CHANGELOG, LICENSE | P2 | 5 | 3–4 d |
| P3-06 | SemVer release and deprecation policy | P2 | 5 | 1–2 d |
| P4-01 | Backup/restore and rollback runbook | P2 | 6 | 3–5 d |
| P4-02 | Health checks and observability | P3 | 6 | 2–3 d |
| P4-03 | AAP/AWX integration | P3 | 6 | 5–8 d |
| P4-04 | Lifecycle review cadence | P3 | 6 | ongoing |

---

## 6. Milestones

| Milestone | Outcome | Indicative timing | Version |
|---|---|---|---|
| M0 — Bootstrap | Reproducible tooling, inventory, lint/CI baseline | Week 1 | v0.1 |
| M1 — Ansible 14 compatible | Core-only syntax passes, FQCN/loops/style fixed, no deprecations | Weeks 2–3 | v0.2 |
| M2 — Secure | No plaintext secrets, `no_log`, modes, checksums, destructive guards | Weeks 3–4 | v0.3 |
| M3 — Idempotent and reliable | Second run `changed=0`, bounded waits, multi-host safe, pack/unpack fixed | Weeks 5–7 | v0.4 |
| M4 — 12.2.1.4 on RHEL 8/9 | OS prep, Java, catalog, end-to-end install | Weeks 8–10 | v1.0 |
| M5 — 14.1.2 | JDK 17/21, RCU 14.1.2, new suite path, Forms/OHS decision | Weeks 11–16 | v2.0 |
| Continuous | Lint `production`, EE, AAP/AWX, lifecycle reviews | Ongoing | — |

Timing assumes lab access, licensed media, and one engineer. Add 30–50% if the environment must be built from scratch.

---

## 7. Known defects (verified)

| ID | Severity | Location | Issue | Fix | Phase |
|---|---|---|---|---|---|
| D-01 | Critical | `roles/ofm-domain-defaults/defaults/main.yml:28,30,34,42`; `roles/ofm-jdbc-datasource/defaults/main.yml:11` | Hardcoded `the old default password` passwords | Required vaulted vars; fail in prod if unset | 2 |
| D-02 | Critical | `roles/ofm-domain-base-122/tasks/main.yml:67–71,138–142`; `roles/ofm-domain-clean/tasks/main.yml:35–39` | RCU password files and `boot.properties` created `0755` | `0600`/`0700`, `no_log`, `block/always` cleanup | 2 |
| D-03 | Critical | All roles | Zero `no_log` tasks | Add to every secret task | 2 |
| D-04 | Critical | `roles/ofm-domain-pack/tasks/main.yml:29` | `archive` is unresolved without `community.general` | Pin collection or use FQCN | 1 |
| D-05 | High | `roles/ofm-domain-managedserver/tasks/main.yml:35` | `ofmMGDSRVexttemplate` is undefined | Remove or define; add `argument_specs` | 3 |
| D-06 | High | `roles/ofm-domain-oem-122/tasks/main.yml:21–23,49–58` | Creates `{{ stageDir }}` but writes to `{{ ofmDomainStageDir }}` | Create the correct directory | 3 |
| D-07 | High | `roles/ofm-domain-pack/tasks/main.yml:34–36`; `roles/ofm-domain-unpack/tasks/main.yml:23–24` | Controller `fetch`/`copy` destinations use remote paths | Use a controller artifact directory | 3 |
| D-08 | High | `roles/ofm-domain-pack/tasks/main.yml:28–31`; `roles/ofm-domain-unpack/tasks/main.yml` | NodeManager tarball is created but never fetched/restored; `nodemanager.*` templates are unused | Fetch, copy, unarchive, template, verify | 3 |
| D-09 | High | `roles/defaults/defaults/main.yml:12`; many user-home paths | `ansible_env.HOME` is evaluated for the connecting user, not `become_user` | Use `ofm_user_home` or `getent passwd oracle` | 3 |
| D-10 | High | `roles/ofm-domain-defaults/defaults/main.yml:41` | `ofmAdminserverMachine` is hardcoded | Derive from inventory/`ansible_fqdn` | 3 |
| D-11 | High | `roles/ofm-domain-clean/tasks/main.yml:13` | `pkill -9 -f {{ ofmDomainName }}` can kill unrelated processes | Graceful stop, bounded wait, exact match | 2 |
| D-12 | High | `roles/ofm-infra-122/tasks/main.yml:18–35` (and Forms/OHS/OEM) | Disk assert is skipped when the mount is absent; required space (~2 GB) is too low | `selectattr` + explicit failure + realistic sizes | 3 |
| D-13 | High | `roles/ofm-installation-defaults/defaults/main.yml:14–16` | `oraInst.loc`/inventory variables are declared but never created | Add template and task | 4 |
| D-14 | High | All playbooks (`hosts: "{{ targetHosts }}"`) | No `run_once`/`delegate_to`; RCU and domain creation collide on multi-host runs | Inventory groups, delegation, `serial` | 3 |
| D-15 | High | `roles/ofm-installation-clean/tasks/main.yml:33–45`; `roles/ofm-domain-clean/tasks/main.yml` | Destructive clean has no confirmation or backup | `ofm_confirm_destroy`, backup, environment guard | 2 |
| D-16 | High | `roles/ofm-domain-base-122/templates/OFM-waitAdminServer.py`, `OFM-waitNodeManager.py` | Infinite `while` loops with no timeout | Bounded retries, exit non-zero, log path | 3 |
| D-17 | Medium | `roles/ofm-infra-122/tasks/main.yml:61–66` (and Forms/Java/OHS) | `mediassource: filesystem` is documented but not implemented | Add local artifact copy branch | 4 |
| D-18 | Medium | `roles/ofm-domain-forms-122/tasks/main.yml:27,33`; `roles/ofm-domain-managedserver/templates/OFM-12.2-createManagedServer.py:26–27` | Duplicate `set_fact` branches; server groups never applied | Remove dead branch; implement or delete groups | 3 |
| D-19 | Medium | `roles/ofm-domain-base-122/tasks/main.yml:347` | Trailing space in `OFM-waitNodeManager.py ` path | Fix path | 3 |
| D-20 | Medium | `OFM-domain-oem.yml`, `OFM-oem-configure.yml` | Byte-identical duplicate playbooks | Keep one, deprecate the other | 3 |
| D-21 | Medium | `roles/ofm-domain-defaults/defaults/main.yml:23–24`; `roles/ofm-jdbc-datasource/defaults/main.yml:7` | `ofmJdbcURL` vs `ofmJDBCURL` naming collision; TNS URL is unused | Standardize names | 3 |
| D-22 | Low | `roles/ofm-domain-base-122/templates/OFM-env-domain`; Coherence vars; `stageRequiredSpace` | Dead templates/variables | Remove or implement | 3 |
| D-23 | Low | `README.md` | Truncated at “Check for exaples”; no usage/matrix | Rewrite | 0 |
| D-24 | Low | All `OFM-*.yml` | Executable bit on YAML files; hundreds of trailing spaces | Normalize permissions/whitespace | 0 |

---

## 8. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Oracle media is licensed and not in CI | Cannot run full install tests in public CI | Keep media external; mock fixtures for logic tests; self-hosted lab runner |
| 12c Premier Support ends Dec 2026 | Unsupported platform, security exposure | Start 12.2.1.4 upgrade immediately; plan 14.1.2 |
| RHEL 7 is EOL | No patches; ansible-core 2.21 requires Python 3.9+ | Move to RHEL 8/9; temporary Python 3.9 exception with exit date |
| Secret migration breaks existing runs | Failed deployments | Compatibility aliases, staged rollout, vaulted example, runbook |
| Variable/role renames break consumers | Playbook failures | One major release of aliases; migration guide; deprecation warnings |
| Multi-host race conditions | Corrupted domain/RCU | `run_once`/`delegate_to`, inventory groups, `serial`, idempotency markers |
| WLST is Python 2-style | Cannot simply modernize to Python 3 | Keep Jython-compatible WLST for 12c/14c; validate per WebLogic release |
| Ansible 15/core 2.22 churn | Future breakage | CI matrix includes 2.22; pin production to 14.6.0 |
| No integration environment | Bugs found late | Build a lab; add molecule + smoke tests; pack/unpack round trip |
| Destructive clean runs accidentally | Data loss | Explicit confirmation, environment guard, backups, `never` tag |

---

## 9. Decision points

These need an owner decision before Phase 4:

1. **Minimum supported platform:** Is RHEL 8/9 the floor, or must RHEL 7 remain for a defined period? If RHEL 7 remains, what is the exit date and Python 3.9 plan?
2. **FMW track:** Is 12.2.1.4 the required near-term target, or can the team go directly to 14.1.2? Direct 14.1.2 is cleaner but may be blocked by Forms/OHS/app certification.
3. **Forms & Reports:** Confirm whether Forms 14.1.2 is available/certified for the suite, or whether Forms stays on 12.2.1.19 until FMW 27.
4. **Secrets backend:** Ansible Vault only, or integrate HashiCorp Vault / CyberArk / cloud secret manager? This affects CI and AAP credentials.
5. **Rename strategy:** Big-bang snake_case rename in v1.0, or one release of compatibility aliases? Recommended: aliases for one major release.
6. **Deployment target:** CLI only, or Ansible Automation Platform/AWX with Execution Environments? If AAP, plan surveys, RBAC, and credential types.
7. **Supported Ansible versions:** Production on 14.6.0 only, or support 2.20/2.21/2.22? Recommended: production 14.6.0; CI tests 2.21/2.22.

---

## 10. Definition of done

### v1.0 — FMW 12.2.1.4 on RHEL 8/9

- [ ] All playbooks pass syntax-check with core + pinned collections.
- [ ] `ansible-lint` profile `moderate` passes; no unresolved waivers.
- [ ] No plaintext secrets; vaulted inventory; `no_log` coverage; `0600`/`0700` modes.
- [ ] Destructive clean requires explicit confirmation and creates a backup.
- [ ] Second run of install/configure is `changed=0` except documented Oracle restarts.
- [ ] OS prep and Java roles are idempotent and check-mode clean.
- [ ] 12.2.1.4 install, domain creation, Forms/OHS extension, pack/unpack work on RHEL 8 and 9.
- [ ] Multi-host run creates RCU/domain once and managed servers per host.
- [ ] README, inventory example, variable reference, secrets guide, and runbooks are complete.
- [ ] CI green on the supported matrix.

### v2.0 — FMW 14.1.2 / JDK 17 or 21

- [ ] 14.1.2 install path validated in the lab.
- [ ] RCU 14.1.2 and response files validated.
- [ ] JDK 17/21 role and certification documented.
- [ ] Forms/OHS path decided and documented.
- [ ] `ansible-lint` profile `production` passes.
- [ ] Execution Environment builds reproducibly.
- [ ] Deprecated variable/role aliases removed with a migration guide.

---

## Appendix A — Verification log

Environment used for this assessment (throwaway, not committed):

```text
Python 3.12.13
ansible-core 2.21.6
ansible-lint 26.11.0
community.general 14.0.1
```

Commands:

```bash
python3.12 -m venv /tmp/opencode/ansible-venv
/tmp/opencode/ansible-venv/bin/pip install 'ansible-core==2.21.6' ansible-lint
/tmp/opencode/ansible-venv/bin/ansible-galaxy collection install community.general -p /tmp/opencode/collections

ANSIBLE_COLLECTIONS_PATH=/tmp/opencode/collections \
  ansible-playbook -i inventories/example/hosts.yml --syntax-check OFM-*.yml

ANSIBLE_COLLECTIONS_PATH=/tmp/opencode/collections ansible-lint
```

Observed:

- 15/15 syntax-check OK with the example inventory + `community.general`.
- `OFM-domain-pack.yml` fails without `community.general` (`archive` unresolved).
- 14/15 fail without `targetHosts`/`unpackHosts` defined.
- 1,385 lint findings; top rules listed in section 1.
- 0 `no_log`, 0 `tags`, 0 `handlers`.
- 40 `command`/`shell` tasks, 22 `with_*` loops, 12 free-form `stat` calls, 20 `ignore_errors`.

---

## Appendix B — Recommended repository layout

```text
ansible-oracle-fusion-middleware/
├── ansible.cfg
├── requirements.yml
├── requirements-dev.txt
├── .ansible-lint
├── .yamllint
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── CONTRIBUTING.md
├── execution-environment.yml
├── ansible-navigator.yml
├── site.yml                      # optional umbrella playbook
├── playbooks/
│   ├── java-install.yml
│   ├── infrastructure-install.yml
│   ├── forms-install.yml
│   ├── ohs-install.yml
│   ├── domain-configure.yml
│   ├── domain-pack.yml
│   ├── domain-unpack.yml
│   ├── domain-clean.yml
│   └── installation-clean.yml
├── inventories/
│   ├── example/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── vault.yml.example
│   ├── dev/
│   ├── test/
│   └── prod/
├── roles/
│   ├── ofm_common/
│   ├── ofm_os_prepare/
│   ├── ofm_java_8/
│   ├── ofm_java_17/
│   ├── ofm_infra_122/
│   ├── ofm_forms_122/
│   ├── ofm_ohs_122/
│   ├── ofm_domain_base/
│   ├── ofm_domain_managedserver/
│   ├── ofm_domain_forms/
│   ├── ofm_domain_oem/
│   ├── ofm_jdbc_datasource/
│   ├── ofm_ldap_integration/
│   ├── ofm_domain_pack/
│   ├── ofm_domain_unpack/
│   ├── ofm_domain_clean/
│   └── ofm_installation_clean/
├── docs/
│   ├── architecture.md
│   ├── prerequisites.md
│   ├── inventory.md
│   ├── variables.md
│   ├── secrets.md
│   ├── runbooks.md
│   ├── troubleshooting.md
│   ├── upgrade-12c-to-14c.md
│   └── variable-migration.md
├── molecule/
│   ├── os_prepare/
│   ├── java/
│   └── syntax/
├── extensions/
│   └── molecule/
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Appendix C — Ansible 14 upgrade runbook

```bash
# 1. Controller: Python 3.12+ and a pinned virtual environment
python3.12 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install 'ansible==14.6.0' 'ansible-lint==26.11.0' yamllint

# 2. Collections
ansible-galaxy collection install -r requirements.yml

# 3. Verify
ansible --version
ansible-lint --version

# 4. Syntax-check every playbook with the example inventory
ansible-playbook -i inventories/example/hosts.yml --syntax-check playbooks/*.yml

# 5. Lint (start at basic; raise the profile over time)
ansible-lint
```

Recommended migration order:

1. Add scaffolding and pin versions.
2. Add the example inventory and remove required `targetHosts`.
3. Add `requirements.yml` and fix `archive`/FQCN.
4. Remove secrets and add vault/`no_log`/modes.
5. Make `command`/`shell` idempotent.
6. Fix the known defects and multi-host orchestration.
7. Add OS prep, Java, and the software catalog.
8. Add molecule/CI and documentation.
9. Cut over to 12.2.1.4 on RHEL 8/9.
10. Plan 14.1.2 with JDK 17/21.

---

## Appendix D — References

- Ansible 14.6.0 release announcement (2026-11-04): <https://forum.ansible.com/t/release-announcement-ansible-community-package-14-6-0/46599>
- Ansible releases and maintenance: <https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html>
- Ansible-core 2.21 porting guide: <https://docs.ansible.com/projects/ansible/latest/porting_guides/porting_guide_core_2.21.html>
- Ansible-core 2.19 porting guide: <https://docs.ansible.com/projects/ansible/latest/porting_guides/porting_guide_core_2.19.html>
- Oracle Fusion Middleware Statement of Direction (June 2026): <https://www.oracle.com/a/ocom/docs/middleware/fusion-middleware-statement-of-direction.pdf>
- Oracle FMW 12.2.1.4 system requirements: <https://docs.oracle.com/en/middleware/fusion-middleware/12.2.1.4/sysrs/system-requirements-and-specifications.html>
- Oracle WebLogic Server 14.1.2 what's new: <https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/14.1.2/notes/whatsnew.html>
- Oracle WebLogic Server 15.1.1 what's new: <https://docs.oracle.com/en/middleware/standalone/weblogic-server/15.1.1/notes/whatsnew.html>
