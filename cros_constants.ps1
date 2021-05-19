$DELAY_AFTER_BOOT = 180
$DELAY_AFTER_PROG = 900

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"
$AGT_PATH = "/usr/local/agt"
$AGT_INTERNAL_PATH = "/usr/local/agt_internal"

$SCENARIO_CONST = @{
    "idle" = @{
        "duration" = 300;
        "agt_log_time" = 300;
        "pwr_log_time" = 300;
        "result" = "na";
        "delay" = 0;
    };
    "s0i3" = @{
        "duration" = 300;
        "agt_log_time" = 300;
        "pwr_log_time" = 300;
        "result" = "na";
        "delay" = 900;
    };
    "stress_ng" = @{
        "duration" = 300;
        "agt_log_time" = 360;
        "pwr_log_time" = 300;
        "result" = "/usr/local";
        "delay" = 0;
    };
    "stress_ng_stop_ui" = @{
        "duration" = 300;
        "agt_log_time" = 360;
        "pwr_log_time" = 300;
        "result" = "/usr/local";
        "delay" = 0;
    };
    "graphics_webglaquarium" = @{
        "duration" = 120;
        "agt_log_time" = 180;
        "pwr_log_time" = 120;
        "result" = "/usr/local/autotest/results/default/graphics_WebGLAquarium/results";
        "delay" = 0;
    };
    "glbench" = @{
        "duration" = 1260;
        "agt_log_time" = 1260;
        "pwr_log_time" = 1260;
        "result" = "/usr/local/autotest/results/default/graphics_GLBench/results";
        "delay" = 0;
    };
    "power_idle" = @{
        "duration" = 660;
        "agt_log_time" = 900;
        "pwr_log_time" = 540;
        "result" = "/usr/local/autotest/results/default/power_Idle/results";
        "delay" = 0;
    };
    "power_loadtest_1h" = @{
        "duration" = 3600;
        "agt_log_time" = 3900;
        "pwr_log_time" = 3500;
        "result" = "/usr/local/autotest/results/default/power_LoadTest.1hour/results";
        "delay" = 0;
    };
    "power_speedometer2" = @{
        "duration" = 120;
        "agt_log_time" = 300;
        "pwr_log_time" = 120;
        "result" = "/usr/local/autotest/results/default/power_Speedometer2/results";
        "delay" = 0;
    };
    "power_thermalload" = @{
        "duration" = 9000;
        "agt_log_time" = 9600;
        "pwr_log_time" = 9000;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad/results";
        "delay" = 0;
    };
    "power_thermalload_3min_3000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 300;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_thermalload_3min_5000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 300;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_thermalload_3min_20000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 300;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_thermalload_30min_1000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 2100;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_thermalload_30min_5000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 2100;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_thermalload_30min_20000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 2100;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_videocall" = @{
        "duration" = 7200;
        "agt_log_time" = 7500;
        "pwr_log_time" = 7200;
        "result" = "/usr/local/autotest/results/default/power_VideoCall/results";
        "delay" = 0;
    };
    "power_videocall_25min" = @{
        "duration" = 1500;
        "agt_log_time" = 1800;
        "pwr_log_time" = 1500;
        "result" = "/usr/local/autotest/results/default/power_VideoCall.25min/results";
        "delay" = 0;
    };
    "arc.GamePerformanceRender" = @{
        "duration" = 1020;
        "agt_log_time" = 1320;
        "pwr_log_time" = 1020;
        "result" = "";
        "delay" = 0;
    }
}