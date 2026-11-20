import os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

os.makedirs('assets/real_photos', exist_ok=True)

photos = [
    ('IMG_20261028_155515_HDR.jpg.jpeg', 'foto_1_vertical_arboles.jpg'),
    ('IMG_20261028_155706_HDR.jpg.jpeg', 'foto_2_horizontal_general.jpg'),
    ('IMG_20261104_124256_HDR.jpg.jpeg', 'foto_3_horizontal_mezquites.jpg'),
    ('IMG_20261104_144426_HDR.jpg.jpeg', 'foto_4_horizontal_espacio.jpg'),
    ('1793824325985.jpg.jpeg', 'foto_5_vertical_instalacion.jpg')
]

for src_name, dst_name in photos:
    full_path = os.path.join(r'C:\Users\sergi\Downloads', src_name)
    with Image.open(full_path) as im:
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        print(f'{src_name} -> {dst_name}: {w}x{h}, aspect={w/h:.2f}')
