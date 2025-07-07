from PIL import Image

bg = Image.open("./resources/background.png").convert("RGBA")
bgX = 192
bgY = 578
target_size = (160, 90)
x_pos = int((bgX - target_size[0])/2)

# Load your four images
imgs = [
    Image.open(f"captured_photo{i+0}.jpg").convert("RGBA")
    for i in range(3)
]

#192x578
positions = [
    (x_pos, 72),
    (x_pos, 72+144),
    (x_pos, 72+144+144),
]

# Suppose each spot is 200×200 pixels:
target_size = (160, 90)
resized = [im.resize(target_size, Image.Resampling.LANCZOS) for im in imgs]

for im, pos in zip(resized, positions):
    bg.paste(im, pos, im)  # using the image itself as a mask :contentReference[oaicite:6]{index=6}

bg.save("composite.png")
