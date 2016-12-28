from __future__ import division
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


counter_value = json.loads(open("config.json file location").read())["PerformanceDataCollectionTimeInterval"]

log_file_name_text = '_avg_disk_readbytes_sec_'


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


def get_readbytes_with_timestamp():
    ts_return_list = []
    ts_a = psutil.disk_io_counters()
    ts_b = ts_a.read_bytes
    ts_c = ts_a.read_time
    ts_d = int((ts_b*1000)/ts_c)
    ts_time_stamp = time.time()
    ts_st = datetime.datetime.fromtimestamp(ts_time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    ts_return_list.append(ts_st)
    ts_return_list.append(ts_d)
    return ts_return_list

disk_stats_with_timestamp = []

for i in range(1,6):
    time.sleep(counter_value)
    disk_stats_with_timestamp.append(get_readbytes_with_timestamp())

disk_stats = [disk_stats_with_timestamp[0][1], disk_stats_with_timestamp[1][1],disk_stats_with_timestamp[2][1], disk_stats_with_timestamp[3][1],disk_stats_with_timestamp[4][1]]

"""
Finding the values from the list
"""
avg_value = (sum(disk_stats) / float(len(disk_stats)))
max_value = max(disk_stats)
min_vale = min(disk_stats)
RecordCount = len(disk_stats)
countercategory = "Logical Volume Manager" 
instance_name = "Total"
counter_label = "avg_disk_readbytes_sec"
counter_name = "Avg.Disk Read_Bytes/Sec"
total_time = counter_value * 4

if __name__ == "__main__":
    all_values = {'Duration: ':total_time,'PerformanceCounterCategory: ':countercategory,'PerformanceCounterInstanceName: ':instance_name,'PerformanceCounterLabel: ':counter_label,'PerformanceCounterName: ':counter_name,'AverageValue: ':avg_value,'MaxValue: ':max_value,'MinValue: ':min_vale,'RecordCount: ':RecordCount,'HostName: ':name_host,'ReportDateTime: ':time_stamp_value,'IPAddress: ':ip_value}
    od_all = collections.OrderedDict(sorted(all_values.items()))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_network_shared_location = json.loads(open("config.json file location").read())["PerformanceDataNetworkShareRootPath"]
    filename = os.path.expanduser(path_network_shared_location) + name_host.strip() + log_file_name_text + timestamp + '.json'
    file_handler = open(filename,'a+') 
    text_json = json.dumps(od_all, indent=4)
    print >> file_handler,text_json
    value = {'Values':disk_stats_with_timestamp} 
    values_variable = json.dumps(value,indent=4)
    print >> file_handler,values_variable
    file_handler.close()
