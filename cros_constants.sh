#!/bin/bash

# --------------------------------------------------------------------------------

# constants for bash scripts


# --------------------------------------------------------------------------------

INFO="\e[1;32mINFO\t: "
ERROR="\e[1;31m"
ENDFORMAT="\e[0m"

AUTOTEST_PATH="/usr/local/autotest"
ATITOOL_PATH="/usr/local/atitool"
AGT_PATH="/usr/local/agt"
AGT_INTERNAL_PATH="/usr/local/agt_internal"

LOGS=(
    "cros_data_logger.log"
    "cros_data_parser.log"
    "cros_file_handler.log"
    "cros_scenario_launcher.log"
    "cros_software_controller.log"
)