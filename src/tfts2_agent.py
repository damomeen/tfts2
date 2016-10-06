#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from json import dumps
from pprint import pformat
import pyagentx
import xmltodict
from parse_xmls import conv_float, get_value, get_param_no_ok, get_warning_level

XML_DIR = './'

logger = logging.getLogger(__name__)
        
class tfts2(pyagentx.Updater):
    def update(self):
        logger.info("\n" + '*'*80 + "\n\n\nUpdating MIB from xmls files in %s\n" % XML_DIR)
        self.update_local()
        self.update_remote()
        self.update_spba()
        logger.info("\n\n")
    
    def update_local(self):
        logger.info("\n\nUpdating from status_local.xml\n")
        try:
            xml = open(XML_DIR+'/status_local.xml', 'r').read()
            status = xmltodict.parse(xml)['status']
            param_list = status['params']['param']
            logger.debug(dumps(status['module']))
            logger.debug(dumps(param_list))
            
            """
            1       TFTS2MIBObjects 
            1.1    moduleInformation 
            1.1.1 moduleType (string)
            1.1.2 moduleVersion (string)
            1.1.3 moduleLocalization (string)
            1.1.4 moduleLaastSysttemUpdate  (string)
            1.1.5 moduleMode (string)
            """
            
            self.set_OCTETSTRING('1.1.1', status['module']['name'])
            self.set_OCTETSTRING('1.1.2', status['module']['version'])
            self.set_OCTETSTRING('1.1.3', status['module']['localization'])
            self.set_OCTETSTRING('1.1.4', status['module']['lastSystemUpdate'])
            self.set_OCTETSTRING('1.1.5', status['module']['mode'])
            
            """
            1.2    moduleParameters 
            1.2.1 localModuleParameters 
            1.2.1.1 lcl10MHzInputSignalDetected (bool)
            1.2.1.2 lclPPSInputSignalDetected (bool)
            1.2.1.3 lclPhaseCorrect (bool)
            1.2.1.4 lclFeedbackSignalDetected (bool)
            1.2.1.5 lclReceivedOpticalPower (bool)
            1.2.1.6 lclDelayCompensation (int)
            1.2.1.7 lclDelayCompensationThreshold (int)
            1.2.1.8 lclDelayCompensationOK (bool)
            1.2.1.9 lclInnerCaseTemperature (float)
            1.2.1.10 lclInnerCaseTemperatureThreshold (float)
            1.2.1.11 lclInnerCaseTemperatureOK (bool)
            """      
            self.set_INTEGER('1.2.1.1', get_param_no_ok(param_list, '10MHz input signal detected'))
            self.set_INTEGER('1.2.1.2', get_param_no_ok(param_list, 'PPS input signal detected'))
            self.set_INTEGER('1.2.1.3', get_param_no_ok(param_list, 'PPS phase correct'))
            self.set_INTEGER('1.2.1.4', get_param_no_ok(param_list, 'Feedback signal  detected'))
            self.set_INTEGER('1.2.1.5', get_param_no_ok(param_list, 'Received optical power'))
            
            warning, level = get_warning_level(param_list, 'Delay compensation', remove='%', cast=int)
            self.set_INTEGER('1.2.1.6', level)
            self.set_INTEGER('1.2.1.8', warning)
            
            warning, level = get_warning_level(param_list, 'Inner case temperature')
            self.set_OCTETSTRING('1.2.1.9', conv_float(level[:-2]))
            self.set_INTEGER('1.2.1.11', warning)
        except:
            import traceback
            logger.error(traceback.format_exc())
            
    def update_remote(self):
        logger.info("\n\nUpdating from status_remote.xml\n")
        try:
            xml = open(XML_DIR+'/status_remote.xml', 'r').read()
            status = xmltodict.parse(xml)['status']
            param_list = status['params']['param']
            logger.debug(dumps(param_list))
            
            '''
            1.2.2 remoteModuleParameters 
            1.2.2.1 rmtRemoteModuleSynchronized (bool)
            1.2.2.2 rmtPLLControlVoltage (float)
            1.2.2.3 rmtPLLControlVoltageThreshold (float)
            1.2.2.4 rmtPLLControlVoltageOK (bool)
            1.2.2.5 rmtPPSSignalDetected (bool)
            1.2.2.6 rmtFeedbackSignalDetected (bool)
            1.2.2.7 rmtReceivedOpticalPower (float)
            1.2.2.8 rmtReceivedOpticalPowerThreshold (float)
            1.2.2.9 rmtReceivedOpticalPowerOK (bool)
            1.2.2.10 rmtInnerCaseTemperature (float)
            1.2.2.11 rmtInnerCaseTemperatureThreshold (float)
            1.2.2.12 rmtInnerCaseTemperature (bool)
            '''
            
            self.set_INTEGER('1.2.2.1', get_param_no_ok(param_list, 'Remote module synchronized'))
            
            warning, level = get_warning_level(param_list, 'PLL control voltage', remove='V', cast=conv_float)
            self.set_OCTETSTRING('1.2.2.2', level)
            self.set_INTEGER('1.2.2.4', warning)
            
            self.set_INTEGER('1.2.2.5', get_param_no_ok(param_list, 'PPS signal detected'))
            self.set_INTEGER('1.2.2.6', get_param_no_ok(param_list, 'Feedback signal  detected'))
            
            warning, level = get_warning_level(param_list, 'Received optical power', remove='dBm', cast=conv_float)
            self.set_OCTETSTRING('1.2.2.7', level)
            self.set_INTEGER('1.2.2.9', warning)
            
            warning, level = get_warning_level(param_list, 'Inner case temperature')
            self.set_OCTETSTRING('1.2.2.10', conv_float(level[:-2]))
            self.set_INTEGER('1.2.2.11', warning)
        except:
            import traceback
            logger.error(traceback.format_exc())
            
    def update_spba(self):
        logger.info("\n\nUpdating from status_spba.xml\n")
        try:
            xml = open(XML_DIR+'/status_spba.xml', 'r').read()
            status = xmltodict.parse(xml)['status']
            param_list = status['params']['param']
            logger.debug(dumps(param_list))
            
            '''
            1.2.3 spbaModuleParameters 
            1.2.3.1 spbaModuleParameters (string)
            1.2.3.2 spbaMode (string)
            1.2.3.3 spbaControl (string)
            1.2.3.4 spbaLockedGain (float)
            1.2.3.5 spbaDir (string)
            1.2.3.6 spbaPumpCurrent (float)
            1.2.3.7 spbaTemperature (float)
            '''

            self.set_OCTETSTRING('1.2.3.1', get_value(param_list, 'SPBA Name'))
            self.set_OCTETSTRING('1.2.3.2', get_value(param_list, 'Mode'))
            self.set_OCTETSTRING('1.2.3.3', get_value(param_list, 'Control'))
            self.set_OCTETSTRING('1.2.3.4', get_value(param_list, 'Locked Gain', remove='dBm', cast=conv_float))
            self.set_OCTETSTRING('1.2.3.5', get_value(param_list, 'Dir'))
            self.set_OCTETSTRING('1.2.3.6', get_value(param_list, 'PumpI', remove='mA', cast=conv_float))
            self.set_OCTETSTRING('1.2.3.7', get_value(param_list, 'Temp',  remove='C', cast=conv_float))
        except:
            import traceback
            logger.error(traceback.format_exc())

class tfts2_agent(pyagentx.Agent):
    def __init__(self, xmls_dir='../xmls', freq=10):
        pyagentx.Agent.__init__(self)
        global XML_DIR
        XML_DIR = xmls_dir
        self.freq = freq
        
    def setup(self):
        self.register('1.3.6.1.4.1.38980.1234', tfts2, freq=self.freq)



if __name__ == '__main__':
    pyagentx.setup_logging(True)
    try:
        a = tfts2_agent()
        a.start()
    except Exception as e:
        print "Unhandled exception:", e
        a.stop()
    except KeyboardInterrupt:
        a.stop()
