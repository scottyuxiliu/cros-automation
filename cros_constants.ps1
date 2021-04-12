$DELAY_AFTER_BOOT = 180
$DELAY_AFTER_PROG = 900

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"
$TEST_SYS_AGT_PATH = "/usr/local/agt"

$SCENARIO_CONST = @{
    "idle" = @{
        "duration" = 300;
        "agt_log_time" = 300;
        "pwr_log_time" = 300;
        "result" = "na"
    };
    "stress_ng" = @{
        "duration" = 300;
        "agt_log_time" = 360;
        "pwr_log_time" = 300;
        "result" = "/usr/local"
    };
    "stress_ng_stop_ui" = @{
        "duration" = 300;
        "agt_log_time" = 360;
        "pwr_log_time" = 300;
        "result" = "/usr/local"
    };
    "graphics_webglaquarium" = @{
        "duration" = 120;
        "agt_log_time" = 180;
        "pwr_log_time" = 120;
        "result" = "/usr/local/autotest/results/default/graphics_WebGLAquarium/results"
    };
    "glbench" = @{
        "duration" = 1260;
        "agt_log_time" = 1260;
        "pwr_log_time" = 1260;
        "result" = "/usr/local/autotest/results/default/graphics_GLBench/results"
    };
    "plt-1h" = @{
        "duration" = 3600;
        "agt_log_time" = 3600;
        "pwr_log_time" = 3600;
        "result" = "/usr/local/autotest/results/default/power_LoadTest.1hour/results"
    };
    "power_thermalload" = @{
        "duration" = 9000;
        "agt_log_time" = 9600;
        "pwr_log_time" = 9000;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad/results"
    };
    "ptl-30m-1kfish" = @{
        "duration" = 1800;
        "agt_log_time" = 2100;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results"
    };
    "power_videocall" = @{
        "duration" = 7200;
        "agt_log_time" = 7500;
        "pwr_log_time" = 7200;
        "result" = "/usr/local/autotest/results/default/power_VideoCall/results"
    };
    "power_videocall_25min" = @{
        "duration" = 1500;
        "agt_log_time" = 1800;
        "pwr_log_time" = 1500;
        "result" = "/usr/local/autotest/results/default/power_VideoCall.25min/results"
    }
}