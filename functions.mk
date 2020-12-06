#
# This function can convert a phony target name into a concrete file in
# BUILD_DIR to use `@date > $@` to build phony recipes that are still tracked
# by a concrete output.
#
# 1: phony target name
#
to_concrete = $(patsubst %,$(BUILD_DIR)/%.txt,$(1))

#
# Get the last element in a space-delimited list.
# https://ftp.gnu.org/old-gnu/Manuals/make/html_node/make_17.html
#
# 1: a space-delimited list of tokens
#
get_last_word = $(word $(words $(1)), $(1))

#
# Strip the name filename from a makefile path.
# https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
#
# 1: makefile path
# 2: makefile name
#
makefile_to_dir = $(patsubst %/$(2),%,$(1))

#
# Allows any makefile to include other makefiles with relative paths only.
#
MK_CFG_NAME ?= conf.mk
get_current_makefile_dir = $(call makefile_to_dir,$(call get_last_word,$(MAKEFILE_LIST)),$(MK_CFG_NAME))

#
# Aggregate files with a specific extension from a given directory into
# a variable.
#
# 1: directory
# 2: file extension
#
get_files = $(wildcard $(1)/*.$(2))

#
# A single source of truth for how to build a generic, concrete target.
#
# 1: name of the concrete target-file
#
define generic_concrete
	@mkdir -p $(dir $1)
	@date > $1
endef
