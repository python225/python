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
from pprint import pprint


"""
Fetch the disk_information of the current Host
"""

def kb_to_gb(val_in_kb):
    val_in_gb = round((float(val_in_kb) / float(1024*1024*1024)),2)
    return str(val_in_gb) + 'GB'

def get_disks_info():
  partions = psutil.disk_partitions()
  dev_to_mnt_point_dict = {}
  dev_to_disk_space = {}
  devices = []
  mount_points = []
  output = {}
  for partion in partions:
      dev_to_mnt_point_dict[partion.device] = partion.mountpoint
  for dev, mnt_point in dev_to_mnt_point_dict.iteritems():
      usage = psutil.disk_usage(mnt_point)
      total_disk = usage.total
      usage_percent = usage.percent
      mnt_point_dict = {}
      disk_dict = {}
      used_per_dict = {}
      mnt_point_dict['mount_point'] = mnt_point  
      disk_dict['Total_disk'] = kb_to_gb(total_disk)
      used_per_dict['Percent_used'] = usage_percent
      disk_stats = [mnt_point_dict,disk_dict,used_per_dict]
      dev_to_disk_space['DeviceID: '+dev] = disk_stats
  return dev_to_disk_space


"""
Fetch the DNS name of the current Host
"""
def get_dns():
    name_dns = socket.gethostname()
    return name_dns


"""
Fetch the Host name of the current Host
"""
def get_host_name():
    name_host = socket.gethostname().split('.')[0]
    return name_host


"""
Fetch the Domain name of the current Host
"""
def get_dom():
    name_domain = socket.gethostname().split('.')[1]
    return name_domain


"""
Fetch the Manufacture details of the current Host
"""
def get_mani():
    manuf = subprocess.check_output("dmidecode | grep Manufacturer | sed -n '1p'| awk '{print$2,$3}'", shell=True)
    return manuf


"""
Fetching UUID of the current Host
"""
def get_mod():
    model = subprocess.check_output("dmidecode | grep UUID",shell=True)
    return model


"""
Fetching the number of logical processors of the current host
"""
def get_proc1():
    totl = psutil.cpu_count()
    return totl


"""
 Fetching getting the Number of processers in the current Host
"""
def get_proc2():
    physical = psutil.cpu_count(logical=False)
    return physical


"""
Fetching the operating system description of the current Host
"""
def get_des():
    dis = platform.platform()
    return dis


"""
Fetching the productname of the current Host
"""
def get_pro():
    a = subprocess.check_output("dmidecode | grep Product | head -1 | awk '{print$3}'", shell=True)
    return a


"""
Fetching the Vendor of the current Host
"""
def get_vend():
    b = subprocess.check_output("dmidecode | grep Vendor", shell=True)
    return b


"""
Fetching the Version of the current Host
"""
def get_ver():
    c = subprocess.check_output("dmidecode | grep Version | sed -n '2p'", shell=True)
    return c


"""
Fetching the processor of the current Host
"""
def get_pr():
    d = platform.processor()
    return d


"""
Fetching the description of the current Host
"""
def get_desc_nic():
    a = subprocess.check_output("lshw -class network | grep description| awk '{print$2,$3}'", shell=True)
    return a


"""
Fetching the system os details of the current Host
"""
def get_os():
    Description = platform.platform()
    Machine = platform.machine()
    Processor = platform.processor()
    SystemOS = platform.system()
    Release = platform.release()
    Version = platform.version()
    x = platform.linux_distribution()
    y = x[0]
    full = [{'Description':Description, 'ProductName':y, 'Machine':Machine, 'Processor':Processor, 'System OS':SystemOS, 'Release':Release}]
    return full


"""
Fetching the  getting name of the network
"""
def get_name():
    a = subprocess.check_output("lshw -class network | grep name| awk '{print$3}'", shell=True)
    return a


"""
Fetch the ip address of the Host
"""
def get_ip_address():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ip = s.getsockname()[0]
    return ip
    ip_Address = get_ip_address()


"""
Fetching the Mac address of the Host
"""
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


"""
Fetching the dhcp-server ipaddress of the vm
"""
def get_dhc():
    aa = subprocess.check_output("cat /var/lib/dhclient/dhclient.leases | grep server-identifier | awk '{print$3}'", shell=True)
    return aa

"""
Fetching the netmask from nics of the Host
"""
def get_netmask(ifname):
  
    addrs = netifaces.ifaddresses(ifname)
    ipinfo = addrs[socket.AF_INET][0]
    netmask = ipinfo['netmask']
    return netmask


"""
Fetching the FQDN of the current Host
"""
def get_fqdn():
    fqdn = socket.gethostname()
    return fqdn


"""
Fetching the Softwares installed on the current Host
"""
def get_softwares_info():
  cmd = "yum list installed | sed -e '1,/Installed/d'"
  list_of_sw = subprocess.check_output(cmd,shell=True)
  software_to_version = {}
  software_to_vendor = {}
  software_to_description = {}
  software_to_version_vendor = {}
  softwares = []
  return_software_list = []
  for i in list_of_sw.split('\n'):
      tmp_list = i.split()
      if len(tmp_list) == 3:
          softwares.append(tmp_list[0])
          software_to_vendor[tmp_list[0]] = tmp_list[2]
          software_to_version[tmp_list[0]] = tmp_list[1]
  for software in softwares:
      version_vendor_list = []
      software_details_dict = {}
      software_details_dict['ProductName:'] = software
      software_details_dict['Version:'] = software_to_version[software]
      software_details_dict['Vendor'] = software_to_vendor[software]
      return_software_list.append(software_details_dict)
  return return_software_list


"""
Fetching the current Time stamp 
"""
def get_tm():
    a = datetime.datetime.now()
    return str(a)
    

"""
Fetching the family-type of the system
"""
def get_fami():
    a = subprocess.check_output("dmidecode | grep Family", shell=True)
    return a


"""
Fetching the total disk size on that vm
"""
def get_size():
    a = subprocess.check_output("fdisk -l | grep Disk | grep /dev/sd | awk '{print$3}'", shell=True)
    return a