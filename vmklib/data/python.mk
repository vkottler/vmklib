PY_PREFIX := python-

.PHONY: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test $(PY_PREFIX)view \
        $(PY_PREFIX)host-coverage $(PY_PREFIX)all $(PY_PREFIX)clean \
        $(PY_PREFIX)dist $(PY_PREFIX)upload $(PY_PREFIX)editable

PY_LINT_EXTRA_ARGS :=
PY_LINT_ARGS := $($(PROJ)_DIR)/tests $(PY_LINT_EXTRA_ARGS)

# don't turn this into a concrete target so we can spam it
$(PY_PREFIX)lint-%: $(VENV_CONC)
	$(PYTHON_BIN)/$* $($(PROJ)_DIR)/$(PROJ) $(PY_LINT_ARGS)

$(PY_PREFIX)lint: $(PY_PREFIX)lint-flake8 $(PY_PREFIX)lint-pylint

$(PY_PREFIX)sa: $(PY_PREFIX)lint-mypy

PYTEST_EXTRA_ARGS :=
PYTEST_ARGS := -x --log-cli-level=10 --cov=$(PROJ) --cov-report html \
               $(PYTEST_EXTRA_ARGS)
$(PY_PREFIX)test: $(VENV_CONC)
	$(PYTHON_BIN)/pytest $(PYTEST_ARGS) $($(PROJ)_DIR)/tests

$(PY_PREFIX)test-%: $(VENV_CONC)
	$(PYTHON_BIN)/pytest $(PYTEST_ARGS) -k "$*" $($(PROJ)_DIR)/tests

$(PY_PREFIX)dist: $(VENV_CONC)
	@rm -rf $($(PROJ)_DIR)/dist
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/python $($(PROJ)_DIR)/setup.py sdist
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/python $($(PROJ)_DIR)/setup.py bdist_wheel

TWINE_ARGS := --non-interactive --verbose
$(PY_PREFIX)upload: $(VENV_CONC) $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test $(PY_PREFIX)dist
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/twine upload $(TWINE_ARGS) $($(PROJ)_DIR)/dist/*

EDITABLE_CONC := $(call to_concrete, $(PY_PREFIX)editable)
$(EDITABLE_CONC): $(VENV_CONC)
	$(PYTHON_BIN)/pip install -e $($(PROJ)_DIR)
	$(call generic_concrete,$@)

$(PY_PREFIX)editable: $(EDITABLE_CONC)

$(PY_PREFIX)view:
	@$(BROWSER) $($(PROJ)_DIR)htmlcov/index.html

PYTHON_COV_PORT := 8080
$(PY_PREFIX)host-coverage:
	cd $($(PROJ)_DIR)/htmlcov && python$(PYTHON_VERSION) -m http.server $(PYTHON_COV_PORT)

$(PY_PREFIX)all: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test

$(PY_PREFIX)clean:
	@find -iname '*.pyc' -delete
	@find -iname '__pycache__' -delete
	@rm -rf $(BUILD_DIR) $($(PROJ)_DIR)/.mypy_cache
	@rm -rf $($(PROJ)_DIR)/cover $($(PROJ)_DIR)/.coverage \
		$($(PROJ)_DIR)/dist $($(PROJ)_DIR)/*.egg-info \
		$($(PROJ)_DIR)/htmlcov $($(PROJ)_DIR)/.pytest_cache \
		$(EDITABLE_CONC)
