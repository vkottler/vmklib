MK_SRC_DIR := $(call get_current_makefile_dir)
include $(MK_SRC_DIR)/functions.mk
include $(MK_SRC_DIR)/venv.mk
include $(MK_SRC_DIR)/python.mk
include $(MK_SRC_DIR)/pypi.mk
include $(MK_SRC_DIR)/datazen.mk
include $(MK_SRC_DIR)/grip.mk
