from pysnmp.hlapi.v3arch.asyncio import *
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from wakeonlan import send_magic_packet
import threading
import asyncio
import tkinter as tk
from tkinter import simpledialog


# Adresse MAC du serveur pour envoyer le paquet Wake-on-LAN
server_mac_address = 'D0:50:99:D3:47:F7'
server_ip_address = '192.168.0.250'
wol_sent = False

# Fonction pour créer une icône de couleur
def create_image(color):
    image = Image.new('RGB', (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 63, 63), outline="black", fill=color)
    return image

# Fonction pour ouvrir la fenêtre de configuration
def open_config(icon, item):
    def save_config():
        global server_ip_address, server_mac_address
        # Récupérer les valeurs des champs de texte
        server_ip_address = ip_entry.get()
        server_mac_address = mac_entry.get()
        print(f"Nouvelle configuration - IP: {server_ip_address}, MAC: {server_mac_address}")
        config_window.destroy()  # Fermer la fenêtre

    def cancel_config():
        config_window.destroy()  # Fermer la fenêtre sans sauvegarder

    # Création de la fenêtre de configuration
    config_window = tk.Tk()
    config_window.title("Configuration du Serveur")

    # Champs pour l'adresse IP
    tk.Label(config_window, text="Adresse IP:").grid(row=0, column=0, padx=10, pady=10)
    ip_entry = tk.Entry(config_window)
    ip_entry.grid(row=0, column=1, padx=10, pady=10)
    ip_entry.insert(0, server_ip_address)

    # Champs pour l'adresse MAC
    tk.Label(config_window, text="Adresse MAC:").grid(row=1, column=0, padx=10, pady=10)
    mac_entry = tk.Entry(config_window)
    mac_entry.grid(row=1, column=1, padx=10, pady=10)
    mac_entry.insert(0, server_mac_address)

    # Bouton "Sauvegarder"
    save_button = tk.Button(config_window, text="Sauvegarder", command=save_config)
    save_button.grid(row=2, column=0, padx=10, pady=10)

    # Bouton "Annuler"
    cancel_button = tk.Button(config_window, text="Annuler", command=cancel_config)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)

    config_window.mainloop()

# Fonction pour vérifier l'état du serveur via SNMP
async def check_snmp_status():
    transport_target = await UdpTransportTarget.create((server_ip_address, 161))

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
    global wol_sent
    if not wol_sent:
        send_magic_packet(server_mac_address)
        wol_sent = True
        icon.icon = create_image('orange')
        icon.update_menu()

        # Lancer un thread pour restaurer l'état après 60 secondes
        threading.Thread(target=restore_after_wol, args=(icon,)).start()

# Fonction pour restaurer l'icône et réactiver l'option WOL après 30 secondes
def restore_after_wol(icon):
    global wol_sent
    asyncio.run(asyncio.sleep(60))  # Attendre 60 secondes
    wol_sent = False  # Réactiver l'option WOL
    asyncio.run(update_icon(icon))  # Mettre à jour l'icône et l'état du serveur        

# Fonction de mise à jour de l'icône dans la barre des tâches
async def update_icon(icon):
    while True:
        uptime = await check_snmp_status()
        if uptime is not None:
            # Convertir les ticks en secondes
            uptime_seconds = uptime // 100  # Chaque tick est 100 ms
            uptime_display = f'Uptime: {uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m'
            icon.icon = create_image('green')
            icon.title = uptime_display  # Met à jour le tooltip avec l'uptime
            icon.menu = Menu(MenuItem('Quitter', quit_app))  # Menu par défaut quand le serveur est en ligne
        else:
            icon.icon = create_image('orange' if wol_sent else 'red')
            icon.title = "Server Offline"  # Message d'erreur si le serveur est hors ligne
            icon.menu = Menu(
                MenuItem('Allumer', wake_on_lan, enabled=not wol_sent),
                MenuItem('Configuration', open_config),
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
