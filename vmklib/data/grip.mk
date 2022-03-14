GRIP_PREFIX := grip-

.PHONY: $(GRIP_PREFIX)check-env $(GRIP_PREFIX)render

GRIP_ENV            := $($(PROJ)_DIR)/.grip.env
SECRETHUB_GRIP_PATH ?= $(USER)/github/tokens/basic-api-token
$(GRIP_ENV):
	@rm -f $@
	@echo "export GRIP_TOKEN=`secrethub read $(SECRETHUB_GRIP_PATH)`" >> $@
	+@echo "wrote '$@'"

GRIP_CONC := $(call to_concrete, grip-$(VENV_NAME))
$(GRIP_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade grip
	$(call generic_concrete,$@)

$(GRIP_PREFIX)check-env: | $(GRIP_ENV)
ifndef GRIP_TOKEN
	$(error GRIP_TOKEN not set, run 'source $(GRIP_ENV)')
endif

GRIP_PORT := 0.0.0.0:8000
GRIP_FILE := README.md
$(GRIP_PREFIX)render: $(GRIP_PREFIX)check-env | $(GRIP_CONC)
	@$(PYTHON_BIN)/grip \
		--pass $(GRIP_TOKEN) \
		--title=$(PROJ) \
		$($(PROJ)_DIR)/$(GRIP_FILE) \
		$(GRIP_PORT)
