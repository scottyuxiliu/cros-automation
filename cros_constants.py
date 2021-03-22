TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
AGT_DIR_PATH = "/usr/local/agt"
PERL_DIR_PATH = "/usr/local/perl"
GCC_DIR_PATH = "/usr/local/gcc"



# graphics_WebGLAquarium
#             20s: preparation
#             45s: 50 fishes
#             45s: 1000 fishes

AUTOTEST_SCENARIOS = {
    "plt-1h": "tests/power_LoadTest/control.1hour",
    "aquarium": "tests/graphics_WebGLAquarium/control",
    "glbench": "tests/graphics_GLBench/control",
    "ptl": "tests/power_ThermalLoad/control",
    "ptl-30m-1kfish": "tests/power_ThermalLoad/control.30min.1000_fish"
}