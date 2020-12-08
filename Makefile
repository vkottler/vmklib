# put names of targets here that aren't real file outputs (not essential, but
# idiomatically correct)
.PHONY: all clean

# set this to control what target is resolved by only invoking 'make'
.DEFAULT_GOAL  := all

# set this to the name of your project, so it can be substituted in wherever
# necessary
PROJ           := sample

# root directory of your project, can use "." or $(shell pwd) but the below
# assignment will guarantee that it's assigned to the directory that this
# file is in (the Makefile targeted by make)
$(PROJ)_DIR    := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

# include target-containing files, if you sub-module this repository the paths
# may need to change, include 'functions.mk' first so other includes can use
# common functions
include $($(PROJ)_DIR)/mk/srcs/conf.mk

all: venv

clean: python-clean
