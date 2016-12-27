#!/usr/bin/python
import pyinotify,subprocess,json
from crontab import CronTab

ABS_PATH_AGENT_CONF_FILE='/mnt/Backups/Ensight/configurations/agentconfig.json'
CONF_MODIFIED=False
#intial_value_list = get_values_list()


def get_values_list():
	config_file = open(ABS_PATH_AGENT_CONF_FILE,'r')
	configurations = json.load(config_file)
	return_dict_values = {}
	for scriptname,time_value in configurations.items():
		return_dict_values[scriptname] = time_value
	return return_dict_values

def get_changed_values_dict():
	current_values_dict = get_values_list()
	return_changed_values_dict = {}
        #tmp_intial_value_list = intial_value_list
	for script_name in current_values_dict.keys():
		if intial_value_list[script_name] != current_values_dict[script_name]:
			return_changed_values_dict[script_name] = current_values_dict[script_name]
        global intial_value_list
	intial_value_list = current_values_dict
	return return_changed_values_dict


def set_cron_job(script_name,set_time_in_min):
        my_user_cron = CronTab(user=True)
        command_var = '/usr/bin/python ' + script_name
        print command_var
        job = my_user_cron.new(command=command_var)
        job.minute.every(set_time_in_min)
        my_user_cron.write()

def onChange(ev):
    #cmd = ['/bin/echo',ABS_PATH_AGENT_CONF_FILE, ev.pathname, 'changed']
    #subprocess.Popen(cmd).communicate()
    #CONF_MODIFIED = True
    print 'changed values are:'
    tmp_dict = get_changed_values_dict()
    for script_name,time_value in tmp_dict.items():
    	tmp_script_name = script_name + '.py'
    	set_cron_job(tmp_script_name,time_value)

		

global intial_value_list
intial_value_list = get_values_list()
    		
if __name__ == '__main__':
	wm = pyinotify.WatchManager()
	wm.add_watch(ABS_PATH_AGENT_CONF_FILE, pyinotify.IN_MODIFY, onChange)
	notifier = pyinotify.Notifier(wm)
	#print "the value of CONF_MODIFIED: " + str(CONF_MODIFIED)
	#global intial_value_list
        #intial_value_list = get_values_list() 
        print intial_value_list
	notifier.loop()
