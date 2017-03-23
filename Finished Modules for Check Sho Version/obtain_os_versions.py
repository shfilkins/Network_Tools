def obtain_os_version():
    from regex_parser import search_file
    
    device_version = search_file('^Cisco IOS Software, .+ (Version .+),', 'show_version.txt')
    
    if device_version:
        return device_version[0]
    else:
        return None
