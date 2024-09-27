import tkinter as tk
import config

# Fonction pour ouvrir la fenêtre de configuration
def open_config():
    def save_config():
        config.set_server_ip(ip_entry.get())
        config.set_server_mac(mac_entry.get())
        print(f"Nouvelle configuration - IP: {config.server_ip_address}, MAC: {config.server_mac_address}")
        config_window.destroy()

    def cancel_config():
        config_window.destroy()

    # Création de la fenêtre de configuration
    config_window = tk.Tk()
    config_window.title("Configuration du Serveur")

    # Champs pour l'adresse IP
    tk.Label(config_window, text="Adresse IP:").grid(row=0, column=0, padx=10, pady=10)
    ip_entry = tk.Entry(config_window)
    ip_entry.grid(row=0, column=1, padx=10, pady=10)
    ip_entry.insert(0, config.server_ip_address)

    # Champs pour l'adresse MAC
    tk.Label(config_window, text="Adresse MAC:").grid(row=1, column=0, padx=10, pady=10)
    mac_entry = tk.Entry(config_window)
    mac_entry.grid(row=1, column=1, padx=10, pady=10)
    mac_entry.insert(0, config.server_mac_address)

    # Boutons Sauvegarder et Annuler
    save_button = tk.Button(config_window, text="Sauvegarder", command=save_config)
    save_button.grid(row=2, column=0, padx=10, pady=10)
    
    cancel_button = tk.Button(config_window, text="Annuler", command=cancel_config)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)

    config_window.mainloop()
