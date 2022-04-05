.PHONY: \
	$(PY_PREFIX)docs \
	$(PY_PREFIX)deps

PY_DOCS_HOST ?= 0.0.0.0
PY_DOCS_PORT ?= 0
PY_DOCS_EXTRA_ARGS ?=

$(PY_PREFIX)docs: | $(VENV_CONC)
	cd $($(PROJ)_DIR) && $(PYTHON) -m pydoc \
		$(PY_DOCS_EXTRA_ARGS) \
		-n $(PY_DOCS_HOST) \
		-p $(PY_DOCS_PORT)

$(PY_PREFIX)docs-%: | $(VENV_CONC)
	$(PYTHON) -m pydoc \
		$(PY_DOCS_EXTRA_ARGS) $*

PYDEPS_CONC := $(call to_concrete, pydeps-$(VENV_NAME))
$(PYDEPS_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade pydeps
	$(call generic_concrete,$@)

PY_DEPS_EXTRA_ARGS ?=
PY_DEPS_ARGS := --no-show $(PY_DEPS_EXTRA_ARGS)

$(PY_PREFIX)deps: | $(PYDEPS_CONC)
	cd $($(PROJ)_DIR) \
		&& mkdir -p im \
		&& $(PYTHON) -m pydeps \
			-T svg -o im/pydeps.svg $(PY_DEPS_ARGS) $(PROJ)
