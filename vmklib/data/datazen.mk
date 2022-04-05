DZ_PREFIX  := dz-
DZ_INSTALL := $(DZ_PREFIX)install

.PHONY: $(DZ_PREFIX)sync $(DZ_PREFIX)clean $(DZ_PREFIX)describe \
        $(DZ_PREFIX)upgrade $(DZ_INSTALL) dz

DZ_DIR      ?= $($(PROJ)_DIR)
DZ_ARGS     := -C $(DZ_DIR)
ifdef DZ_MANIFEST
DZ_ARGS     += -m $(DZ_MANIFEST)
endif
ifdef DZ_VERBOSE
DZ_ARGS     += -v
endif

DZ_DIR   := $($(PROJ)_DIR)/datazen-out
DZ_ENTRY := $(PYTHON) -m datazen

DZ_CONC := $(call to_concrete, $(DZ_INSTALL)-$(VENV_NAME))
$(DZ_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade datazen
	$(call generic_concrete,$@)

$(DZ_INSTALL): $(DZ_CONC)

$(DZ_PREFIX)sync: | $(DZ_CONC)
	$(DZ_ENTRY) $(DZ_ARGS)

dz: $(DZ_PREFIX)sync

$(DZ_PREFIX)clean: | $(DZ_CONC)
	$(DZ_ENTRY) $(DZ_ARGS) -c
	@rm -rf $(DZ_DIR)

$(DZ_PREFIX)describe: | $(DZ_CONC)
	$(DZ_ENTRY) $(DZ_ARGS) -d

$(DZ_PREFIX)upgrade: | $(VENV_CONC)
	$(PIP) install --upgrade datazen
