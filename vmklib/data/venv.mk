.PHONY: venv venv-clean

# set the Python version if it hasn't been set yet
PYTHON_VERSION   ?= 3.8
REQUIREMENTS_DIR ?= $($(PROJ)_DIR)/$(PROJ)
REQ_FILES        ?= requirements dev_requirements

VENV_NAME        := venv$(PYTHON_VERSION)
VENV_DIR         := $($(PROJ)_DIR)/$(VENV_NAME)
PYTHON_BIN       := $(VENV_DIR)/bin
VENV_ACTIVATE    := $(PYTHON_BIN)/activate

PYTHON           := $(PYTHON_BIN)/python
PIP              := $(PYTHON) -m pip

VENV_CONC        := $(call to_concrete, $(VENV_NAME))
REQ_CONC         := $(REQ_FILES:%=$(call to_concrete,$(VENV_NAME)/req-%))

# target for building a real Python virtual environment directory
$(VENV_DIR): $(MK_DATA_DIR)/fresh_venv.txt
	python$(PYTHON_VERSION) -m venv $@
	@touch $@
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r $<

# add empty files for missing requirements files and let the caller know
# an attempt to install from a missing one was made
$(REQUIREMENTS_DIR)/%.txt:
	@mkdir -p $(dir $@)
	@touch $@
	+@echo "creating empty '$@', request made to install it"

# target for installing requirements files into the virtual environment
$(call to_concrete, $(VENV_NAME)/req-%): $(REQUIREMENTS_DIR)/%.txt | $(BUILD_DIR) $(VENV_DIR)
	$(call time_wrap,$(PIP) install --upgrade -r $<)
	$(call generic_concrete,$@)

$(call to_concrete, $(VENV_NAME)/edit_venv): $(MK_DATA_DIR)/edit_venv.txt | $(BUILD_DIR) $(VENV_DIR)
	$(call time_wrap,$(PIP) install --upgrade -r $<)
	$(call generic_concrete,$@)

$(VENV_CONC): $(REQ_CONC)
	$(call generic_concrete,$@)

venv: $(VENV_CONC)

venv-clean:
	@rm -rf $($(PROJ)_DIR)/venv* $(BUILD_DIR)/venv* $(VENV_CONC) $(REQ_CONC)
