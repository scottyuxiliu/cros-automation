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
AUTOTEST_DURATION["login_GaiaLogin"]=300
AUTOTEST_DURATION["graphics_WebGLAquarium"]=120
AUTOTEST_DURATION["power_Idle"]=660
AUTOTEST_DURATION["power_Speedometer2"]=120
AUTOTEST_DURATION["power_ThermalLoad.3min.3000_fish"]=180
AUTOTEST_DURATION["power_ThermalLoad.3min.5000_fish"]=180
AUTOTEST_DURATION["power_ThermalLoad.3min.20000_fish"]=180
AUTOTEST_DURATION["power_ThermalLoad.30min.1000_fish"]=1800
AUTOTEST_DURATION["power_ThermalLoad.30min.3000_fish"]=1800
AUTOTEST_DURATION["power_ThermalLoad.30min.5000_fish"]=1800
AUTOTEST_DURATION["power_ThermalLoad.30min.20000_fish"]=1800
AUTOTEST_DURATION["power_ThermalLoad.60min.3000_fish"]=3600
AUTOTEST_DURATION["power_ThermalLoad.60min.5000_fish"]=3600
AUTOTEST_DURATION["power_VideoCall"]=7200
AUTOTEST_DURATION["power_LoadTest.1hour"]=3600


declare -A AUTOTEST_RESULT_DIR
AUTOTEST_RESULT_DIR["login_GaiaLogin"]="na"
AUTOTEST_RESULT_DIR["graphics_WebGLAquarium"]="/usr/local/autotest/results/default/graphics_WebGLAquarium/results"
AUTOTEST_RESULT_DIR["power_Idle"]="/usr/local/autotest/results/default/power_Idle/results"
AUTOTEST_RESULT_DIR["power_Speedometer2"]="/usr/local/autotest/results/default/power_Speedometer2/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.3min.3000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.3min.5000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.3min.20000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.30min.1000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.30min.3000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.30min.5000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.30min.20000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.60min.3000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_ThermalLoad.60min.5000_fish"]="/usr/local/autotest/results/default/power_ThermalLoad.option/results"
AUTOTEST_RESULT_DIR["power_VideoCall"]="/usr/local/autotest/results/default/power_VideoCall/results"
AUTOTEST_RESULT_DIR["power_LoadTest.1hour"]="/usr/local/autotest/results/default/power_LoadTest.1hour/results"


declare -A AGT_LOG_TIME
AGT_LOG_TIME["login_GaiaLogin"]=300
AGT_LOG_TIME["graphics_WebGLAquarium"]=180
AGT_LOG_TIME["power_Idle"]=760
AGT_LOG_TIME["power_Speedometer2"]=180
AGT_LOG_TIME["power_ThermalLoad.3min.3000_fish"]=240
AGT_LOG_TIME["power_ThermalLoad.3min.5000_fish"]=240
AGT_LOG_TIME["power_ThermalLoad.3min.20000_fish"]=240
AGT_LOG_TIME["power_ThermalLoad.30min.1000_fish"]=1900
AGT_LOG_TIME["power_ThermalLoad.30min.3000_fish"]=1900
AGT_LOG_TIME["power_ThermalLoad.30min.5000_fish"]=1900
AGT_LOG_TIME["power_ThermalLoad.30min.20000_fish"]=1900
AGT_LOG_TIME["power_ThermalLoad.60min.3000_fish"]=3700
AGT_LOG_TIME["power_ThermalLoad.60min.5000_fish"]=3700
AGT_LOG_TIME["power_VideoCall"]=7300
AGT_LOG_TIME["power_LoadTest.1hour"]=3700

