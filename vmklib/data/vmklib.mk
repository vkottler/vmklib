MK_PREFIX := mk-

.PHONY: $(MK_PREFIX)upgrade $(MK_PREFIX)sys-upgrade $(MK_PREFIX)header \
        $(MK_PREFIX)todo

UPGRADE_CMD := install --upgrade vmklib --force-reinstall

$(MK_PREFIX)upgrade: $(VENV_CONC)
	$(PYTHON_BIN)/pip $(UPGRADE_CMD)

$(MK_PREFIX)sys-upgrade:
ifdef MK_SUDO
	sudo -H pip$(PYTHON_VERSION) $(UPGRADE_CMD)
else
	pip$(PYTHON_VERSION) $(UPGRADE_CMD)
endif

$(MK_PREFIX)header:
	+@cat $(MK_DATA_DIR)/header.mk

$(MK_PREFIX)todo:
	-cd $($(PROJ)_DIR) && ack -i todo $(PROJ) tests
