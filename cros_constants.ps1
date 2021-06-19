$DELAY_AFTER_BOOT = 180
$DELAY_AFTER_PROG = 900

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"
$AGT_PATH = "/usr/local/agt"
$AGT_INTERNAL_PATH = "/usr/local/agt_internal"

$LOGS = @(
    "cros_data_logger.log",
    "cros_data_parser.log",
    "cros_file_handler.log",
    "cros_scenario_launcher.log",
    "cros_software_controller.log"
)

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
    "graphics_WebGLAquarium" = @{
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
    "power_Idle" = @{
        "duration" = 660;
        "agt_log_time" = 760;
        "pwr_log_time" = 540;
        "result" = "/usr/local/autotest/results/default/power_Idle/results";
        "delay" = 0;
    };
    "power_LoadTest.1hour" = @{
        "duration" = 3600;
        "agt_log_time" = 3700;
        "pwr_log_time" = 3500;
        "result" = "/usr/local/autotest/results/default/power_LoadTest.1hour/results";
        "delay" = 0;
    };
    "power_Speedometer2" = @{
        "duration" = 120;
        "agt_log_time" = 180;
        "pwr_log_time" = 120;
        "result" = "/usr/local/autotest/results/default/power_Speedometer2/results";
        "delay" = 0;
    };
    "power_ThermalLoad" = @{
        "duration" = 9000;
        "agt_log_time" = 9100;
        "pwr_log_time" = 9000;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad/results";
        "delay" = 0;
    };
    "power_ThermalLoad.3min.3000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 240;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.3min.5000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 240;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.3min.20000_fish" = @{
        "duration" = 180;
        "agt_log_time" = 240;
        "pwr_log_time" = 180;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.30min.1000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 1900;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.30min.3000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 1900;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.30min.5000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 1900;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.30min.20000_fish" = @{
        "duration" = 1800;
        "agt_log_time" = 1900;
        "pwr_log_time" = 1800;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.60min.3000_fish" = @{
        "duration" = 3600;
        "agt_log_time" = 3700;
        "pwr_log_time" = 3600;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.60min.5000_fish" = @{
        "duration" = 3600;
        "agt_log_time" = 3700;
        "pwr_log_time" = 3600;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_ThermalLoad.150min.3000_fish" = @{
        "duration" = 9000;
        "agt_log_time" = 9100;
        "pwr_log_time" = 9000;
        "result" = "/usr/local/autotest/results/default/power_ThermalLoad.option/results";
        "delay" = 0;
    };
    "power_VideoCall" = @{
        "duration" = 7200;
        "agt_log_time" = 7300;
        "pwr_log_time" = 7200;
        "result" = "/usr/local/autotest/results/default/power_VideoCall/results";
        "delay" = 0;
    };
    "power_VideoCall.25min" = @{
        "duration" = 1500;
        "agt_log_time" = 1800;
        "pwr_log_time" = 1500;
        "result" = "/usr/local/autotest/results/default/power_VideoCall.25min/results";
        "delay" = 0;
    };
    "arc.GamePerformanceRender" = @{
        "duration" = 1020;
        "agt_log_time" = 1080;
        "pwr_log_time" = 1020;
        "result" = "";
        "delay" = 0;
    };
    "ui.MeetCUJ.16p_notes" = @{
        "duration" = 220;
        "agt_log_time" = 280;
        "pwr_log_time" = 220;
        "result" = "";
        "delay" = 0;
    }
}