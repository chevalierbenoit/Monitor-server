from pystray import Icon, Menu, MenuItem
from config_window import open_config
from wol_utils import wake_on_lan
from icon_utils import create_cpu_image
from server_monitor import ServerStatus,ServerMonitor
from snmp_utils import check_snmp_status
import threading
import asyncio

quit_applications = False

# Fonction pour quitter l'application
def quit_app(monitor):
    return lambda icon, item: stop_icon(monitor)

def stop_icon(monitor):
    global quit_applications
    # On quitte l'application en arrêtant l'icône
    quit_applications = True
    monitor.get_icon().stop()

# Fonction pour configurer l'icône et les menus contextuels
def setup_tray_icon():
    monitor = ServerMonitor()
    icon = Icon("SNMP Status", icon=create_cpu_image('#87CEFA'), title="Initialisation...")
    icon.menu = update_icon_menu(monitor)
    monitor.set_icon(icon)

    # Démarrage de la tâche asynchrone dans un thread séparé
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_until_complete, args=(update_icon(monitor),)).start()

    return monitor.get_icon()

# Fonction de mise à jour de l'icône dans la barre des tâches
async def update_icon(monitor):
    global quit_applications

    while True:
        uptime = await check_snmp_status()
        icon = monitor.get_icon()

        # Si l'applicatoire est en cours d'arrêt, on arrête la boucle
        if quit_applications:
            break
        
        if uptime is not None:
            uptime_seconds = uptime // 100
            uptime_display = f'Uptime: {uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m'
            monitor.set_status(ServerStatus.ON)
            icon.menu = update_icon_menu(monitor)
            icon.title = uptime_display
        else:
            if monitor.get_status() != ServerStatus.STARTING:
                if monitor.get_status() != ServerStatus.OFF:
                    monitor.set_status(ServerStatus.OFF)
                    icon.menu = update_icon_menu(monitor)

        await asyncio.sleep(10)  # Vérifier toutes les 10 secondes

def update_icon_menu(monitor):
    menu = Menu(
        MenuItem('Allumer', lambda: wake_on_lan(monitor), enabled=monitor.get_status() == ServerStatus.OFF),
        MenuItem('Configuration', open_config),
        Menu.SEPARATOR,
        MenuItem('Quitter', quit_app(monitor))
    )

    return menu        