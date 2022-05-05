#
# Set up platform-specific variables.
#
ifeq ($(OS),Windows_NT)

SEP  := \\
NULL := NUL
path = $(subst /,$(SEP),$(1))

else

SEP  := /
NULL := /dev/null
path = $(1)
MKDIR = $(shell mkdir $(call path, $(1)))

endif

BUILD_DIR_NAME ?= build
BUILD_DIR      ?= $(call path,$($(PROJ)_DIR)/$(BUILD_DIR_NAME))
$(BUILD_DIR):
	@mkdir -p $@
	@touch $@

#
# Get the last element in a space-delimited list.
# https://ftp.gnu.org/old-gnu/Manuals/make/html_node/make_17.html
#
# 1: a space-delimited list of tokens
#
get_last_word = $(word $(words $(1)), $(1))

#
# Get the full path to the currently loaded makefile. 
#
get_current_makefile = $(call get_last_word,$(MAKEFILE_LIST))

#
# Strip the name filename from a makefile path.
# https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
#
# 1: makefile path
# 2: makefile name
#
makefile_to_dir = $(patsubst %$(SEP)$(2),%,$(1))

#
# Allows any makefile to include other makefiles with relative paths only.
#
MK_CFG_NAME ?= conf.mk
get_current_makefile_dir = $(call makefile_to_dir,$(call get_current_makefile),$(MK_CFG_NAME))

# Package directories.
MK_SRC_DIR  := $(call get_current_makefile_dir)
MK_PY_DIR   := $(call path,$(MK_SRC_DIR)/..)
MK_DATA_DIR := $(call path,$(MK_SRC_DIR)/data)

# Set a root directory for the current git repository if we're in one,
# otherwise use the project directory.
GIT_ROOT    := $(shell git rev-parse --show-toplevel 2>$(NULL))
ifeq ($(GIT_ROOT),)
GIT_ROOT    := $($(PROJ)_DIR)
endif

include $(call path,$(MK_SRC_DIR)/functions.mk)
include $(call path,$(MK_SRC_DIR)/time.mk)
include $(call path,$(MK_SRC_DIR)/venv.mk)

include $(call path,$(MK_SRC_DIR)/python.mk)
include $(call path,$(MK_SRC_DIR)/python/build.mk)
include $(call path,$(MK_SRC_DIR)/python/upload.mk)
include $(call path,$(MK_SRC_DIR)/python/pypi.mk)
include $(call path,$(MK_SRC_DIR)/python/docs.mk)

include $(call path,$(MK_SRC_DIR)/vmklib.mk)
include $(call path,$(MK_SRC_DIR)/datazen.mk)
include $(call path,$(MK_SRC_DIR)/grip.mk)
include $(call path,$(MK_SRC_DIR)/yaml.mk)
