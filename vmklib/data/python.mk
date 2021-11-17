PY_PREFIX := python-

.PHONY: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test $(PY_PREFIX)view \
        $(PY_PREFIX)host-coverage $(PY_PREFIX)all $(PY_PREFIX)clean \
        $(PY_PREFIX)dist $(PY_PREFIX)upload $(PY_PREFIX)editable \
        $(PY_PREFIX)stubs $(PY_PREFIX)format $(PY_PREFIX)format-check \
        $(PY_PREFIX)sa-types $(PY_PREFIX)edit

PY_WIDTH := 79
PY_LINE_LENGTH_ARG := --line-length $(PY_WIDTH)
PY_SOURCES_ARG := $($(PROJ)_DIR)/$(PROJ) \
                  $($(PROJ)_DIR)/tests

PY_LINT_EXTRA_ARGS :=
PY_LINT_ARGS := $(PY_SOURCES_ARG) $($(PROJ)_DIR)/setup.py $(PY_LINT_EXTRA_ARGS)

# don't turn this into a concrete target so we can spam it
$(PY_PREFIX)lint-%: | $(VENV_CONC)
	$(PYTHON_BIN)/$* $(PY_LINT_ARGS)

$(PY_PREFIX)lint: $(PY_PREFIX)lint-flake8 \
                  $(PY_PREFIX)lint-pylint \
                  $(PY_PREFIX)format-check

$(PY_PREFIX)sa: $(PY_PREFIX)lint-mypy

$(PY_PREFIX)sa-types:
	-$(PYTHON_BIN)/mypy $($(PROJ)_DIR)/$(PROJ) $(PY_LINT_ARGS)
	$(PYTHON_BIN)/mypy --install-types --non-interactive

PY_BLACK_ARGS := $(PY_LINE_LENGTH_ARG) $(PY_SOURCES_ARG) \
                 $($(PROJ)_DIR)/setup.py
PY_ISORT_ARGS := $(PY_LINE_LENGTH_ARG) $(PY_SOURCES_ARG) \
                 --profile black --fss -m 3

$(PY_PREFIX)format: | $(VENV_CONC)
	$(PYTHON_BIN)/isort $(PY_ISORT_ARGS)
	$(PYTHON_BIN)/black $(PY_BLACK_ARGS)

$(PY_PREFIX)tags:
	ctags -f $($(PROJ)_DIR)/tags -R \
		$($(PROJ)_DIR)/$(PROJ) $($(PROJ)_DIR)/tests

$(PY_PREFIX)edit: $(PY_PREFIX)tags | $(VENV_CONC)
	. $(VENV_ACTIVATE) && cd $($(PROJ)_DIR) && $(EDITOR)

$(PY_PREFIX)format-check: | $(VENV_CONC)
	$(PYTHON_BIN)/isort --check-only $(PY_ISORT_ARGS)
	$(PYTHON_BIN)/black --check $(PY_BLACK_ARGS)

$(PY_PREFIX)stubs: | $(VENV_CONC)
	$(PYTHON_BIN)/stubgen -p $(PROJ) -o $($(PROJ)_DIR)

PYTEST_EXTRA_ARGS :=
PYTEST_ARGS := -x --log-cli-level=10 --cov=$(PROJ) --cov-report html \
               $(PYTEST_EXTRA_ARGS)
$(PY_PREFIX)test: | $(VENV_CONC)
	$(PYTHON_BIN)/pytest $(PYTEST_ARGS) $($(PROJ)_DIR)/tests

$(PY_PREFIX)test-%: | $(VENV_CONC)
	$(PYTHON_BIN)/pytest $(PYTEST_ARGS) -k "$*" $($(PROJ)_DIR)/tests

$(PY_PREFIX)dist: $(PY_PREFIX)stubs | $(VENV_CONC)
	@rm -rf $($(PROJ)_DIR)/dist $(BUILD_DIR)/bdist* $(BUILD_DIR)/lib
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/python $($(PROJ)_DIR)/setup.py sdist
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/python $($(PROJ)_DIR)/setup.py bdist_wheel
	@cd $($(PROJ)_DIR)/$(PROJ) && find -iname '*.pyi' -delete

TWINE_ARGS := --non-interactive --verbose
$(PY_PREFIX)upload: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test $(PY_PREFIX)dist
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/twine upload $(TWINE_ARGS) $($(PROJ)_DIR)/dist/*

EDITABLE_CONC := $(call to_concrete, $(PY_PREFIX)editable)
$(EDITABLE_CONC): | $(VENV_CONC)
	$(PYTHON_BIN)/pip install -e $($(PROJ)_DIR)
	$(call generic_concrete,$@)

$(PY_PREFIX)editable: $(EDITABLE_CONC)

$(PY_PREFIX)view:
	@$(BROWSER) $($(PROJ)_DIR)htmlcov/index.html

PYTHON_COV_PORT := 0
$(PY_PREFIX)host-coverage:
	cd $($(PROJ)_DIR)/htmlcov \
		&& python$(PYTHON_VERSION) -m http.server $(PYTHON_COV_PORT)

$(PY_PREFIX)all: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test

$(PY_PREFIX)clean:
	@find -iname '*.pyc' -delete
	@find -iname '__pycache__' -delete
	@rm -rf $($(PROJ)_DIR)/$(PROJ)-stubs
	@rm -rf $(BUILD_DIR)/bdist* $(BUILD_DIR)/lib $($(PROJ)_DIR)/.mypy_cache
	@rm -rf $($(PROJ)_DIR)/cover $($(PROJ)_DIR)/.coverage \
		$($(PROJ)_DIR)/dist $($(PROJ)_DIR)/*.egg-info \
		$($(PROJ)_DIR)/htmlcov $($(PROJ)_DIR)/.pytest_cache \
		$(EDITABLE_CONC)
