from PIL import Image, ImageColor

def change_image_color(image_path, color):
    # Charger l'image PNG
    image = Image.open(image_path).convert("RGBA")

    # Créer une nouvelle image pour stocker le résultat
    colored_image = Image.new("RGBA", image.size)

    # Remplacer les pixels non transparents par la nouvelle couleur
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = image.getpixel((x, y))
            # Si le pixel n'est pas transparent
            if a > 0:
                colored_image.putpixel((x, y), (color[0], color[1], color[2], a))
            else:
                colored_image.putpixel((x, y), (0, 0, 0, 0))  # Garder transparent

    return colored_image

def create_cpu_image(html_color):
    color = ImageColor.getrgb(html_color)
    return change_image_color("img/cpu.png", color) 