#   Copyright (c) 2019 Grzegorz Raczek
#   https://github.com/grzracz
#   Files available under MIT license

import sys  # (sys.argv)
import socket   # (socket.gethostbyname())
import subprocess   # for using ipconfig (subnet mask) and ping


# tries to find ip from domain
def viable_ip(domain_name):
    viable = False
    try:
        socket.gethostbyname(domain_name)
        viable = True
    finally:
        return viable


# converts ip address to decimal integer
def ip_to_int(ip):
    ip = ip_dec_to_bin(ip)
    result = 0
    power = 31
    for x in range(0, len(ip)):
        if ip[x] == ".":
            continue
        else:
            result += int(ip[x]) * 2 ** power
            power -= 1
    return result


# converts decimal ip to binary ip
def ip_dec_to_bin(ip):
    bin_ip = ""
    i1 = 0
    for x in range(0, 3):
        i2 = ip.find('.', i1)
        substring = ip[i1:i2]
        i1 = i2 + 1
        bin_ip += '{0:08b}'.format(int(substring)) + "."
    bin_ip += '{0:08b}'.format(int(ip[i1:]))
    return bin_ip


# converts binary ip to decimal
def ip_bin_to_dec(ip):
    dec_ip = ""
    i1 = 0
    for x in range(1, 4):
        i2 = ip.find('.', i1)
        substring = ip[i1:i2]
        i1 = i2 + 1
        num = 0
        for y in range(0, 8):
            num += int(substring[y]) * 2**(7 - y)
        dec_ip += str(num) + '.'
    num = 0
    substring = ip[i1:]
    for y in range(0, 8):
        num += int(substring[y]) * 2**(7 - y)
    dec_ip += str(num)
    return dec_ip


# performs logical and on two ip addresses
def logical_and(ip1, ip2):
    ip1 = ip_dec_to_bin(ip1)
    ip2 = ip_dec_to_bin(ip2)
    if len(ip1) != len(ip2):
        sys.stderr.write("INPUT ERROR: Incorrect usage of logical_and function")
        return 0
    result = ""
    for x in range(0, len(ip1)):
        if ip1[x] == '.':
            result += '.'
        else:
            if ip1[x] == '1' and ip2[x] == '1':
                result += '1'
            else:
                result += '0'
    return ip_bin_to_dec(result)


# performs logical or on two ip addresses
def logical_or(ip1, ip2):
    ip1 = ip_dec_to_bin(ip1)
    ip2 = ip_dec_to_bin(ip2)
    if len(ip1) != len(ip2):
        sys.stderr.write("INPUT ERROR: Incorrect usage of logical_or function")
        return 0
    result = ""
    for x in range(0, len(ip1)):
        if ip1[x] == '.':
            result += '.'
        else:
            if ip1[x] == '0' and ip2[x] == '0':
                result += '0'
            else:
                result += '1'
    return ip_bin_to_dec(result)


# performs logical not on an ip address
def logical_not(ip):
    ip = ip_dec_to_bin(ip)
    result = ""
    for x in range(0, len(ip)):
        if ip[x] == '.':
            result += '.'
        else:
            if ip[x] == '0':
                result += '1'
            else:
                result += '0'
    return ip_bin_to_dec(result)


# converts cidr to ip address
def cidr_to_ip(cidr):
    if type(cidr) == str:
        cidr = cidr.replace('/', '')
        cidr = int(cidr)
    result = ""
    for x in range(1, 33):
        if x > 1 and (x - 1) % 8 == 0:
            result += "."
        if cidr > 0:
            result += '1'
            cidr -= 1
        else:
            result += '0'
            cidr -= 1
    return ip_bin_to_dec(result)


# converts mask to CIDR and combines with ip
def get_address_from_system():
    return get_ip_from_system() + "/" + str(ip_dec_to_bin(get_mask_from_system()).count('1'))   # ip/cidr


# gets subnet mask from system
def get_mask_from_system():
    ip = socket.gethostbyname((socket.gethostname()))
    proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if str(ip).encode() in line:
            break
    mask = str(proc.stdout.readline()).rstrip().split(":")[-1].replace(' ', '')  # extracting subnet mask
    return mask[:-5]    # removing \r and \n


# gets ip from system
def get_ip_from_system():
    return socket.gethostbyname((socket.gethostname()))


# checks if ip is correct
def correct_ip_address(ip):
    # Only numbers and dot/slash?
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '/']
    for i in ip:
        if i not in characters:
            return False

    # 4 modules?
    if ip.count('.') != 3:
        return False
    for x in range(1, len(ip)):
        if ip[x] == '.' and ip[x-1] == '.':
            return False

    # All modules in range 0-255?
    i1 = 0
    for x in range(0, 4):
        i2 = ip.find('.', i1)
        if i2 == -1:
            i2 = ip.find('/', i1)
        substring = ip[i1:i2]
        i1 = i2 + 1

        if substring == '':
            return False
        if int(substring) < 0 or int(substring) > 255:
            return False

    # Subnet mask in range 0-32?
    if ip.find('/') < 0:
        return False
    substring = ip[ip.find('/') + 1:]
    if substring == '':
        return False
    if int(substring) < 0 or int(substring) > 32:
        return False

    return True     # if nothing returned false before


# returns network address
def network_address(address):
    return logical_and(address[:address.find('/')], cidr_to_ip(address[address.find('/'):]))    # logical_and(ip, mask)


# returns network class based on its first octave
def network_class(ip):
    lead = ip[:ip.find('.')]
    if int(lead) < 128:
        return "A (very big)"
    elif int(lead) < 192:
        return "B (medium size)"
    elif int(lead) < 224:
        return "C (small)"
    elif int(lead) < 240:
        return "D (for group transmission)"
    else:
        return "E (reserved for IETF)"


# returns if address is public or private
def is_private(address):
    ip = address[:address.find('/')]
    if ip[:ip.find('.')] == "10":
        return True
    elif ip[:ip.find('.')] == "172":
        octave2 = ip[ip.find('.') + 1: ip.find('.', ip.find('.') + 1)]
        if 16 <= int(octave2) <= 31:
            return True
    elif ip[:ip.find('.', ip.find('.') + 1)] == "192.168":
        return True
    else:
        return False


# returns network mask from address
def network_mask(address):
    return cidr_to_ip(address[address.find('/'):])


# returns network broadcast address
def network_broadcast_address(address):
    return logical_or(network_address(address), logical_not(network_mask(address)))


# returns first host address
def first_host_address(address):
    ip = network_address(address)
    first_host = ip[:ip.rfind('.') + 1] + str(int(ip[ip.rfind('.') + 1:]) + 1)  # get last octave and increment
    return first_host


# returns last host address
def last_host_address(address):
    ip = network_broadcast_address(address)
    last_host = ip[:ip.rfind('.') + 1] + str(int(ip[ip.rfind('.') + 1:]) - 1)  # get last octave and decrement
    return last_host


# returns max number of hosts
def max_host_number(address):
    return ip_to_int(logical_and(network_broadcast_address(address), logical_not(network_mask(address)))) - 1


# pings ip address and prints/saves output
def ping(ip, file_name):
    ping_process = subprocess.Popen(["ping", "-n", "5", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = ping_process.stdout.readline()
        file_name.write(line[:-1].decode())
        print(line[:-2].decode())
        if line == b'':
            break


# main
if len(sys.argv) == 1:
    print("No parameters given, using current computer address...")
    _address = get_address_from_system()
elif len(sys.argv) == 2:
    _address = sys.argv[1]
else:
    _address = sys.argv[1]
    sys.stderr.write("INPUT ERROR: Too many parameters, using the first one...\n")

if not correct_ip_address(_address):
    sys.stderr.write("INPUT ERROR: Incorrect address, using current computer address...\n")
    _address = get_address_from_system()
    if not correct_ip_address(_address):
        sys.exit("FATAL ERROR: Unable to get current computer address, quitting...")
else:
    print("IP Address and Subnet Mask are correct.")

print("\nIP Address:", _address[:_address.find('/')] + ", binary:", ip_dec_to_bin(_address[:_address.find('/')]))
print("Subnet Mask (CIDR):", _address[_address.find('/'):])

print("Data:")
network_address_value = network_address(_address)
print("Network address:", network_address_value + ", binary:", ip_dec_to_bin(network_address_value))
print("Network class:", network_class(_address))
print("Network type:", "private" if is_private(_address) else "public")
network_mask_value = network_mask(_address)
print("Subnet Mask:", network_mask_value + ", binary:", ip_dec_to_bin(network_mask_value))
network_broadcast_address_value = network_broadcast_address(_address)
print("Broadcast address:", network_broadcast_address_value + ", binary:",
      ip_dec_to_bin(network_broadcast_address_value))
first_host_address_value = first_host_address(_address)
print("First host address:", first_host_address_value + ", binary:", ip_dec_to_bin(first_host_address_value))
last_host_address_value = last_host_address(_address)
print("Last host address:", last_host_address_value + ", binary:", ip_dec_to_bin(last_host_address_value))
max_host_number_value = max_host_number(_address)
print("Max number of hosts:", max_host_number_value)

name = _address[:_address.find('/')] + "-" + _address[_address.find('/') + 1:] + "-info.txt"
file = open(name, 'w+')
print("\nSaving values to a text file (" + name + ")...")

file.write("IP Address: " + _address[:_address.find('/')] + " (" + ip_dec_to_bin(_address[:_address.find('/')]) + ")\n")
file.write("Subnet Mask (CIDR): " + _address[_address.find('/'):] + "\n\n")

file.write("Network address: " + network_address_value + " (" + ip_dec_to_bin(network_address_value) + ")\n")
file.write("Network class: " + network_class(_address) + '\n')
file.write("Network type: " + ("private" if is_private(_address) else "public") + '\n')
file.write("Subnet Mask: " + network_mask_value + " (" + ip_dec_to_bin(network_mask_value) + ")\n")
file.write("Broadcast address: " + network_broadcast_address_value + " (" +
           ip_dec_to_bin(network_broadcast_address_value) + ")\n")
file.write("First host address: " + first_host_address_value + " (" + ip_dec_to_bin(first_host_address_value) + ")\n")
file.write("Last host address: " + last_host_address_value + " (" + ip_dec_to_bin(last_host_address_value) + ")\n")
file.write("Max number of hosts: " + str(max_host_number_value) + '\n')

ip_addr = _address[:_address.find('/')]
if ip_addr != network_address(_address) and ip_addr != network_broadcast_address(_address):
    if is_private(_address):
        if network_address(_address) != network_address(get_address_from_system()):
            print("This host is in a different private network. Unable to ping.")
        else:
            print("This address is in your local network.")
            user_input = input("Do you want to ping it? Y/N: ")
            if user_input == 'Y' or user_input == 'y':
                ping(ip_addr, file)
    else:
        print("This host is public.")
        user_input = input("Do you want to ping it? Y/N: ")
        if user_input == 'Y' or user_input == 'y':
            ping(ip_addr, file)

for _x in range(1, len(sys.argv)):
    if sys.argv[_x] == ip_addr:
        continue
    if viable_ip(sys.argv[_x]):
        print("Parameter " + sys.argv[_x] + " is a pingable domain.")
        user_input = input("Do you want to ping it? Y/N: ")
        if user_input == 'Y' or user_input == 'y':
            file.write("\nPinging " + sys.argv[_x] + ":")
            ping(socket.gethostbyname(sys.argv[_x]), file)

file.close()
