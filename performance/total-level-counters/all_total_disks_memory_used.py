import subprocess
import datetime
import json
import socket
import fcntl
import struct
import psutil
import time
import datetime
import collections
import os

counter_value = json.loads(open("/mnt/Backups/Ensight/configurations/serveragentconfig.json").read())["PerformanceDataCollectionTimeInterval"]

log_file_name_text = '_avg_total_disk_used_'

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
time_stamp_value = get_tm()


"""
Fetching the IPAddress of the current Host
"""
def get_ip_address():
    s = ipaddress_value = subprocess.check_output("ifconfig eth0 | grep inet | awk '{print$2}'| sed -n '1 p'", shell=True)
    return s
ip_value = get_ip_address()



def get_mount_and_device():
    mount_and_device = {}
    for disk_obj in psutil.disk_partitions():
        mount_and_device[disk_obj.mountpoint] = disk_obj.device
    return mount_and_device


def get_readbytes_with_timestamp():
    ts_return_list = []
    ts_a = psutil.disk_usage('/')
    ts_b = ts_a.used
    ts_d = (ts_b/(1024*1024))
    ts_time_stamp = time.time()
    ts_st = datetime.datetime.fromtimestamp(ts_time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    ts_return_list.append(ts_st)
    ts_return_list.append(ts_d)
    return ts_return_list


def get_readbytes():  
    a = psutil.disk_usage('/')
    b = a.used
    d = (b/(1024*1024)) 
    return d

disk_stats = []

disk_stats_with_timestamp = []

for i in range(1,6):
    time.sleep(counter_value)
    disk_stats.append(get_readbytes())
    disk_stats_with_timestamp.append(get_readbytes_with_timestamp())

"""
Finding the values from the list
"""
avg_value = (sum(disk_stats) / float(len(disk_stats)))
max_value = max(disk_stats)
min_value = min(disk_stats)
RecordCount = len(disk_stats)
countercategory = "Mounted Disks"
instancename = "mount point"
counterlabel = "avg_total_megabytes_used"
countername= "Avg_Total_MegaBytes_Used"
total_time = counter_value * 4


if __name__ == "__main__":
    all_values = {'Duration: ':total_time,'PerformanceCounterCategory: ':countercategory,'PerformanceCounterInstanceName: ':instancename,'PerformanceCounterLabel: ':counterlabel,'PerformanceCounterName: ':countername,'AverageValue: ':avg_value,'MaxValue: ':max_value,'MinValue: ':min_value,'RecordCount: ':RecordCount,'HostName: ':name_host,'ReportDateTime: ':time_stamp_value,'IPAddress: ':ip_value}
    od_all = collections.OrderedDict(sorted(all_values.items()))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_network_shared_location = json.loads(open("/mnt/Backups/Ensight/configurations/serveragentconfig.json").read())["PerformanceDataNetworkShareRootPath"]
    filename = os.path.expanduser(path_network_shared_location) + name_host.strip() + log_file_name_text + timestamp + '.json'
    file_handler = open(filename,'a+') 
    text_json = json.dumps(od_all, indent=4)
    print >> file_handler,text_json
    value = {'Values':disk_stats_with_timestamp} 
    values_variable = json.dumps(value,indent=4)
    print >> file_handler,values_variable
    file_handler.close()
