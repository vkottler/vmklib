MK_PREFIX := mk-
MK_INSTALL := $(MK_PREFIX)install

.PHONY: $(MK_PREFIX)upgrade $(MK_PREFIX)sys-upgrade $(MK_PREFIX)header \
        $(MK_PREFIX)todo $(MK_INSTALL)

UPGRADE_CMD := install --upgrade vmklib

MK_CONC := $(call to_concrete, $(MK_INSTALL)-$(VENV_NAME))
$(MK_CONC): | $(VENV_CONC)
	$(PIP) $(UPGRADE_CMD)
	$(call generic_concrete,$@)

$(MK_INSTALL): $(DZ_CONC)

$(MK_PREFIX)upgrade: | $(VENV_CONC)
	$(PIP) $(UPGRADE_CMD)

$(MK_PREFIX)sys-upgrade:
ifdef MK_SUDO
	sudo -H python$(PYTHON_VERSION) -m pip $(UPGRADE_CMD)
else
	python$(PYTHON_VERSION) -m pip $(UPGRADE_CMD)
endif

$(MK_PREFIX)header:
	+@cat $(MK_DATA_DIR)/header.mk | tail -n 9
	@test -f Makefile || \
		cat $(MK_DATA_DIR)/header.mk | tail -n 9 > Makefile

$(MK_PREFIX)todo:
	-cd $($(PROJ)_DIR) && ack -i todo $(PROJ) tests
