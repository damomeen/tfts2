# Copyright 2016 Poznan Supercomputing and Networking Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

tfts2
----------------

1. Overview

'tfts2' subagent plugin for NET-SNMP.
    
    
2. Installation

2.1 Requirements

    - Python 2.7 (https://www.python.org/)
    - Net-SNMP (www.net-snmp.org/)
    - pyagentx (https://github.com/rayed/pyagentx)
    - xmltodict (https://github.com/martinblech/xmltodict)
    
    1. Install python libraries by pip:
        pip install pyagentx xmltodict
        
2.2 Download from github:

    git clone https://github.com/damomeen/tfts2
    
    
3. Setup

3.1 Net-SNMP agent configuration

    1. Edit snmpd.conf: 
        nano /etc/snmp/snmpd.conf
        
        and add following config lines:
        
            master  agentx
            view  systemview  included   .1.3.6.1.4.1.38980.1234
            rocommunity  public  default
            
        Review other settings in this configuration file.

    2. Restart snmp agent:
        /etc/init.d/snmpd restart
        
3.2 tfts2 subagent configuratioin

    1. add right to execute ./tfts2/src/tfts2
        chmod +x ./tfts2/src/tfts2
        
    2. add ./tfts2/src to PATH environment variable in order to allow run 'tfts2' anywhere.
        Make this permament in '.bashrc', '.bash_profile', etc.
        cd ./tfts2/src
        export PATH=$PATH:`pwd`
        
4. Start up

    1. See help by running tfts2 without arguments:
        tfts2
        
        will produce the output:
            Usage: tfts2 [options] start|stop|restart

            Options:
              --version             show program's version number and exit
              -h, --help            show this help message and exit
              -p PIDDIR, --pidDir=PIDDIR
                                        directory for pid file (default: ./tmp/)
              -l LOGDIR, --logDir=LOGDIR
                                        directory for log file (default: ./tfts2/log/)
              -x XMLDIR, --xmlDir=XMLDIR
                                        directory containing xml files (default: ./tfts2/xmls/) 
              -f FREQ, --freq=FREQ  How frequently (in seconds) xmls should be checked
                                        (default: 10 seconds)


    2. run 'tfts2' service from any location:
        tfts2 start
        
        or run 'tfts2' service specifing from where monitored xml files are:
        tfts2 start -x <xmls-dir>
        
    3. stop 'tfts2' service from any location:
        tfts2 stop
        
    4. make test:
        snmpwalk -v 2c -c public localhost 1.3.6.1.4.1.38980.1234
        
        
