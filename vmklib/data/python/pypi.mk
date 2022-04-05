PYPI_PREFIX := pypi-

.PHONY: \
	$(PYPI_PREFIX)check-env \
	$(PYPI_PREFIX)check-env-ci \
	$(PYPI_PREFIX)upload \
	$(PYPI_PREFIX)upload-only \
	$(PYPI_PREFIX)upload-only-ci

UPLOAD_ENV          := $($(PROJ)_DIR)/.pypi.env
SECRETHUB_PYPI_PATH ?= $(USER)/pypi/api-keys/personal-upload
$(UPLOAD_ENV):
	@rm -f $@
	@echo "export TWINE_USERNAME=__token__" >> $@
	@echo "export TWINE_PASSWORD=`secrethub read $(SECRETHUB_PYPI_PATH)`" >> $@
	+@echo "wrote '$@'"

$(PYPI_PREFIX)check-env: | $(UPLOAD_ENV)
ifndef TWINE_USERNAME
	$(error TWINE_USERNAME not set, run 'source $(UPLOAD_ENV)')
endif
ifndef TWINE_PASSWORD
	$(error TWINE_PASSWORD not set, run 'source $(UPLOAD_ENV)')
endif

$(PYPI_PREFIX)upload: $(PYPI_PREFIX)check-env $(PY_PREFIX)upload
$(PYPI_PREFIX)upload-only: $(PYPI_PREFIX)check-env $(PY_PREFIX)upload-only

$(PYPI_PREFIX)check-env-ci:
ifndef TWINE_USERNAME
	$(error TWINE_USERNAME not set, can't upload '$(PROJ)'.)
endif
ifndef TWINE_PASSWORD
	$(error TWINE_PASSWORD not set, can't upload '$(PROJ)'.)
endif

$(PYPI_PREFIX)upload-ci: $(PYPI_PREFIX)check-env-ci $(PY_PREFIX)upload-only
