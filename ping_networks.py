import os
import re
import pprint

#To run this you need to have one file in the directory with the script.  Name the file "network_list".
#The file needs to contain a list of networks with their CIDR notation subnet masks.  eg 10.10.20.0/26.

list_of_networks = open('network_list', 'r')  #open a list of networks.

percentage_out = open('output', 'a')  #this is used to write the results (percentage free, etc) after reading through the ping results file.

ip_address_status = dict()
free_ips = dict()
used_ips = dict()

def sweep_network(number):
    network_sweep = three_octets[0] + '.' + three_octets[1] + '.' + three_octets[2] + '.' + str(number)
    cmd2 = "ping -c 3 " + network_sweep + " >> ping_results"
    os.system(cmd2)

def make_percentage(start, stop, network_block):
    count = 0
    for i in range(start, stop):
        ip_address  = first_three_octets[0] + '.' + first_three_octets[1] + '.' + first_three_octets[2] + '.' + str(i)
        if ip_address_status[ip_address] is "Available":
            count += 1
            free_ips.setdefault(network_ip, []).append(ip_address)
        else:
            used_ips.setdefault(network_ip, []).append(ip_address)
    result = "%s: %.0f%%\n" % (network_ip, 100*float(count)/network_block)
    percentage_out.write(result) 
    
for network in list_of_networks:
    cmd1 = "echo NEXT NETWORK >> ping_results"
    os.system(cmd1)
    device_ip = network.rstrip() #for each network strip off /n
    three_octets = device_ip.split('.')
    #/24
    if "/24" in device_ip:
        for i in range(1, 255):
            sweep_network(i)
    #/25
    elif "0/25" in device_ip:
        for i in range(1, 127):
            sweep_network(i)
            
    elif "128/25" in device_ip:
        for i in range(129, 255):
            sweep_network(i)
            
    #/26
    elif "0/26" in device_ip:
        for i in range(1, 63):
            sweep_network(i)
            
    elif "64/26" in device_ip:
        for i in range(65, 127):
            sweep_network(i)
            
    elif "128/26" in device_ip:
        for i in range(129, 191):
            sweep_network(i)
            
    elif "192/26" in device_ip:
        for i in range(193, 255):
            sweep_network(i)
    #/27
    elif "0/27" in device_ip:
        for i in range(1, 31):
            sweep_network(i)
    elif "32/27" in device_ip:
        for i in range(33, 63):
            sweep_network(i)
    elif "64/27" in device_ip:
        for i in range(65, 95):
            sweep_network(i)        
    elif "96/27" in device_ip:
        for i in range(97, 127):
            sweep_network(i)        
    elif "128/27" in device_ip:
        for i in range(129, 159):
            sweep_network(i)        
    elif "160/27" in device_ip:
        for i in range(161, 191):
            sweep_network(i)
    elif "192/27" in device_ip:
        for i in range(193, 223):
            sweep_network(i)
    elif "224/27" in device_ip:
        for i in range(225, 255):
            sweep_network(i)
    #/28

ping_results = open('ping_results', 'r')  #these are the collected results from your ping test.
  
for line in ping_results:
    if "ping statistics" in line:
        search_pattern = re.search(r'--- (\d+\.\d+\.\d+\.\d+) ping statistics ---', line)
        ip = search_pattern.group(1)
        if ip not in ip_address_status:
            ip_address_status.setdefault(ip, {})

    if "3 received, 0% packet loss" in line:
        ip_address_status[ip] = "Used"
    
    elif "0 received, +3 errors, 100% packet loss" in line:
        ip_address_status[ip] = "Available"
        
    elif "0 received, 100% packet loss" in line:
        ip_address_status[ip] = "Available"

#Rewind the file to the beginning.  
list_of_networks.seek(0)        
for network in list_of_networks:
    network_ip = network.rstrip() #for each device strip off /n
    first_three_octets = network_ip.split('.')
     
    #/24
    if "/24" in network_ip:
        make_percentage(1, 255, 254)
    #/25
    elif "0/25" in network_ip:
        make_percentage(1, 127, 126)
                
    elif "128/25" in network_ip:
        make_percentage(129, 255, 126)
                   
    #/26
    elif "0/26" in network_ip:
        make_percentage(1, 63, 62)
            
    elif "64/26" in network_ip:
        make_percentage(65, 127, 62)
            
    elif "128/26" in network_ip:
        make_percentage(129, 191, 62)
            
    elif "192/26" in network_ip:
        make_percentage(193, 255, 62)
   
   #/27
    elif "0/27" in network_ip:
        make_percentage(1, 31, 30)
  
    elif "32/27" in network_ip:
        make_percentage(33, 63, 30)
    
    elif "64/27" in network_ip:
        make_percentage(65, 95, 30)
            
    elif "96/27" in network_ip:
        make_percentage(97, 127, 30)
 
    elif "128/27" in network_ip:
        make_percentage(129, 159, 30)

    elif "160/27" in network_ip:
        make_percentage(161, 191, 30)
        
    elif "192/27" in network_ip:
        make_percentage(193, 223, 30)

    elif "224/27" in network_ip:
        make_percentage(225, 255, 30)

print "\n" 
percentage_out.write('\n')       
percentage_out.write("Free IP Addresses:\n") 
percentage_out.write(pprint.pformat(free_ips))
percentage_out.write("\nUsed IP Addresses:\n")
percentage_out.write(pprint.pformat(used_ips))        
        
list_of_networks.close()
ping_results.close()
percentage_out.close()
    
    
    
            
            
            
            
            

