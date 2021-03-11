$DELAY_AFTER_BOOT = 180

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"
$TEST_SYS_AGT_PATH = "/usr/local/agt"

$SCENARIO_CONST = @{
    "aquarium" = @{
        "duration" = 120;
        "agt_log_time" = 180;
        "pwr_log_time" = 120;
        "id" = "graphics_WebGLAquarium"
    }
    "glbench" = @{
        "duration" = 1260;
        "agt_log_time" = 1260;
        "pwr_log_time" = 1260;
        "id" = "graphics_GLBench"
    }
    "plt-1h" = @{
        "duration" = 3600;
        "agt_log_time" = 3600;
        "pwr_log_time" = 3600;
        "id" = "power_LoadTest.1hour"
    }
    "ptl" = @{
        "duration" = 9000;
        "agt_log_time" = 9600;
        "pwr_log_time" = 9000;
        "id" = "power_ThermalLoad"
    }
}