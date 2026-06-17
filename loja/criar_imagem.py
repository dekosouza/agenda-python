import os
from PIL import Image

os.makedirs("static/img", exist_ok=True)
img = Image.new("RGB", (600, 600), "#e0e7ff")
img.save("static/img/sem-imagem.jpg")
print("Imagem criada!")