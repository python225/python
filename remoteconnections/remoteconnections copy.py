#!/usr/bin/python

import netifaces
import json
import socket
import fcntl
import struct
import psutil
import logging
import os
import platform
import dmidecode
import subprocess
import datetime
from subprocess import check_output
import collections
import time


log_file_name_text = '_netstats_'


"""
Fetch the Host name of the current Host
"""
def get_host_name():
    name_host = socket.gethostname().split('.')[0]
    return name_host
name_host = get_host_name()


"""
Fetching the time-stamp
"""
def get_tm():
       a = datetime.datetime.now()
       return str(a)
time_stamp = get_tm()



"""
Fetching the active connections on the current host
"""

def get_active_connections():
    active_connections= []
    for connection in psutil.net_connections():
        tmp_active_connection = {}
        if connection.type == 1:
            tmp_active_connection['Connection_Type'] = 'TCP'
            tmp_active_connection['Local_Port'] = connection.laddr[1]
            tmp_active_connection['LocalIP'] = connection.laddr[0]
            tmp_active_connection['ReportDateTime'] = time_stamp
            tmp_active_connection['LocalHostName'] = name_host
            if not connection.raddr:
                tmp_active_connection['RemoteIP'] = 'Null'
                tmp_active_connection['Remote-Port'] = 'Null'
            else:
                tmp_active_connection['RemoteIP'] = connection.raddr[0]
                tmp_active_connection['Remote_Port'] = connection.raddr[1]

        elif connection.type  == 2:
            tmp_active_connection['Connection_Type'] = 'UDP'
            tmp_active_connection['Local_Port'] = connection.laddr[1]
            tmp_active_connection['LocalIP'] = connection.laddr[0]
            tmp_active_connection['ReportDateTime'] = time_stamp
            tmp_active_connection['LocalHostName'] = name_host
            if not connection.raddr:
                tmp_active_connection['RemoteIP'] = 'Null'
                tmp_active_connection['Remote-Port'] = 'Null'
            else:
                tmp_active_connection['RemoteIP'] = connection.raddr[0]
                tmp_active_connection['Remote-Port'] = connection.raddr[1]
        else:
            tmp_active_connection['Connection_Type'] = connection.type
            tmp_active_connection['Local_Port'] = connection.laddr[1]
            tmp_active_connection['LocalIP'] = connection.laddr[0]
            if not connection.raddr:
                tmp_active_connection['RemoteIP'] = 'Null'
                tmp_active_connection['Remote-Port'] = 'Null'
            else:
                tmp_active_connection['RemoteIP'] = connection.raddr[0]
                tmp_active_connection['Remote-Port'] = connection.raddr[1]
      
        active_connections.append(tmp_active_connection)
    return active_connections

connections = get_active_connections()


if __name__ == "__main__":

    all_values = {'active_connections':connections}
    od_all = collections.OrderedDict(sorted(all_values.items()))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_network_shared_location = json.loads(open("/mnt/Backups/Ensight/configurations/config.json").read())["RemoteConnectionsDataNetworkShareRootPath"]
    filename = os.path.expanduser(path_network_shared_location) + name_host.strip() + log_file_name_text + timestamp + '.json'
    file_handler = open(filename,'a+')
    text_json = json.dumps(od_all, indent=4)
    print >> file_handler,text_json
    file_handler.close()
    
