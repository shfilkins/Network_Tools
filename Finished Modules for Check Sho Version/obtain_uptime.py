def obtain_uptime():
    from regex_parser import search_file
    uptime = search_file('uptime is (.+$)', 'show_version.txt')
    return uptime[0]
    if uptime:
        return uptime[0]
    else:
        return None