#
# A single source of truth for how to build a generic, concrete target.
#
# 1: name of the concrete target-file
#
define generic_concrete
	@mkdir -p $(dir $1)
	@date > $1
endef

#
# A simple target for linking adjacent projects into a project's root
# directory.
#
# 1: name of the adjacent directory
#
define generic_link_adjacent
        test -d $($(PROJ)_DIR)/../$1
        ln -s $($(PROJ)_DIR)/../$1 $@
endef

#
# This function can convert a phony target name into a concrete file in
# BUILD_DIR to use `@date > $@` to build phony recipes that are still tracked
# by a concrete output.
#
# 1: phony target name
#
to_concrete = $(patsubst %,$(BUILD_DIR)/%.txt,$(1))

#
# Aggregate files with a specific extension from a given directory into
# a variable.
#
# 1: directory
# 2: file extension
#
get_files = $(wildcard $(1)/*.$(2))
