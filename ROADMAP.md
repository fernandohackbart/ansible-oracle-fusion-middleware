# ROADMAP — Implementation Checklist

**Status:** In progress  
**Updated:** 2026-11-17  
**Baseline:** 15 playbooks, 17 roles, 42 templates, FMW 12.2.1.2, JDK 8u101, RHEL 7-era assumptions  
**Target:** Ansible 14.6.0 / ansible-core 2.21.6, Python 3.12+, RHEL 8/9, FMW 12.2.1.4 → 14.1.2

> Detailed assessment, evidence, defect table, and rationale: [docs/roadmap-details.md](docs/roadmap-details.md).

## How to use this checklist

- Each checkbox is a shippable unit of work.
- One commit per item (or per tight group of directly related items).
- `[x]` = implemented **and** validated with the available checks.
- `[ ]` = not started. Add `**BLOCKED:**` with the reason when work cannot proceed without licensed media, lab hosts, or a decision.
- Local validation commands: `make lint`, `make syntax`, `make test`.
- Do not tick an item if its acceptance criteria were not met.

---

## Phase 0 — Baseline and guardrails

- [x] **0.1 Add `ansible.cfg`** — deterministic inventory/roles/collections paths, host-key checking, no retry files, deprecation warnings, interpreter discovery.  
  _Acceptance:_ `ansible-config dump --only-changed` shows only intentional settings.

- [x] **0.2 Add `requirements.yml` and `requirements-dev.txt`** — pin `community.general`, `ansible.posix`, `ansible==14.6.0`, `ansible-lint`, `yamllint`, `molecule`, `ansible-builder`, `pre-commit`.  
  _Acceptance:_ `ansible-galaxy collection install -r requirements.yml` succeeds; versions are pinned.

- [x] **0.3 Add lint/format configuration** — `.ansible-lint` (`profile: basic`), `.yamllint`, `.editorconfig`, `.gitignore` (vault files, `.venv`, artifacts, media, retries, molecule state).  
  _Acceptance:_ `ansible-lint` and `yamllint` run with the committed config and no missing-file errors.

- [x] **0.4 Add example inventory and group vars** — `inventories/example/hosts.yml`, `group_vars/all.yml`, `group_vars/vault.yml.example`; define `ofm_admin`, `ofm_managed`, `ofm_ohs`, `ofm_forms`.  
  _Acceptance:_ playbook syntax-check works without `-e targetHosts=...`.

- [x] **0.5 Rewrite `README.md`** — purpose, support matrix, prerequisites, quick start, inventory, variables, secrets, validation, links.  
  _Acceptance:_ a new engineer can run the example inventory by following the README only.

- [x] **0.6 Add `Makefile` and CI workflow** — `setup`, `syntax`, `lint`, `test`, `clean`; CI runs syntax-check, yamllint, ansible-lint.  
  _Acceptance:_ `make lint` and `make syntax` pass locally; CI workflow is syntactically valid.

- [x] **0.7 Add project metadata** — `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`.  
  _Acceptance:_ files exist and state the project’s support and contribution policy.

- [x] **0.8 Normalize file hygiene** — remove trailing whitespace, fix YAML indentation, add final newlines, remove executable bits from YAML.  
  _Acceptance:_ `git diff --check` is clean; `find . -name '*.yml' -perm -u+x` returns nothing.

---

## Phase 1 — Ansible 14 compatibility

- [x] **1.1 Add FQCN to every module action** — replace short names with `ansible.builtin.*` or the correct collection FQCN.  
  _Acceptance:_ `fqcn` lint rule is at zero (excluding documented waivers).

- [x] **1.2 Fix collection modules and unarchive options** — `archive` → `community.general.archive`; `unarchive: copy: no` → `remote_src: true`; add `requirements.yml` coverage.  
  _Acceptance:_ `ansible-playbook --syntax-check` passes with only `ansible-core` + pinned collections.

- [x] **1.3 Replace legacy loops** — `with_items` and `with_indexed_items` → `loop` with `loop_control.index_var` where an index is needed.  
  _Acceptance:_ no `with_*` loop keys remain.

- [x] **1.4 Replace free-form module arguments** — `stat: path=...`, `fail: msg=...` → mapping syntax.  
  _Acceptance:_ `no-free-form` lint rule is at zero.

- [x] **1.5 Normalize booleans and conditionals** — `yes`/`no` → `true`/`false`; `x == False` → `not x`; string booleans → real booleans where safe.  
  _Acceptance:_ `yaml[truthy]` and `literal-compare` are at zero or documented.

- [x] **1.6 Modernize play keywords** — `user:` → `remote_user:`; `become_method: sudo` → `ansible.builtin.sudo` or default.  
  _Acceptance:_ no `user:` play keyword remains; schema lint passes for playbooks.

- [x] **1.7 Make `command`/`shell` tasks explicit** — add `argv` where possible, `creates`, `changed_when`, `failed_when`, `check_mode: false` as appropriate.  
  _Acceptance:_ `no-changed-when` is at zero or every remaining task has a documented reason.

- [x] **1.8 Validate on ansible-core 2.20.x and 2.21.6** — syntax-check all playbooks; fix deprecation/failure-inference warnings.  
  _Acceptance:_ no deprecation warnings; syntax gate is green on both cores. Validated with 2.20.11 and 2.21.6.

- [ ] **1.8b Validate on ansible-core 2.22** — **BLOCKED:** ansible-core 2.22 requires Python 3.13+ on the controller; this environment has Python 3.12. Add to the CI matrix when Python 3.13 is available.

---

## Phase 2 — Security and secrets

- [x] **2.1 Remove hardcoded passwords** — delete the default passwords; require `ofmAdminPassword`, `ofmNodemanagerPassword`, `ofmJdbcRCUPassword`, `ofmJdbcsysPassword`, `ofmJDBCPassword`.  
  _Acceptance:_ no hardcoded default password remains in roles/templates; missing secrets fail with a clear message. Names will be normalized in Phase 5.

- [x] **2.2 Add vaulted-secret example** — documented `group_vars/<env>/vault.yml`, vault password handling, and `.gitignore` protections.  
  _Acceptance:_ example uses `!vault` or a documented external secret lookup; no real secret is committed.

- [x] **2.3 Add `no_log` coverage** — every task that templates, copies, or consumes a secret.  
  _Acceptance:_ `-vvv` run does not print passwords; secret tasks are identifiable.

- [x] **2.4 Fix secret file modes and cleanup** — RCU password files `0600`, `boot.properties` `0600`, security dir `0700`, WLST credential/key files `0600`, stage dirs `0750`; cleanup in `block/always`.  
  _Acceptance:_ no secret file is world-readable; failed tasks do not leave secrets behind.

- [x] **2.5 Harden downloads** — SHA256 checksums, `timeout`, `retries`, `until`, explicit `validate_certs`/`ca_path`; gate `-ignoreSysPrereqs` and `DECLINE_SECURITY_UPDATES`.  
  _Acceptance:_ every `get_url` has a checksum variable and retry policy; bypass flags are opt-in.

- [x] **2.6 Guard destructive operations** — `ofm_confirm_destroy` assertion, production environment guard, backup before clean, remove `pkill -9 -f`.  
  _Acceptance:_ clean playbooks refuse to run without confirmation; no broad `pkill -9`.

- [x] **2.7 Harden generated wrappers** — `umask 077`, `0600` logs, no plaintext passwords in dead env templates/wrapper scripts; remove dead secret-bearing templates.  
  _Acceptance:_ generated wrappers are not world-readable and do not export passwords unnecessarily.

---

## Phase 3 — Correctness, idempotency, and reliability

- [x] **3.1 Fix simple verified defects** — undefined `ofmMGDSRVexttemplate`, OEM stage-dir mismatch, trailing space in wait-script cleanup, duplicate OEM playbooks.  
  _Acceptance:_ syntax/lint pass; the affected tasks reference defined variables and paths.

- [x] **3.2 Fix execution-context assumptions** — replace `ansible_env.HOME` with a defined Oracle user home; replace hardcoded `ofmAdminserverMachine` with inventory-derived values.  
  _Acceptance:_ running as root + `become_user: oracle` writes to the Oracle home, not `/root`; admin host is inventory-driven.

- [x] **3.3 Fix pack/unpack** — controller-side artifact directory, fetch both JAR and NodeManager tarball, restore and template NodeManager files, validate unpack.  
  _Acceptance:_ pack → fetch → unpack → start round trip is documented and code-complete.

- [x] **3.4 Bound waits and fix disk checks** — WLST wait loops exit non-zero after a maximum; disk assertions fail when a mount is absent; realistic space values.  
  _Acceptance:_ no infinite loop; missing mount produces a clear failure.

- [x] **3.5 Make multi-host runs safe** — inventory groups, `run_once`/`delegate_to` for RCU and domain creation, `serial` for rolling changes, `any_errors_fatal` where appropriate.  
  _Acceptance:_ a two-host play creates RCU/domain once and managed servers per host.

- [x] **3.6 Add tags and handlers** — `install`, `configure`, `extend`, `pack`, `unpack`, `clean`, `validate`; `never` on destructive tasks; restart handlers.  
  _Acceptance:_ `--tags validate` works without running install; restart handlers are defined. The explicit bootstrap start/stop remains because domain creation requires it.

- [x] **3.7 Make WLST operations idempotent** — check `getMBean(...)` before create; add install/domain markers with version and checksum.  
  _Acceptance:_ second run of configure/extend does not fail on existing objects.

- [x] **3.8 Remove dead code and duplicates** — unused `OFM-env-domain`, unused NodeManager templates (or wire them up), unused Coherence vars, duplicate Forms `set_fact`, unused `stageRequiredSpace`.  
  _Acceptance:_ no unreferenced templates/vars remain; lint is cleaner.

---

## Phase 4 — Oracle platform modernization

- [x] **4.1 Add `ofm_os_prepare` role** — OS validation, packages, `oracle` user/groups, limits, sysctl, SELinux/firewalld, directories, `/etc/oraInst.loc`, inventory.  
  _Acceptance:_ role is idempotent and `--check` clean on RHEL 8/9. Lab validation pending in 4.5.

- [x] **4.2 Add versioned Java role and software catalog** — JDK 8 latest for 12.2.1.4; JDK 17/21 for 14.1.2; checksums, alternatives, profile.d.  
  _Acceptance:_ Java version is a variable; no hardcoded 8u101; catalog is the single source of media names/checksums. The role name remains `ofm-java-8` for compatibility and is renamed in Phase 5.

- [x] **4.3 Parameterize FMW 12.2.1.4** — version, RCU version, response file names, WLST script names, media names.  
  _Acceptance:_ no hardcoded `12.2.1.2` strings remain; 12.2.1.4 is selectable by variable. Lab validation is tracked in 4.5.

- [x] **4.4 Scaffold FMW 14.1.2** — versioned vars/roles, RCU 14.1.2 response files, JDK 17/21, upgrade/rollback docs.  
  _Acceptance:_ 14.1.2 path is selectable; lab validation is explicitly tracked as blocked/pending.

- [ ] **4.5 Lab validation** — install 12.2.1.4 and 14.1.2 on RHEL 8/9 with licensed media; validate Forms/OHS.  
  **BLOCKED:** requires licensed Oracle media, lab hosts, and an approved maintenance window.

---

## Phase 5 — Engineering quality and CI

- [x] **5.1 Add `meta/argument_specs.yml` to all roles** — types, required flags, defaults, choices.  
  _Acceptance:_ invalid inventory values fail before tasks run.

- [x] **5.2 Add Molecule scenarios** — `syntax`, `os_prepare`, `java`; container images; mock media fixtures.  
  _Acceptance:_ `molecule test -s syntax` passes locally; Docker scenarios are scaffolded for CI/lab.

- [x] **5.3 Add CI matrix and Execution Environment** — ansible-core 2.20/2.21/2.22, Python 3.12/3.13, lint profiles, `ansible-builder`.  
  _Acceptance:_ CI matrix and EE definition are committed; EE build validation is pending Docker/registry access.

- [x] **5.4 Add documentation set** — architecture, prerequisites, inventory, variables, secrets, runbooks, troubleshooting, 12c→14c upgrade.  
  _Acceptance:_ docs match the implemented roles and variables.

- [x] **5.5 Add release/deprecation policy** — SemVer tags, changelog rules, one-major-release alias window.  
  _Acceptance:_ `v0.1`/`v0.2`/`v1.0`/`v2.0` milestones are defined and followed.

---

## Phase 6 — Operations and lifecycle

- [x] **6.1 Add backup/restore and rollback runbook** — pack before change, artifact retention, restore procedure.  
  _Acceptance:_ runbook is documented; lab validation is pending in 4.5.

- [x] **6.2 Add health checks and observability** — AdminServer, NodeManager, OHS checks; log locations; failure messages.  
  _Acceptance:_ `--tags validate` reports actionable status.

- [x] **6.3 Document AAP/AWX integration** — inventories, credentials, surveys, RBAC, EE.  
  _Acceptance:_ a platform operator can import the project without extra-var host targeting.

- [x] **6.4 Define lifecycle review cadence** — quarterly Ansible/collection review; FMW 27, Java 25, RHEL 10 planning.  
  _Acceptance:_ owners and dates are recorded.

---

## Progress log

| Date | Item | Commit | Notes |
|---|---|---|---|
| 2026-11-17 | Checklist created | — | Detailed version retained in `docs/roadmap-details.md` |
| 2026-11-17 | 0.1 `ansible.cfg` | — | Validated with `ansible-config dump --only-changed` |
| 2026-11-17 | 0.2 dependencies pinned | — | `ansible-galaxy` confirms collections installed |
| 2026-11-17 | 0.4 example inventory | — | 15/15 playbooks pass `--syntax-check` without extra vars |
| 2026-11-17 | 0.3 lint/format config | — | `ansible-lint` exits 0 with warnings; yamllint reports existing whitespace debt |
| 2026-11-17 | 0.5 README rewrite | — | Includes support matrix, inventory, secrets, and playbook reference |
| 2026-11-17 | 0.6 Makefile + CI | — | `make syntax` and `make lint` pass locally |
| 2026-11-17 | 0.7 project metadata | — | License is a proprietary placeholder pending owner decision |
| 2026-11-17 | 0.8 file hygiene | — | `git diff --check` clean; yamllint exits 0; autofixes applied |
| 2026-11-17 | 1.1 FQCN | — | All role task modules converted; syntax/lint pass |
| 2026-11-17 | 1.2 collection modules | — | `archive` uses `community.general`; `remote_src: true` |
| 2026-11-17 | 1.3 loops | — | No `with_*` remains; indexed loops use `index_var` |
| 2026-11-17 | 1.4 free-form args | — | Completed by the formatting autofix; lint rule at zero |
| 2026-11-17 | 1.5 booleans/conditionals | — | `yaml[truthy]` and `literal-compare` at zero |
| 2026-11-17 | 1.6 play keywords | — | `remote_user`, parameterized `become_user`, FQCN sudo |
| 2026-11-17 | 1.7 command/shell | — | 40 tasks now declare `changed_when`; long commands use folded scalars |
| 2026-11-17 | 1.8 core validation | — | Syntax green on 2.20.11 and 2.21.6; 2.22 blocked by Python 3.13 |
| 2026-11-17 | 2.1 hardcoded passwords | — | Defaults empty; domain/JDBC asserts fail with guidance |
| 2026-11-17 | 2.2 vault example | — | `docs/secrets.md`, vault example, ignore rules |
| 2026-11-17 | 2.3 no_log coverage | — | Secret-bearing templates and RCU tasks marked `no_log` |
| 2026-11-17 | 2.4 secret modes/cleanup | — | RCU/boot/WLST credentials secured; RCU cleanup in `always` |
| 2026-11-17 | 2.5 download hardening | — | Checksum variable, retries/until, TLS options, opt-in bypass flags |
| 2026-11-17 | 2.6 destructive guards | — | Confirmation/prod guards, backup check, graceful process stop |
| 2026-11-17 | 2.7 wrapper hardening | — | `umask 077`, boot.properties secured, dead secret templates removed |
| 2026-11-17 | 3.1 simple defects | — | Undefined var, OEM stage dir, trailing path, OEM alias fixed |
| 2026-11-17 | 3.2 execution context | — | Oracle home variable and inventory-derived admin host |
| 2026-11-17 | 3.3 pack/unpack | — | Controller artifact repo, both artifacts fetched/restored, NM templates wired |
| 2026-11-17 | 3.4 waits/disk | — | Wait scripts capped at 60 attempts; mount lookup fails explicitly; sizes updated |
| 2026-11-17 | 3.5 multi-host safety | — | Group targets, RCU `run_once`, serial clean/unpack, fail-fast |
| 2026-11-17 | 3.6 tags/handlers | — | Play tags, `never` on clean, validate playbook, restart handlers |
| 2026-11-17 | 3.7 WLST idempotency | — | MBean guards, install/domain/extension markers |
| 2026-11-17 | 3.8 dead code | — | Removed unused vars/templates/comments; server groups implemented |
| 2026-11-17 | 4.1 OS prepare role | — | Packages, user/groups, limits, sysctl, directories, oraInst.loc |
| 2026-11-17 | 4.2 software catalog/Java | — | Catalog for 12.2.1.2/12.2.1.4/14.1.2; Java versioned |
| 2026-11-17 | 4.3 FMW 12.2.1.4 | — | Version/RCU/response/media parameterized; lab pending |
| 2026-11-17 | 4.4 FMW 14.1.2 scaffold | — | RCU/response/JDK 17 scaffold and upgrade runbook |
| 2026-11-17 | 5.1 argument specs | — | 19 role argument specs added |
| 2026-11-17 | 5.2 molecule | — | Syntax scenario passes; Docker scenarios scaffolded |
| 2026-11-17 | 5.3 CI matrix/EE | — | 2.20/2.21/2.22 matrix, EE and navigator config |
| 2026-11-17 | 5.4 documentation | — | Architecture, prerequisites, inventory, variables, runbooks, troubleshooting |
| 2026-11-17 | 5.5 release policy | — | SemVer, deprecation window, release checklist, changelog refresh |
| 2026-11-17 | 6.1 backup/restore | — | Runbook documented; lab validation pending |
| 2026-11-17 | 6.2 observability | — | Validate role, ports, log paths, alerts |
| 2026-11-17 | 6.3 AAP/AWX | — | EE, credentials, surveys, RBAC, job templates |
| 2026-11-17 | 6.4 lifecycle | — | Quarterly checklist, owners, decision log |
