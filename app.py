from pysnmp.hlapi.v3arch.asyncio import *
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from wakeonlan import send_magic_packet
import threading
import asyncio


# Adresse MAC du serveur pour envoyer le paquet Wake-on-LAN
SERVER_MAC_ADDRESS = 'D0:50:99:D3:47:F7'

# Fonction pour créer une icône de couleur
def create_image(color):
    image = Image.new('RGB', (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 63, 63), outline="black", fill=color)
    return image

# Fonction pour vérifier l'état du serveur via SNMP
async def check_snmp_status():
    transport_target = await UdpTransportTarget.create(('192.168.0.250', 161))

    error_indication, error_status, error_index, var_binds = await getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),  # SNMP v1, changez si nécessaire
        transport_target,
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))  # OID pour sysUptime
    )

    if error_indication:
        print(f"Error indication: {error_indication}")
        return None  # Retourne None en cas d'erreur
    elif error_status:
        print(f"Error status: {error_status.prettyPrint()}")
        return None  # Retourne None en cas d'erreur
    else:
        # Extraction de l'uptime
        uptime_ticks = var_binds[0][1]  # La valeur est le deuxième élément du tuple
        return uptime_ticks  # Retourne les ticks d'uptime

# Fonction pour envoyer une requête Wake-on-LAN
def wake_on_lan(icon, item):
    send_magic_packet(SERVER_MAC_ADDRESS)
    print(f"Sent Wake-on-LAN packet to {SERVER_MAC_ADDRESS}")

# Fonction de mise à jour de l'icône dans la barre des tâches
async def update_icon(icon):
    while True:
        uptime = await check_snmp_status()
        if uptime is not None:
            print(f"uptime {uptime}")
            # Convertir les ticks en secondes
            uptime_seconds = uptime // 10  # Chaque tick est 10 ms
            uptime_display = f'Uptime: {uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m'
            icon.icon = create_image('green')
            icon.title = uptime_display  # Met à jour le tooltip avec l'uptime
            icon.menu = Menu(MenuItem('Quitter', quit_app))  # Menu par défaut quand le serveur est en ligne
        else:
            icon.icon = create_image('red')
            icon.title = "Server Offline"  # Message d'erreur si le serveur est hors ligne
            icon.menu = Menu(
                MenuItem('Allumer', wake_on_lan),
                Menu.SEPARATOR,
                MenuItem('Quitter', quit_app)
            )

        await asyncio.sleep(10)  # Vérifier toutes les 10 secondes

# Fonction pour quitter l'application
def quit_app(icon, item):
    icon.stop()

# Fonction de démarrage de l'icône
def setup(icon):
    icon.visible = True
    # Démarrage de la tâche asynchrone dans un thread séparé
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_until_complete, args=(update_icon(icon),)).start()

# Créer l'icône rouge par défaut
icon = Icon("SNMP Status", create_image('red'))

# Démarrage de l'icône dans la barre des tâches
icon.run(setup)
