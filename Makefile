###############################################################################
MK_INFO := https://pypi.org/project/vmklib
ifeq (,$(shell which mk))
$(warning "No 'mk' in $(PATH), install 'vmklib' with 'pip' ($(MK_INFO))")
endif
ifndef MK_AUTO
$(error target this Makefile with 'mk', not '$(MAKE)' ($(MK_INFO)))
endif
###############################################################################

# put names of targets here that aren't real file outputs (not essential, but
# idiomatically correct)
.PHONY: all clean edit lint yaml

# set this to control what target is resolved by only invoking 'make'
.DEFAULT_GOAL := all

all: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test lint

edit: $(PY_PREFIX)edit

clean: $(PY_PREFIX)clean venv-clean
	@rm -rf $(BUILD_DIR) $($(PROJ)_DIR)/tags

lint: $(YAML_PREFIX)lint-local $(YAML_PREFIX)lint-manifest.yaml

yaml: lint
