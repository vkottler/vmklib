.PHONY: \
	$(PY_PREFIX)upload \
	$(PY_PREFIX)upload-only

TWINE_CONC := $(call to_concrete, twine-$(VENV_NAME))
$(TWINE_CONC): | $(VENV_CONC)
	$(PIP) install --upgrade twine
	$(call generic_concrete,$@)

TWINE_ARGS := --non-interactive --verbose --skip-existing
$(PY_PREFIX)upload: $(PY_PREFIX)all | $(TWINE_CONC)
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/twine check dist/* && \
		$(PYTHON_BIN)/twine upload $(TWINE_ARGS) dist/*

$(PY_PREFIX)upload-only: $(PY_BUILD_CONC) | $(TWINE_CONC)
	cd $($(PROJ)_DIR) && \
		$(PYTHON_BIN)/twine check dist/* && \
		$(PYTHON_BIN)/twine upload $(TWINE_ARGS) dist/*
	rm $<
