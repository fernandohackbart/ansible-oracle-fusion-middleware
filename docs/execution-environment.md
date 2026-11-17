# Execution Environment

The project can be packaged as an Ansible Execution Environment (EE) so the
controller runs a pinned Python, ansible-core, and collection set.

## Build

```bash
pip install ansible-builder
ansible-builder build -f execution-environment.yml -t ofm-ee:latest
```

## Run

```bash
ansible-navigator run OFM-validate.yml -i inventories/example/hosts.yml --mode stdout
```

## Notes

- The EE contains **no** Oracle media, JDK archives, or licensed software.
- Mount the artifact repository or provide a media URL at runtime.
- The EE pins ansible-core 2.21.6. Rebuild it when the project moves to a new
  ansible-core major version.
- For AAP/AWX, push the built image to the organization registry and configure
  the credentials and inventories in the controller.
