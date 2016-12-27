import inventory_functions
import network_usage
from pprint import pprint
import json
import os
import socket
import collections
import time

log_file_name_text = '_inventory_'



"""
Fetch the Host name of the current Host
"""
def get_host_name():
    name_host = socket.gethostname().split('.')[0]
    return name_host
name_host = get_host_name()




if __name__ == "__main__":

    inventory_list = ['DNSHostName','Disks','HostName','DomainName','ReportDateTime','DiskTotalSize','Manufacturer','Model','NumberOfLogicalProcessors','NumberOfProcessors','Softwares','OperatingSystem','NICs']
    inventory_list.sort()
    value_set = {}
    return_dict_all_values = {}
    value_set['DNSHostName'] = inventory_functions.get_dns()
    value_set['HostName'] = inventory_functions.get_host_name()
    value_set['Disks'] = inventory_functions.get_disks_info()
    value_set['Softwares'] = inventory_functions.get_softwares_info()
    value_set['ReportDateTime'] = inventory_functions.get_tm()
    value_set['DomainName'] = inventory_functions.get_dom()
    value_set['Manufacturer'] = inventory_functions.get_mani()
    value_set['DiskTotalSize'] = inventory_functions.get_size()
    value_set['Model'] = inventory_functions.get_mod()
    value_set['NumberOfLogicalProcessors'] = inventory_functions.get_proc1()
    value_set['NumberOfProcessors'] = inventory_functions.get_proc2()
    value_set['DomaintName'] = inventory_functions.get_dom()
    value_set['OperatingSystem'] = inventory_functions.get_os()
    value_set['NICs'] = network_usage.nics_report()


for value in inventory_list:
    Disks = inventory_functions.get_disks_info()
    return_dict_all_values[value] = value_set[value]

if __name__ == "__main__":
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_network_shared_location = json.loads(open("/mnt/Backups/Ensight/configurations/serveragentconfig.json").read())["InventoryDataNetworkShareRootPath"]
    filename = os.path.expanduser(path_network_shared_location) + name_host.strip() + log_file_name_text + timestamp + '.json'
    od_all = collections.OrderedDict(sorted(return_dict_all_values.items()))
    file_handler = open(filename,'a+') 
    text_json = json.dumps(od_all, indent=4)
    print >> file_handler,text_json
    file_handler.close()