# Variables globales pour l'adresse IP et l'adresse MAC
server_ip_address = '192.168.0.250'
server_mac_address = '00:11:22:33:44:55'

def set_server_ip(ip):
    global server_ip_address
    server_ip_address = ip

def set_server_mac(mac):
    global server_mac_address
    server_mac_address = mac
