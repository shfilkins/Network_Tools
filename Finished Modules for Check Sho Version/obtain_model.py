def obtain_model():
    from regex_parser import search_file
    
    device_model = search_file('^Cisco (\d+) ', 'show_version.txt')
    
    if device_model:
        return device_model[0]
    else:
        return None
        
