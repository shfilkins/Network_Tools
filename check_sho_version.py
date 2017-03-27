import paramiko
import telnetlib
import time
import cPickle as pickle
#this should make the pickle operations faster.
import re

#This script can use telnet or SSH to log in to a network device.  The choice is presented to the user.
#The script will also request a username and password from the user.  The username is a local one on my GNS3 lab routers.
#The IP addresses of the routers are stored in 'ip_addresses.txt' in the local directory.
#Then the user is prompted for an IP address or the location of a file containing them.
#The script logs into the device(s) and runs 'show version'.  It then processes this command and puts
#the device_model, device_type, vendor, os_version, serial_number, confreg and uptime into a dictionary.
#the dictionary will be keyed by device hostname.  It will also contain the device IP address.  
#the dictionary will be stored with pickle for later retrieval.

def get_device_ip():
    fhand = open('ip_addresses.txt')    #a .txt file containing the IP addresses of the routers.
    ip = list()
    for line in fhand:
        ip.append(line.strip())
    fhand.close()
    return ip
def telnet_or_ssh():
    via = raw_input('Connect via Telnet(t) or SSH(s)?')   #the choice is yours.
    return via

def paramiko_connex(ip, username, password):
    remote_connex_pre = paramiko.SSHClient()   #set remote_connex_pre to an instance of the paramiko client.
    remote_connex_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #lab example, skips missing SSH host key.
    remote_connex_pre.connect(ip, username=username, password=password,look_for_keys=False, allow_agent=False)
    #connects to the device using the ip address, and the collected username and password.
    remote_conn = remote_connex_pre.invoke_shell()
    #can use the invoke_shell method to pass multiple commands.
    remote_conn.send('\n')
    remote_conn.send('terminal length 0\n')    #this helps you collect all the output of your command, instead of paging the output.
    time.sleep(1)
    remote_conn.send('sh version \n')   #this is from the login prompt, to get to enable prompt is more difficult.
    time.sleep(1)
    output = remote_conn.recv(65535)
    remote_connex_pre.close()
    return output       #this is the full output of the show version command.
    
def telnetlib_connex(ip, username, password):
    TELNET_PORT = 23    #specifies the port to telnet, could you use this to try other ports???
    TELNET_TIMEOUT = 6  #this makes it timeout quicker than normal.
    READ_TIMEOUT = 6
    remote_conn = telnetlib.Telnet(ip, TELNET_PORT, TELNET_TIMEOUT)
    
    output = remote_conn.read_until('sername:', READ_TIMEOUT)
    #keep looking in the output until you see username or get to the timeout value.
    #you don't know if Username or username, so just look for 'sername'.
    remote_conn.write(username + '\n')   #send the username.
    time.sleep(1)
    output = remote_conn.read_until('ssword:', READ_TIMEOUT)
    remote_conn.write(password + '\n')       #send the password in cleartext!
    time.sleep(1)

    remote_conn.write ('terminal length 0\n')
    time.sleep(1)
    
    remote_conn.write('show version \n')   #run the command.
    time.sleep(1)
    
    output = remote_conn.read_very_eager()
    #read as much data as it can until it starts blocking.
    remote_conn.close()
    return output
    
def get_device_name(output):
    pattern = re.search(r'(.+?)(>|#)', output)  #search for anything preceding the login prompt.
    device_name = pattern.group(1)
    return device_name
    
def get_device_vendor(output):
    pattern = re.search(r'(.+) IOS Software', output)  #Cisco precedes IOS software in the output of the command.
    vendor = pattern.group(1)
    return vendor
    
def get_device_type(output):
    pattern = re.search(r'Serial interfaces', output) #If it has serial interfaces, it's a router.
    if pattern:
        return 'Router'
    else:
        return 'Switch'
def get_device_serial(output):
    pattern = re.search(r'Processor board ID (.+)\r', output)   #gets the serial number from the processor board.
    serial = pattern.group(1)
    return serial
def get_device_confreg(output):
    pattern = re.search(r'Configuration register is (.+)\r', output)   #gets the confreg.
    confreg = pattern.group(1)
    return confreg
def get_device_passwd():
    username = raw_input('\nUsername:')
    password = raw_input('\nPassword:')
    return username, password
    
def get_device_uptime(output):
    pattern = re.search(r' uptime is (.+)\r', output)
    uptime = pattern.group(1)
    return uptime
   
def get_device_model(output):
    pattern = re.search(r'Cisco (\d+) ', output)    #looks for digits following Cisco.  This is the device model.
    model = pattern.group(1)
    return model
        
def get_os_version(output):
    pattern = re.search(r'Cisco IOS Software, .+ \((.+, .+),', output)  #gets the version.
    version = pattern.group(1)
    return version
    
if __name__ == "__main__":
    network_dict = dict()
    ip_addr = get_device_ip()   #returns a list of IP addresses
    username, password = get_device_passwd()
    via = telnet_or_ssh()
    for ip in ip_addr:   #iterates over a list of IP addresses
        if via == 't':   #user selects 't' or 's' for either a telnet or SSH connection.
            output = telnetlib_connex(ip, username, password)
        elif via == 's':
            output = paramiko_connex(ip, username, password)
        
        name = get_device_name(output)
        uptime = get_device_uptime(output)
        vendor = get_device_vendor(output)
        model = get_device_model(output)
        device_type = get_device_type(output)
        serial_num = get_device_serial(output)
        os_version = get_os_version(output)
        confreg = get_device_confreg(output)
        
        network_dict[name] = {'IP': ip, 'vendor': vendor, 'model': model, 'device_type': device_type, 'uptime': uptime, 'serial': serial_num, 'os': os_version, 'confreg': confreg}
        #everything gets put in the dictionary using the device name with it's associated IP address.
        #there are two devices in the dictionary, but there could be more.
    fhandle = open('tmp.pkl', 'wb')
    #open the pickle file for writing.
    pickle.dump(network_dict, fhandle)
    #put the dictionary in for later.
    fhandle.close()

    
    