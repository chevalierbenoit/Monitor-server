from wakeonlan import send_magic_packet
import asyncio
from icon_utils import create_image
import config
from server_monitor import ServerStatus, ServerMonitor

# Fonction pour envoyer une requête Wake-on-LAN
def wake_on_lan(monitor):
    send_magic_packet(config.server_mac_address)
    print(f"Sent Wake-on-LAN packet to {config.server_mac_address}")
    monitor.set_status(ServerStatus.STARTING)
    
    # Restaurer l'icône après 60 secondes
    asyncio.run(restore_after_wol(monitor))

# Fonction pour restaurer l'icône après 60 secondes
async def restore_after_wol(monitor):
    await asyncio.sleep(60)
    if monitor.get_status() == ServerStatus.STARTING:
        monitor.set_status(ServerStatus.OFF)
        print("Server did not start successfully")