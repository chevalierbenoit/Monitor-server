import configparser
import os

# Chemin du fichier de configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
# Variables globales pour l'adresse IP et l'adresse MAC
server_ip_address = None
server_mac_address = None

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if 'Server' in config:
        server_ip = config['Server']['ip_address']
        server_mac = config['Server']['mac_address']
        return server_ip, server_mac
    else:
        write_config('192.168.0.1', '00:00:00:00:00:00')
        return '192.168.0.1', '00:00:00:00:00:00'

def write_config(ip_address, mac_address):
    config = configparser.ConfigParser()
    config['Server'] = {
        'ip_address': ip_address,
        'mac_address': mac_address
    }

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_server_ip():
    global server_ip_address
    global server_mac_address
    if server_ip_address is None:
        server_ip_address, server_mac_address = read_config()
    return server_ip_address

def get_server_mac():
    global server_ip_address
    global server_mac_address
    if server_mac_address is None:
        server_ip_address, server_mac_address = read_config()
    return server_mac_address

def set_server_ip(ip):
    global server_ip_address
    global server_mac_address
    server_ip_address = ip
    write_config(server_ip_address, server_mac_address)

def set_server_mac(mac):
    global server_ip_address
    global server_mac_address
    server_mac_address = mac
    write_config(server_ip_address, server_mac_address)