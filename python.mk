.PHONY: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test $(PY_PREFIX)view \
        $(PY_PREFIX)host-coverage $(PY_PREFIX)all $(PY_PREFIX)clean

PY_PREFIX := python-

# don't turn this into a concrete target so we can spam it
PY_EXTRA_LINT_ARGS ?=
$(PY_PREFIX)lint-%: $(VENV_CONC)
	$(PYTHON_BIN)/$* $($(PROJ)_DIR)/$(PROJ) $($(PROJ)_DIR)/tests \
		$(PY_EXTRA_LINT_ARGS)

$(PY_PREFIX)lint: $(PY_PREFIX)lint-flake8 $(PY_PREFIX)lint-pylint

$(PY_PREFIX)sa: $(PY_PREFIX)lint-mypy

PYTEST_ARGS := -x --log-cli-level=10 --cov=$(PROJ) --cov-report html
$(PY_PREFIX)test: $(VENV_CONC)
	$(PYTHON_BIN)/pytest $(PYTEST_ARGS)

$(PY_PREFIX)view:
	@$(BROWSER) $($(PROJ)_DIR)htmlcov/index.html

$(PY_PREFIX)host-coverage:
	cd $($(PROJ)_DIR)/htmlcov && python$(PYTHON_VERSION) -m http.server 8080

$(PY_PREFIX)all: $(PY_PREFIX)lint $(PY_PREFIX)sa $(PY_PREFIX)test

$(PY_PREFIX)clean:
	@find -iname '*.pyc' -delete
	@find -iname '__pycache__' -delete
	@rm -rf $(BUILD_DIR) $($(PROJ)_DIR)/.mypy_cache
	@rm -rf $($(PROJ)_DIR)/cover $($(PROJ)_DIR)/.coverage dist \
		$($(PROJ)_DIR)/*.egg-info $($(PROJ)_DIR)/htmlcov \
		$($(PROJ)_DIR)/.pytest_cache
