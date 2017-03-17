#the function takes a regex and a filename to use for the search.
#it reads the file line by line, searching for the pattern.
#if it finds the pattern, ie. if the pattern is True, it grabs
#what the pattern captures in '()' parentheses.
#it appends the searched for captured items into a list which 
#will be returned to the calling program.

def search_file(regex, file):
    import re
    tmp_lst = list()
    fhand = open(file)
    for line in fhand:
        pattern = re.search(regex, line)
        if pattern:
            searched_for = pattern.group(1)
            tmp_lst.append(searched_for)
    fhand.close()
    return tmp_lst
    
#Example of how to use:
#if you have a file from a router it will always have '#' or '>' 
#after the device name, eg "cr1.123456#sh ip ospf interface"
#So to capture the device name you could do this:
#device_name = generic_regex_parser('(.+?)(>|#)', 'ospf_data.txt')
#then just run this multiple times to build a list of device names.
#then just access by index from the list.