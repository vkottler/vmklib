.PHONY: \
	$(PY_PREFIX)clean-build \
	$(PY_PREFIX)dist \
	$(PY_PREFIX)build \
	$(PY_PREFIX)build-once \
	$(PY_PREFIX)stubs \
	$(PY_PREFIX)dist-with-stubs \
	$(PY_PREFIX)editable

PY_CLEAN_BUILD_CMD := rm -rf $($(PROJ)_DIR)/dist $(BUILD_DIR)/bdist* \
                      $(BUILD_DIR)/lib

$(PY_PREFIX)clean-build:
	$(PY_CLEAN_BUILD_CMD)

$(PY_PREFIX)dist: $(PY_PREFIX)clean-build | $(VENV_CONC)
	cd $($(PROJ)_DIR) && \
		$(PYTHON) $($(PROJ)_DIR)/setup.py sdist
	cd $($(PROJ)_DIR) && \
		$(PYTHON) $($(PROJ)_DIR)/setup.py bdist_wheel

PY_BUILD_INSTALL_CONC := $(call to_concrete, build-$(VENV_NAME))
$(PY_BUILD_INSTALL_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade build
	$(call generic_concrete,$@)

PY_BUILD_CMD := $(call time_wrap_cd,$(PYTHON) -m build,$($(PROJ)_DIR))

$(PY_PREFIX)build: $(PY_PREFIX)clean-build | $(PY_BUILD_INSTALL_CONC)
	$(PY_BUILD_CMD)

PY_BUILD_CONC := $(call to_concrete, build-$(PROJ)-$(VENV_NAME))
$(PY_BUILD_CONC): | $(PY_BUILD_INSTALL_CONC)
	$(PY_CLEAN_BUILD_CMD)
	$(PY_BUILD_CMD)
	$(call generic_concrete,$@)

$(PY_PREFIX)build-once: $(PY_BUILD_CONC)

# Allow overriding the target used to build the package distributions.
PY_BUILDER ?= $(PY_PREFIX)build

$(PY_PREFIX)stubs: | $(VENV_CONC)
	$(PYTHON_BIN)/stubgen -p $(PROJ) -o $($(PROJ)_DIR)

# Prefer 'dist' because stubgen does not work very well (the resulting stubs
# are missing a lot of actual type information that mypy and other tools should
# infer by looking at source).
$(PY_PREFIX)dist-with-stubs: $(PY_PREFIX)clean-build $(PY_PREFIX)stubs | $(VENV_CONC)
	cd $($(PROJ)_DIR) && \
		$(PYTHON) $($(PROJ)_DIR)/setup.py sdist
	cd $($(PROJ)_DIR) && \
		$(PYTHON) $($(PROJ)_DIR)/setup.py bdist_wheel
	@cd $($(PROJ)_DIR)/$(PROJ) && find -iname '*.pyi' -delete

EDITABLE_CONC := $(call to_concrete, $(PY_PREFIX)editable)
$(EDITABLE_CONC): | $(VENV_CONC)
	$(PIP) install -e $($(PROJ)_DIR)
	$(call generic_concrete,$@)

$(PY_PREFIX)editable: $(EDITABLE_CONC)
