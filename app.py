from tray_icon import setup_tray_icon

# Fonction principale de démarrage
def main():
    icon = setup_tray_icon()  # Configurer l'icône avec les menus contextuels
    icon.run()

if __name__ == "__main__":
    main()
