TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
AGT_DIR_PATH = "/usr/local/agt"
PERL_DIR_PATH = "/usr/local/perl"
GCC_DIR_PATH = "/usr/local/gcc"
COREBOOT_DIR_PATH = "/usr/local/coreboot"

AGT_COLS = ["CPU0 CORES Core0 Temp","CPU0 CORES Core1 Temp","CPU0 CORES Core2 Temp","CPU0 CORES Core3 Temp","CPU0 CORES Core0 Freq Eff","CPU0 CORES Core1 Freq Eff","CPU0 CORES Core2 Freq Eff","CPU0 CORES Core3 Freq Eff","CPU0 CORES Core0 C0","CPU0 CORES Core1 C0","CPU0 CORES Core2 C0","CPU0 CORES Core3 C0","CPU0 CORES Core0 OS Pstate","CPU0 CORES Core1 OS Pstate","CPU0 CORES Core2 OS Pstate","CPU0 CORES Core3 OS Pstate","CPU0 GFX GFX Temp","CPU0 GFX GFX Freq Eff","CPU0 GFX GFX Busy","CPU0 MISC APU Power","CPU0 MISC Skin Temp Margin","CPU0 MISC Peak Temperature","CPU0 MISC PROCHOT (%)","CPU0 MISC STAPM Time Constant","CPU0 MISC Slow PPT Time Constant","CPU0 STAPM Sustained Power Limit","CPU0 STAPM STAPM Value","CPU0 PPT PPT Limit FAST","CPU0 PPT PPT Value FAST","CPU0 PPT PPT Limit SLOW","CPU0 PPT PPT Value SLOW","CPU0 TDC TDC Limit VDDCR_VDD","CPU0 TDC TDC Limit VDDCR_SOC","CPU0 EDC EDC Limit VDDCR_VDD","CPU0 EDC EDC Limit VDDCR_SOC"]

MANUAL_SCENARIOS = {
    "idle": {
        "command": ""
    },
    "s0i3": {
        "command": "echo mem > /sys/power/state"
    },
    "stress_ng": {
        "command": "cd /usr/local; stress-ng -M --cpu=4 -t 300 --log-file keyval"
    },
    "stress_ng_stop_ui": {
        "command": "cd /usr/local; stop ui; stress-ng -M --cpu=4 -t 300 --log-file keyval"
    }
}


# graphics_WebGLAquarium
#             20s: preparation
#             45s: 50 fishes
#             45s: 1000 fishes

AUTOTEST_SCENARIOS = {
    "plt-1h": {
        "method": "autotest",
        "control": "tests/power_LoadTest/control.1hour"
    },
    "aquarium": {
        "method": "autotest",
        "control": "tests/graphics_WebGLAquarium/control"
    },
    "glbench": {
        "method": "autotest",
        "control": "tests/graphics_GLBench/control"
    },
    "ptl": {
        "method": "autotest",
        "control": "tests/power_ThermalLoad/control"
    },
    "ptl-30m-1kfish": {
        "method": "autotest",
        "control": "tests/power_ThermalLoad/control.30min.1000_fish"
    },
    "power_videocall": {
        "method": "autotest",
        "control": "tests/power_VideoCall/control"
    },
    "power_videocall_25min": {
        "method": "autotest",
        "control": "tests/power_VideoCall/control.25min"
    }
}