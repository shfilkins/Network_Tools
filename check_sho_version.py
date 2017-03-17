from regex_parser import search_file

def obtain_uptime():
    uptime = search_file('uptime is (.+$)', 'show_version.txt')
    if uptime:
        return uptime[0]
    else:
        return None

#make this output more descriptive, combine with vendor and device type
def obtain_model():
    device_model = search_file('^Cisco (\d+) ', 'show_version.txt')
    if device_model:
        return device_model[0]
    else:
        return None
        
def obtain_os_version():
    device_version = search_file('^Cisco IOS Software, .+ (Version .+),', 'show_version.txt')
    if device_version:
        return device_version[0]
    else:
        return None

#need device name, need ios file for later comparison, need to put these in a dictionary for later pprint    
def get_device_name():
    pass
    
print obtain_model()
print obtain_uptime()
print obtain_os_version()