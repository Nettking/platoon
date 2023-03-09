import socket
import struct
import netifaces

def get_broadcast_ip_address():
    # Get the IP address and netmask of the default network interface
    default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip_address = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['addr']
    netmask = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['netmask']
    
    # Convert the netmask to an integer
    netmask_int = struct.unpack('>I', socket.inet_aton(netmask))[0]
    
    # Calculate the broadcast IP address
    broadcast_int = (netmask_int ^ 0xffffffff) | struct.unpack('>I', socket.inet_aton(ip_address))[0]
    broadcast_ip_address = socket.inet_ntoa(struct.pack('>I', broadcast_int))
    
    return broadcast_ip_address



if __name__ == '__main__':
    print(get_broadcast_ip_address())