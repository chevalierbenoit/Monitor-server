import asyncio
from pysnmp.hlapi.asyncio import *
from PIL import Image, ImageDraw
import config

# Fonction pour vérifier l'état du serveur via SNMP
async def check_snmp_status():
    transport_target = await UdpTransportTarget.create((config.get_server_ip(), 161))
    
    error_indication, error_status, error_index, var_binds = await getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),  # SNMP v1, changez si nécessaire
        transport_target,
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))  # OID pour sysUptime
    )

    if error_indication:
        return None  # Serveur hors ligne
    elif error_status:
        return None
    else:
        uptime_ticks = var_binds[0][1]
        return uptime_ticks
