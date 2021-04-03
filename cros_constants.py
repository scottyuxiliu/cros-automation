TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
AGT_DIR_PATH = "/usr/local/agt"
PERL_DIR_PATH = "/usr/local/perl"
GCC_DIR_PATH = "/usr/local/gcc"
COREBOOT_DIR_PATH = "/usr/local/coreboot"

MANUAL_SCENARIOS = {
    "idle": {
        "command": ""
    },
    "s0i3": {
        "command": "echo mem > /sys/power/state"
    },
    "stress-ng": {
        "command": "cd /usr/local; stress-ng -M --cpu=4 -t 300"
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
    "pvc-25m": {
        "method": "autotest",
        "control": "tests/power_VideoCall/control.25min"
    }
}