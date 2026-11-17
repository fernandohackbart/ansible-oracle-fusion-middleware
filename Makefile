SHELL := /bin/bash
PLAYBOOKS := $(wildcard OFM-*.yml)

.PHONY: help setup syntax lint yamllint molecule test test-all clean

help:
	@echo "Targets:"
	@echo "  setup     Create .venv and install pinned dependencies"
	@echo "  syntax    Run ansible-playbook --syntax-check on every playbook"
	@echo "  lint      Run ansible-lint with the committed configuration"
	@echo "  yamllint  Run yamllint"
	@echo "  molecule  Run the molecule syntax scenario"
	@echo "  test      syntax + lint"
	@echo "  test-all  syntax + lint + yamllint + molecule"
	@echo "  clean     Remove local caches and retry files"

setup:
	python3.12 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements-dev.txt
	. .venv/bin/activate && ansible-galaxy collection install -r requirements.yml

syntax:
	@set -e; for playbook in $(PLAYBOOKS); do \
		echo "== $$playbook"; \
		ansible-playbook --syntax-check "$$playbook"; \
	done

lint:
	ansible-lint --offline --nocolor .

yamllint:
	yamllint .

molecule:
	molecule test -s syntax

test: syntax lint

test-all: syntax lint yamllint molecule

clean:
	rm -rf .cache artifacts .venv
	rm -f ./*.retry
