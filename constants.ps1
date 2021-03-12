$DELAY_AFTER_BOOT = 180

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"
$TEST_SYS_AGT_PATH = "/usr/local/agt"

$SCENARIO_CONST = @{
    "aquarium" = @{
        "duration" = 120;
        "agt_log_time" = 180;
        "pwr_log_time" = 120;
        "result" = "results/default/graphics_WebGLAquarium/results"
    };
    "glbench" = @{
        "duration" = 1260;
        "agt_log_time" = 1260;
        "pwr_log_time" = 1260;
        "result" = "results/default/graphics_GLBench/results"
    };
    "plt-1h" = @{
        "duration" = 3600;
        "agt_log_time" = 3600;
        "pwr_log_time" = 3600;
        "result" = "results/default/power_LoadTest.1hour/results"
    };
    "ptl" = @{
        "duration" = 9000;
        "agt_log_time" = 9600;
        "pwr_log_time" = 9000;
        "result" = "results/default/power_ThermalLoad/results"
    };
    "ptl-30m-1kfish" = @{
        "duration" = 1800;
        "agt_log_time" = 2100;
        "pwr_log_time" = 1800;
        "result" = "results/default/power_ThermalLoad.option/results"
    }
}