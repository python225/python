#!/usr/bin/python
import subprocess
import netifaces
import json
import socket
import fcntl
import struct
import os
import datetime
import collections
import time


"""
 Defining this value for the purpose of file name
"""

log_file_name_text = '_networkusage_'

"""
Fetch the Host name of the current Host
"""
def get_host_name():
    name_host = socket.gethostname().split('.')[0]
    return name_host
name_of_host = get_host_name()

"""
Fetching the current time 
"""

def get_tm():
       a = datetime.datetime.now()
       return str(a)
time_value = get_tm()


"""
Fetching the name of the Nic
"""

def get_nics():
    cmd_ifconfig_1="ifconfig -a | sed 's/[ \t].*//;/^$/d'"
    str_of_nics = subprocess.check_output(cmd_ifconfig_1, shell=True)
    list_of_nics = str_of_nics.splitlines()
    return list_of_nics



def nics_with_config():
    all_nics = get_nics()
    nic_list_with_conf = []
    for nic in all_nics:
        path = "/etc/sysconfig/network-scripts/" + "ifcfg-" + nic.replace(':','')
        value = os.path.isfile(path)
        if value:
            nic_list_with_conf.append(nic.replace(':',''))
    return nic_list_with_conf


"""
Fetching the DHCP is enabled or not from the current Host

"""
def check_nic_conf_file(calling_nic):
    path_config = "/etc/sysconfig/network-scripts/" + "ifcfg-" + calling_nic
    conf_file = open(path_config,'r')
    config = conf_file.read()
    #print config
    return_value = config.rfind('BOOTPROTO=dhcp')
    if return_value != -1:
        return 'Dhcp enabled'

    else:
        return 'Dhcp disabled'

"""
Fetching the Host Name

"""
def get_hostname():
    return socket.gethostname()         


"""
Fetching the time-stamp 
"""
def get_dt():
    a = datetime.datetime.now()
    return str(a)


"""
Fetching the Transmitted-bytes and Recived-bytes from the Nics card 
"""
     
def nics_report():

    dict_nics_info = {}

    outer_nic_list_with_conf = nics_with_config()
    outer_nic_list_with_conf.remove('lo')
    for new_nic in outer_nic_list_with_conf:
        #new_correct_nic = new_nic.replace(':',"")
        #print new_correct_nic
        new_correct_nic = new_nic
        check_nic_conf_file(new_correct_nic)
        cmd = 'ifconfig ' + new_correct_nic

        output_ifconfig = subprocess.check_output(cmd,shell=True)

        output_ifconfig_list = output_ifconfig.split('\n\n')

        mac_rx_tx = []
        dhcp_stat_dict = {}
        ht_name_dict = {}
        time_date = {}

        for output_line in output_ifconfig_list:
            nic_line_list = output_line.splitlines()
            for line in nic_line_list:
                if 'inet' in line and ('netmask' in line):
                    dict_inet_nmsk_broadcast = {}
                    list_inet_line = line.split()
                    dict_inet_nmsk_broadcast[list_inet_line[0]] = str(list_inet_line[1])
                    dict_inet_nmsk_broadcast[list_inet_line[2]] = str(list_inet_line[3])
                if 'inet' in line and ('netmask' in line) and  ('broadcast' in line):
                    dict_inet_nmsk_broadcast[list_inet_line[4]] = str(list_inet_line[5])
                    mac_rx_tx.append(dict_inet_nmsk_broadcast)
                if 'ether' in line:
                    dict_ether_mac = {}
                    ether_mac_line = line.split()
                    #print ether_mac_line
                    #dict_ether_mac[ether_mac_line[0]] = str(ether_mac_line[1])
                    dict_ether_mac['MAC Address'] = str(ether_mac_line[1])
                    mac_rx_tx.append(dict_ether_mac)
                if 'RX' in line and ('packets' in line):
                    rx_bytes = {}
                    rx_bytes_line = line.split()
                    rx_bytes['Recevied Bytes'] = str(rx_bytes_line[4]) + ' ' + 'bytes'
                    mac_rx_tx.append(rx_bytes)
                if 'TX' in line and ('packets' in line):
                    tx_bytes = {}
                    tx_bytes_line = line.split()
                    tx_bytes['Transmitted Bytes'] = tx_bytes_line[4] + ' ' + 'bytes'
                    mac_rx_tx.append(tx_bytes)
        dhcp_stat_dict['DHCP status'] = check_nic_conf_file(new_nic)
        mac_rx_tx.append(dhcp_stat_dict)
        ht_name_dict['Hostname'] = get_hostname()
        mac_rx_tx.append(ht_name_dict)
        dict_nics_info[new_correct_nic] = mac_rx_tx
        time_date['Reported Time&Date'] = get_dt()
        mac_rx_tx.append(time_date)
    return dict_nics_info
all_values = nics_report()

if __name__ == "__main__":
    od_all = collections.OrderedDict(sorted(all_values.items()))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_network_shared_location = json.loads(open("/mnt/Backups/Ensight/configurations/config.json").read())["NetworkUsageDataNetworkShareRootPath"]
    filename = os.path.expanduser(path_network_shared_location) + name_of_host.strip() + log_file_name_text + timestamp + '.json'
    file_handler = open(filename,'a+') 
    text_json = json.dumps(od_all, indent=4)
    print >> file_handler,text_json
    file_handler.close()


