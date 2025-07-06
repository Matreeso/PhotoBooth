from PIL import Image

bg = Image.open("background.png").convert("RGBA")

# Load your four images
imgs = [
    Image.open(f"img{i+1}.png").convert("RGBA")
    for i in range(4)
]

positions = [
    (50, 50),             # top-left corner of 1st image
    (300, 50),            # 2nd image
    (50, 300),            # 3rd image
    (300, 300),           # 4th image
]

# Suppose each spot is 200×200 pixels:
target_size = (200, 200)
resized = [im.resize(target_size, Image.Resampling.LANCZOS) for im in imgs]

for im, pos in zip(resized, positions):
    bg.paste(im, pos, im)  # using the image itself as a mask :contentReference[oaicite:6]{index=6}

bg.save("composite.png")
