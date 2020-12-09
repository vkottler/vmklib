DZ_PREFIX := dz-

.PHONY: $(DZ_PREFIX)sync $(DZ_PREFIX)clean $(DZ_PREFIX)describe \
        $(DZ_PREFIX)-upgrade

DZ_DIR      ?= $($(PROJ)_DIR)
DZ_ARGS     := -C $(DZ_DIR)
ifdef DZ_MANIFEST
DZ_ARGS     += -m $(DZ_MANIFEST)
endif
ifdef DZ_VERBOSE
DZ_ARGS     += -v
endif

$(DZ_PREFIX)sync: $(VENV_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS)

$(DZ_PREFIX)clean: $(VENV_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS) -c
	@rm -rf $($(PROJ)_DIR)/datazen-out

$(DZ_PREFIX)describe: $(VENV_CONC)
	$(PYTHON_BIN)/dz $(DZ_ARGS) -d

$(DZ_PREFIX)upgrade: $(VENV_CONC)
	$(PYTHON_BIN)/pip install --upgrade datazen
