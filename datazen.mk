DZ_PREFIX := dz-

.PHONY: $(DZ_PREFIX)sync $(DZ_PREFIX)clean $(DZ_PREFIX)describe

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

$(DZ_PREFIX)clean:
	$(PYTHON_BIN)/dz $(DZ_ARGS) -c

$(DZ_PREFIX)describe:
	$(PYTHON_BIN)/dz $(DZ_ARGS) -d
