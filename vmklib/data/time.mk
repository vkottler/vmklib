TIME := /usr/bin/time

ifeq (,$(shell which $(TIME)))
	TIME_CMD :=
else

# Allow disabling time output.
ifdef NO_TIME
	TIME_CMD :=
else

# Set a sane default for the output presentation.
ifndef TIME_FMT
	TIME_CMD := $(TIME) -p
else
	TIME_CMD := $(TIME) -f "$(TIME_FMT)"
endif

endif

endif

# Wraps a command with the 'time' invocation, while printing the original
# command (but only once).
define time_wrap
+@echo "$1" && $(TIME_CMD) $1
endef

# Wraps a command with the 'time' invocation, while printing the original
# command and allows changing directories ahead of command invocation.
define time_wrap_cd
+@echo "cd $2 && $1" && cd $2 && $(TIME_CMD) $1
endef

# Wraps a command with the 'time' invocation, but doesn't print the command.
define time_wrap_silent
@$(TIME_CMD) $1
endef
