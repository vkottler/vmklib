MK_PREFIX := mk-

.PHONY: $(MK_PREFIX)upgrade $(MK_PREFIX)sys-upgrade

UPGRADE_CMD := install --upgrade vmklib

$(MK_PREFIX)upgrade: $(VENV_CONC)
	$(PYTHON_BIN)/pip $(UPGRADE_CMD)

$(MK_PREFIX)sys-upgrade:
ifdef MK_SUDO
	sudo -H pip$(PYTHON_VERSION) $(UPGRADE_CMD)
else
	pip$(PYTHON_VERSION) $(UPGRADE_CMD)
endif
