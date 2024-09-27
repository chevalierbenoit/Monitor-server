from PIL import Image, ImageDraw

# Fonction pour créer une icône de couleur
def create_image(color):
    image = Image.new('RGB', (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 63, 63), outline="black", fill=color)
    return image