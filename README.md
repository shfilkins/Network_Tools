# Network_Tools
A collection of tools for network engineering.

Contains:
regex_parser.py containing a function 'search_a_file' which opens a file, then searches for a specified term. The term is captured using a regex .group and returned by the function.

ping_networks.py; pings through a range of networks if you give it a list.  It recognizes CIDR notation so it can ping through
each network without pinging the broadcast IP, for example. 
After storing the results of the pings, it generates a new file from the ping results, telling you percent free from your network(s).
This takes a while to run due to timeouts waiting for free IP addresses which don't respond.
