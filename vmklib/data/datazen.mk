DZ_PREFIX  := dz-
DZ_INSTALL := $(DZ_PREFIX)install

.PHONY: $(DZ_PREFIX)sync $(DZ_PREFIX)clean $(DZ_PREFIX)describe \
        $(DZ_PREFIX)upgrade $(DZ_INSTALL)

DZ_DIR      ?= $($(PROJ)_DIR)
DZ_ARGS     := -C $(DZ_DIR)
ifdef DZ_MANIFEST
DZ_ARGS     += -m $(DZ_MANIFEST)
endif
ifdef DZ_VERBOSE
DZ_ARGS     += -v
endif

DZ_CONC := $(call to_concrete, $(DZ_INSTALL)-$(VENV_NAME))
$(DZ_CONC): | $(VENV_CONC)
	$(PYTHON_BIN)/pip install --upgrade datazen
	$(call generic_concrete,$@)

$(DZ_INSTALL): $(DZ_CONC)

$(DZ_PREFIX)sync: | $(DZ_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS)

$(DZ_PREFIX)clean: | $(DZ_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS) -c
	@rm -rf $($(PROJ)_DIR)/datazen-out

$(DZ_PREFIX)describe: | $(DZ_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS) -d

$(DZ_PREFIX)upgrade: | $(VENV_CONC)
	$(PYTHON_BIN)/pip install --upgrade datazen
