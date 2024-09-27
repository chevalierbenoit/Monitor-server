from enum import Enum
from icon_utils import create_image

class ServerStatus(Enum):
    ON = "Allumé"
    OFF = "Éteint"
    STARTING = "En cours d'allumage"

class ServerMonitor():
    def __init__(self):
        self.current_status = ServerStatus.OFF
        self.current_icon = None

    def set_status(self,status):
        print(f"Changement de l'état du serveur: {status}")
        self.current_status = status
        if self.current_icon is not None:
            self.update_icon()

    def get_status(self):
        return self.current_status

    def set_icon(self,icon):
        self.current_icon = icon

    def get_icon(self):
        return self.current_icon
    
    def update_icon(self):
        print("Mise à jour de l'icône...")
        if self.current_status == ServerStatus.ON:
            self.current_icon.icon = create_image('green')
            self.current_icon.title = "Serveur Allumé"
        elif self.current_status == ServerStatus.OFF:
            self.current_icon.icon = create_image('red')
            self.current_icon.title = "Serveur Éteint"
        elif self.current_status == ServerStatus.STARTING:
            self.current_icon.icon = create_image('orange')
            self.current_icon.title = "Serveur en cours d'allumage"

        print("Mise à jour de l'icône terminée.")
        # self.current_icon.run()    