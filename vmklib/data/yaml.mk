YAML_PREFIX := yaml-

.PHONY: \
	$(YAMLLINT_INSTALL)

YAMLLINT_INSTALL := $(YAML_PREFIX)lint-install
YAMLLINT_ARGS ?=

YAMLLINT_CONC := $(call to_concrete, $(YAMLLINT_INSTALL)-$(VENV_NAME))
$(YAMLLINT_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade yamllint
	$(call generic_concrete,$@)

$(YAMLLINT_INSTALL): $(YAMLLINT_CONC)

$(YAML_PREFIX)lint-%: | $(YAMLLINT_CONC)
	$(call time_wrap,$(PYTHON_BIN)/yamllint \
		$(YAMLLINT_ARGS) $($(PROJ)_DIR)/$*)
