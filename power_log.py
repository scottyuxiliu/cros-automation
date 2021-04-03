# DAQTools Module

#+-------------------------------------------------------------------+
#|                                                                   |
#|   DAQ TOOLS MODULE                                                |
#|                                                                   |
#|   rev = 2018.05.30.1702                                           | --- [jelui] initial revision 
#|                                                                   |
#+-------------------------------------------------------------------+

import argparse
import os
import sys

import time
import shutil
import requests
import subprocess

import pathlib





# Set up logging
import logging

logger = logging.getLogger('power_log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('power_log_debug.log') # to overwrite existing log file, use mode="w"
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


#+----------------------+
#| INITIALIZE VARIABLES |
#+----------------------+
therm_steady_state_delay = 10

# config_file = '\vausamd25\PPO1\ppomkserver\Depot\Projects\matisse-am4\daq-config\daqtool_matisse_am4_turpandap_ddr4_1card_cpu_mem_s0.xml'

config_file = str( pathlib.PureWindowsPath(r'\\vausamd25\PPO1\ppomkserver\Depot\Projects\matisse-am4\daq-config\daqtool_matisse_am4_turpandap_ddr4_1card_cpu_mem_s0.xml') )
config_file = str( pathlib.PureWindowsPath(r'\\vausamd25\PPO1\ppomkserver\Depot\Projects\Picasso\daq-config\daqtool_picasso_fp5_mandolindap_ddr4_1card_apu_mem_s0_s3_s5.xml') )

rdaq_service_url = 'http://desktop-o0rqd95:1025/DaqTool'
rdaq_service_url = 'http://ppomkhostll:1025/DaqTool'

results_folder = str( pathlib.PureWindowsPath(r'C:\Users\jaoliu\Documents\AMD\matisse-am4\measured-results\matisse_am4_proto_wmx9403n_windows10_18362.53_default_idlepwr') )

daq_logger_file_ext = "nidata.csv"




#+--------------------------+
#| START CLI DAQTOOL SERVER |
#+--------------------------+
def startCLIDAQToolServer( _daq_tool ):
    print( "Starting {0} server instance".format(_daq_tool) )
    subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " --start-server"])
    time.sleep(1)
    return

#+-------------------------+
#| STOP CLI DAQTOOL SERVER |
#+-------------------------+
def stopCLIDAQToolServer( _daq_tool ):
    print( "Stopping {0} server instance".format(_daq_tool) )
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " --exit"])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " --exit"])
    time.sleep(1)
    return

#+------------------------------+
#| START CLI POWER DATA CAPTURE |
#+------------------------------+
def startCLIPowerDataCapture( _daq_tool, _results_folder, _ace_file_ext ):
    print( "Starting DAQTool Power Capture" )
    _ace_daq_file_path = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _ace_file_ext 
    # print _ace_daq_file_path	
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " StartCapture " + _ace_daq_file_path ])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " StartCapture " + _ace_daq_file_path ])
    time.sleep(1)
    return

#+-----------------------------+
#| STOP CLI POWER DATA CAPTURE |
#+-----------------------------+
def stopCLIPowerDataCapture ( _daq_tool ):
    print( "Stopping DAQTool Power Capture" )
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " StopCapture"])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " StopCapture"])
    time.sleep(1)
    return

#+------------------------------+
#| LOAD CLI DAQTOOL CONFIG FILE |
#+------------------------------+
def loadCLIDAQToolConfigFile( _daq_tool, _config_file ):
    print( "Loading CLI DAQTool Config file: {0}".format(_config_file) )
    #subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " LoadConfig " + _config_file])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " LoadConfig " + _config_file])
    # wait until config file fully loads
    time.sleep(5)
    return

#+------------------------------+
#| ADJUST CLI THERMAL SET POINT |
#+------------------------------+	
def adjustCLIThermalSetPoint( _daq_tool, _therm_set_point ):
    print( "Adjusting CLI Thermal Head to Set Point: {0}".format(str(_therm_set_point)) )
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " SetDeviceAttribute FeedbackChiller FeedbackTarget " + str(_therm_set_point)])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " SetDeviceAttribute FeedbackChiller FeedbackTarget " + str(_therm_set_point)])
    # delay 1min for thermal steady state
    time.sleep(therm_steady_state_delay)
    return
	
#+-------------------------------+
#| START RDAQ POWER DATA CAPTURE |
#+-------------------------------+
def startRDAQPowerDataCapture( _rdaq_service_url ):
    ''' For HOBL only

    '''

    # print "Using the following config file: "
    # _content = requests.get(url = _rdaq_service_url + "//Configuration")
    # print _content.json

    print( "Starting RDAQ DAQTool Power Capture" )
    requests.get(url = _rdaq_service_url + "//Measurement//Start") 
    time.sleep(1)
    return

#+------------------------------+
#| STOP RDAQ POWER DATA CAPTURE |
#+------------------------------+
def stopRDAQPowerDataCapture( _rdaq_service_url, _results_folder, _daq_logger_file_ext ):
    ''' For HOBL only

    '''
    _rdaq_power_file = _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    
    print( "Stopping RDAQ DAQTool Power Capture: {0}".format(_rdaq_power_file) )
    
    requests.get(url = _rdaq_service_url + "//Measurement//Stop//" + _rdaq_power_file)
    time.sleep(1)
    return



#+-------------------------------+
#| LOAD RDAQ DAQTOOL CONFIG FILE |
#+-------------------------------+
def loadRDAQDAQToolConfigFile( _rdaq_service_url, _config_file ):
    print( "Loading RDAQ DAQTool Config File: {0}".format(_config_file) )
    _content = { "FilePath" : _config_file }
    requests.post(_rdaq_service_url + "//Configuration//LoadFromFile", json=_content)
    time.sleep(1)
    return

#+---------------------------------+
#| GET RDAQ OUTPUT SHARE DIRECTORY |
#+---------------------------------+
def getRDAQOutputShareDirectory ( _rdaq_service_url ):
    print( "Getting RDAQ DAQTool Output Share Directory" )
	# example content <string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">\\LPP-HOST2\Logs</string>
    _resp = requests.get(_rdaq_service_url + "//OutputShareDirectory")
    _outputShareDirectory = _resp.content
    _outputShareDirectory = _outputShareDirectory.split(">")[1]
    _outputShareDirectory = _outputShareDirectory.split("<")[0]
    print( "RDAQ DAQTool Output Share Directory is located at: {0}".format(_outputShareDirectory) )
    return _outputShareDirectory
	
#+-----------------------------------------+
#| GET CURRENT RDAQ MONITORED TEMPERATURED |
#+-----------------------------------------+
def getCurrentRDAQMonitoredTemperature ( _rdaq_service_url ):
    print( "Getting current reading of RDAQ Monitored Temperature" )
    _resp = requests.get(_rdaq_service_url + "//FeedbackChiller//Temperature")
    _temperature = _resp.content
    _temperature = _temperature.split(">")[1]
    _temperature = _temperature.split("<")[0]
    print( "Current RDAQ Monitored Temperature: {0}".format(_temperature) )
    return

#+------------------------------------------------------------------+
#| START RDAQ FEEDBACK CHILLER AND SPECIFY TARGET THERMAL SET POINT |
#+------------------------------------------------------------------+
def startRDAQFeedbackChiller ( _rdaq_service_url, _therm_set_point):
    print( "Starting RDAQ feedback chiller and setting target thermal set point to: {0}".format(str(_therm_set_point)) )
    _resp = requests.get(_rdaq_service_url + "//FeedbackChiller//Start//" + str(_therm_set_point))
    return

#+--------------------------------------------------------------+
#| STOP RDAQ FEEDBACK CHILLER AND SPECIFY FAIL SAFE TEMPERATURE |
#+--------------------------------------------------------------+
def stopRDAQFeedbackChiller ( _rdaq_service_url, _fail_safe_temp ):
    print( "Stopping RDAQ feedback chiller and setting fail safe temperature: {0}".format(str(_fail_safe_temp)) )
    _resp = requests.get(_rdaq_service_url + "//FeedbackChiller//Stop//" + str(_fail_safe_temp))
    return

#+-------------------------------------------------------------------------+
#| MOVE RDAQ POWER DATA FROM OUTPUT SHARE DIRECTORY TO SPECIFIED DIRECTORY |
#+-------------------------------------------------------------------------+
def moveRDAQPowerDataFile ( _rdaq_service_url, _results_folder, _daq_logger_file_ext):
    _source = getRDAQOutputShareDirectory( _rdaq_service_url )
    _source = _source + "\\" + _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    _destination = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    print( "Moving RDAQ power from {0} to {1}".format(_source, _destination) )
    shutil.move(_source, _destination)
    return

#+-------------------------------------------------------------------------+
#| COPY RDAQ POWER DATA FROM OUTPUT SHARE DIRECTORY TO SPECIFIED DIRECTORY |
#+-------------------------------------------------------------------------+
def copyRDAQPowerDataFile ( _rdaq_service_url, _results_folder, _daq_logger_file_ext):
    _source = getRDAQOutputShareDirectory( _rdaq_service_url )
    _source = _source + "\\" + _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    _destination = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    print( "Copying RDAQ power from {0} to {1}".format(_source, _destination) )
    shutil.copy(_source, _destination)
    return


#+--------------------------------+
#| CONVERT FROM ACE TO DAQ LOGGER |
#+--------------------------------+
def convertACEtoDAQLogger( _daq_tool, _results_folder, _ace_file_ext, _daq_logger_file_ext ):
    print( "Converting power data file from ACE DAQ file format to DAQ Logger file format" )
    _ace_daq_file_path = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _ace_file_ext
    _daq_logger_file_path = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _daq_logger_file_ext
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + _daq_tool + " --convert-to-csv " + _ace_daq_file_path + " " + _daq_logger_file_path])
    subprocess.call(["cmd.exe", "/C cmd /C " + _daq_tool + " --convert-to-csv " + _ace_daq_file_path + " " + _daq_logger_file_path])
    time.sleep(1)
    return

#+---------------------+
#| DELETE ACE DAQ FILE |
#+---------------------+
def deleteACEFile( _results_folder, _ace_file_ext ):
    print( "Deleting ACE DAQ power data file" )
    _ace_daq_file_path = _results_folder + "\\" + _results_folder.split("\\")[-1] + "_" + _ace_file_ext
    # subprocess.call(["cmd.exe", "/C START /MIN cmd /C " + "del " + _ace_daq_file_path])
    subprocess.call(["cmd.exe", "/C cmd /C " + "del " + _ace_daq_file_path])
    time.sleep(1)
    return

#+--------------------------+
#| CHANGE WORKING DIRECTORY |
#+--------------------------+
def changeWorkingDirectory( _directory ):
    print( "Changing working directory to {0}".format(_directory) )
    os.chdir(_directory)
    time.sleep(1)
    return










def load_rdaq_config_file(rdaq_service_url, config_file):
    ''' For all other test purposes

    '''

    logger.info( "Loading RDAQ DAQTool Config File: {0}".format(config_file) )
    content = { "FilePath" : config_file }
    requests.post(rdaq_service_url + "//Configuration//LoadFromFile", json=content)
    time.sleep(1)
    return


def get_rdaq_log_dir(rdaq_service_url):
    ''' For all other test purposes


    '''

    logger.info( 'Getting RDAQ DAQTool Output Share Directory' )

    resp = requests.get(rdaq_service_url + "//OutputShareDirectory")
    content = str(resp.content)

    logger.debug('server response: {0}'.format(content))

    logger.debug('Extracting directory from the response content. Directory is between {0} and {1}'.format(content.find('>')+1, content.rfind('<')))
    rdaq_log_dir = content[content.find('>')+1 : content.rfind('<')]

    rdaq_log_dir = '\\' + str( pathlib.PureWindowsPath(rdaq_log_dir) )

    logger.info( "RDAQ DAQTool Output Share Directory is located at: {0}".format(rdaq_log_dir) )
    return rdaq_log_dir


def start_rdaq_power_capture(rdaq_service_url):
    ''' For all other test purposes
    
    '''

    logger.info( "Starting RDAQ DAQTool Power Capture" )
    requests.get(url = rdaq_service_url + "//Measurement//Start") 
    time.sleep(1)
    return


def stop_rdaq_power_capture(rdaq_service_url, results_folder, rdaq_power_file):
    ''' For all other test purposes

    '''
    
    logger.info( "Stopping RDAQ DAQTool Power Capture: {0}".format(rdaq_power_file) )
    
    requests.get(url = rdaq_service_url + "//Measurement//Stop//" + rdaq_power_file)
    time.sleep(1)
    return


def copy_rdaq_power_data_file(rdaq_service_url, results_folder, rdaq_power_file, source=None):
    ''' For all other test purposes

    '''

    if source is None:
        source = get_rdaq_log_dir(rdaq_service_url)
    else:
        pass
    
    source = os.path.join(source, rdaq_power_file)
    destination = os.path.join(results_folder, rdaq_power_file)

    logger.info( "Copying RDAQ power from {0} to {1}".format(source, destination) )

    shutil.copy(source, destination)
    return


#+-------------------+
#| CAPTURE ARGUMENTS |
#+-------------------+

parser = argparse.ArgumentParser(description='Power logging utility')
parser.add_argument('-m', '--mode', default='normal', help='mode, default "normal", possible values: "normal", "hobl"')

parser.add_argument('-b', '--begin', action='store_true', help='begin power logging')
parser.add_argument('-e', '--end', action='store_true', help='end power logging')


parser.add_argument('-c', '--config', help='config file path')
parser.add_argument('-u', '--url', help='RDAQ service URL')
parser.add_argument('-o', '--output', help='The output file name')
parser.add_argument('-d', '--directory', help='the results directory')
parser.add_argument('-s', '--source', default=None, help='the source directory')

args = parser.parse_args()

if args.mode == 'normal':

    if args.begin:

        logger.info("--------------------------------------------------------")
        logger.info("START POWER LOGGING USING RDAQ SERVICE")
        logger.info("--------------------------------------------------------")

        if args.config is None:
            raise ValueError('Config file path not provided. Please provide valid config file path!')

        elif args.url is None:
            raise ValueError('RDAQ service URL not provided. Please provide valid RDAQ service URL!')

        else:
            logger.debug('config_file: {0}'.format(args.config))

            load_rdaq_config_file(rdaq_service_url=args.url, config_file=args.config)
            start_rdaq_power_capture(rdaq_service_url=args.url)

    elif args.end:

        logger.info("--------------------------------------------------------")
        logger.info("STOP POWER LOGGING USING RDAQ SERVICE")
        logger.info("--------------------------------------------------------")

        if args.url is None:
            raise ValueError('RDAQ service URL not provided. Please provide valid RDAQ service URL!')

        elif args.directory is None:
            raise ValueError('The results directory not provided. Please provide valid results directory!')

        elif args.output is None:
            raise ValueError('The output file name not provided. Please provide valid output file name!')

        else:
            logger.debug('results_folder: {0}'.format(args.directory))

            stop_rdaq_power_capture(rdaq_service_url=args.url, results_folder=args.directory, rdaq_power_file=args.output)
            copy_rdaq_power_data_file(
                rdaq_service_url=args.url,
                results_folder=args.directory,
                rdaq_power_file=args.output,
                source=args.source
            )