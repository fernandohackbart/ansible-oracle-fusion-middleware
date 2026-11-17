# Contributing

## Workflow

1. Pick an unchecked item from [ROADMAP.md](ROADMAP.md).
2. Create a short-lived branch: `feature/<item-id>-<slug>`.
3. Make the smallest coherent change.
4. Run `make test` (and `make yamllint` once whitespace cleanup is complete).
5. Update the checkbox and progress log in `ROADMAP.md`.
6. Commit with a focused message, for example `fix: correct oem stage directory`.
7. Open a pull request describing the acceptance criteria that were met.

## Validation

```bash
make syntax
make lint
make yamllint
```

`ansible-lint` must not regress. The current configuration starts at profile
`basic`; remove temporary `warn_list` entries as the corresponding roadmap items
are completed.

## Conventions

- Use FQCN module names (`ansible.builtin.*`, `community.general.*`).
- Prefer `loop` over `with_*`.
- Every `command`/`shell` task needs `creates`, `changed_when`, or a documented
  reason why it is intentionally always changed.
- Never commit plaintext secrets. Use Ansible Vault or an external secret manager.
- Set explicit file modes for files containing credentials or configuration.
- Hidden failures (`ignore_errors`) require a comment and a follow-up roadmap item.
- Keep role names and variables snake_case for new code. Legacy aliases are
  documented in the roadmap and will be removed in a major release.

## Commit messages

Use a short imperative subject and an optional body explaining the why:

```text
fix: bound the admin server wait loop

Add a maximum attempt count so a failed startup does not hang the playbook.
```
