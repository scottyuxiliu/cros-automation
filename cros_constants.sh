#!/bin/bash

# --------------------------------------------------------------------------------

# constants for bash scripts


# --------------------------------------------------------------------------------

INFO="\e[1;32mINFO\t: "
WARNING="\e[1;33mWARNING\t: "
ERROR="\e[1;31mERROR\t: "
ENDFORMAT="\e[0m"

AUTOTEST_PATH="/usr/local/autotest"
ATITOOL_PATH="/usr/local/atitool"
AGT_PATH="/usr/local/agt"
AGT_INTERNAL_PATH="/usr/local/agt_internal"

# We can create indexed arrays with a more concise syntax, by simply assign them some values:
LOGS=(
    "cros_data_logger.log"
    "cros_data_parser.log"
    "cros_file_handler.log"
    "cros_scenario_launcher.log"
    "cros_software_controller.log"
)

DELAY_AFTER_BOOT=180
DELAY_AFTER_PROG=900

# Associative arrays can be created in the same way: the only thing we need to change is the option used: instead of lowercase -a we must use the -A option of the declare command:
declare -A AUTOTEST_DURATION
AUTOTEST_DURATION["graphics_webglaquarium"]=120
AUTOTEST_DURATION["power_idle"]=660
AUTOTEST_DURATION["power_speedometer2"]=300
AUTOTEST_DURATION["power_thermalload_3min_3000_fish"]=300
AUTOTEST_DURATION["power_thermalload_3min_5000_fish"]=300
AUTOTEST_DURATION["power_thermalload_3min_20000_fish"]=300
AUTOTEST_DURATION["power_thermalload_30min_1000_fish"]=2100
AUTOTEST_DURATION["power_thermalload_30min_5000_fish"]=2100
AUTOTEST_DURATION["power_thermalload_30min_20000_fish"]=2100


declare -A AUTOTEST_RESULT_DIR
AUTOTEST_RESULT_DIR["graphics_webglaquarium"]="/usr/local/autotest/results/default/graphics_WebGLAquarium/results"
AUTOTEST_RESULT_DIR["power_idle"]="/usr/local/autotest/results/default/power_Idle/results"
AUTOTEST_RESULT_DIR["power_speedometer2"]="/usr/local/autotest/results/default/power_Speedometer2/results"
AUTOTEST_RESULT_DIR["power_thermalload_3min_3000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_thermalload_3min_5000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_thermalload_3min_20000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_thermalload_30min_1000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_thermalload_30min_5000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_thermalload_30min_20000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"

