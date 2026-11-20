import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_og_logo_image():
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), '#160d08')
    draw = ImageDraw.Draw(img)

    # 1. Fondo con gradiente radial cálido (fogata / atardecer bajo los mezquites)
    for r in range(480, 0, -8):
        alpha = int(35 * (1 - r / 480))
        # Tono ámbar/dorado de brasa
        draw.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(36 + alpha, 22 + alpha//2, 15 + alpha//4))

    # Marco perimetral fino dorado
    border_margin = 32
    draw.rectangle(
        [border_margin, border_margin, W - border_margin, H - border_margin],
        outline='#D99124',
        width=2
    )
    # Esquinas decorativas
    c_len = 24
    for cx, cy, dx, dy in [
        (border_margin, border_margin, 1, 1),
        (W - border_margin, border_margin, -1, 1),
        (border_margin, H - border_margin, 1, -1),
        (W - border_margin, H - border_margin, -1, -1)
    ]:
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill='#F4B52D')

    # 2. Cargar fuentes del sistema o usar fuentes disponibles
    font_large = None
    font_sub = None
    font_slogan = None
    font_tag = None

    font_paths = [
        "C:\\Windows\\Fonts\\georgiab.ttf",
        "C:\\Windows\\Fonts\\georgia.ttf",
        "C:\\Windows\\Fonts\\timesbd.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_large = ImageFont.truetype(fp, 68)
                font_sub = ImageFont.truetype(fp, 46)
                font_slogan = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 24)
                font_tag = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 18)
                break
            except Exception:
                pass

    if not font_large:
        font_large = ImageFont.load_default()
        font_sub = font_large
        font_slogan = font_large
        font_tag = font_large

    # 3. Dibujar Emblema del Logo (Medallón de Maíz y Mezquite)
    center_y = 210
    cx = W // 2

    # Aura y círculos exteriores
    draw.ellipse([cx - 95, center_y - 95, cx + 95, center_y + 95], fill='#2a170d', outline='#D99124', width=3)
    draw.ellipse([cx - 86, center_y - 86, cx + 86, center_y + 86], outline='#596442', width=2)

    # Ramas de mezquite estilizadas
    # Hojas verdes olivo
    leaves = [
        (cx - 50, center_y - 20), (cx - 65, center_y - 45), (cx - 45, center_y - 60),
        (cx + 50, center_y - 20), (cx + 65, center_y - 45), (cx + 45, center_y - 60)
    ]
    for lx, ly in leaves:
        draw.ellipse([lx - 12, ly - 8, lx + 12, ly + 8], fill='#596442')

    # Mazorca dorada estilizada
    elote_poly = [
        (cx, center_y - 65),
        (cx + 26, center_y - 30),
        (cx + 28, center_y + 25),
        (cx + 15, center_y + 55),
        (cx, center_y + 65),
        (cx - 15, center_y + 55),
        (cx - 28, center_y + 25),
        (cx - 26, center_y - 30)
    ]
    draw.polygon(elote_poly, fill='#F4B52D')

    # Granos y detalles de la mazorca
    for gy in range(center_y - 45, center_y + 45, 16):
        draw.arc([cx - 22, gy - 10, cx + 22, gy + 10], start=200, end=340, fill='#D99124', width=3)
    draw.line([cx, center_y - 55, cx, center_y + 55], fill='#D99124', width=3)

    # Hojas de elote en la base (color terracota rojizo)
    draw.arc([cx - 38, center_y + 15, cx + 5, center_y + 65], start=40, end=160, fill='#A94D27', width=4)
    draw.arc([cx - 5, center_y + 15, cx + 38, center_y + 65], start=20, end=140, fill='#A94D27', width=4)
    # Chispa en la base
    draw.polygon([(cx, center_y + 62), (cx - 6, center_y + 72), (cx, center_y + 78), (cx + 6, center_y + 72)], fill='#E04B29')

    # 4. Textos de Marca
    # Tag superior
    tag_text = "AUTÉNTICA TRADICIÓN MEXICANA"
    bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = bbox_tag[2] - bbox_tag[0]
    draw.text((cx - tag_w // 2, 335), tag_text, fill='#D99124', font=font_tag)

    # Nombre "ELOTES"
    text1 = "ELOTES"
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    w1 = bbox1[2] - bbox1[0]
    # Sombra de texto suave
    draw.text((cx - w1 // 2 + 2, 365 + 2), text1, fill='#0a0503', font=font_large)
    draw.text((cx - w1 // 2, 365), text1, fill='#F5E8CE', font=font_large)

    # Nombre "LOS MEZQUITES"
    text2 = "LOS MEZQUITES"
    bbox2 = draw.textbbox((0, 0), text2, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    draw.text((cx - w2 // 2 + 2, 440 + 2), text2, fill='#0a0503', font=font_sub)
    draw.text((cx - w2 // 2, 440), text2, fill='#F4B52D', font=font_sub)

    # Línea decorativa
    line_y = 508
    line_half = 160
    draw.line([cx - line_half, line_y, cx + line_half, line_y], fill='#A94D27', width=2)
    draw.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill='#F4B52D')

    # Eslogan inferior y ubicación
    slogan = "\"Entre mezquites sabe mejor\" • Agua Fría, Apodaca"
    bbox_s = draw.textbbox((0, 0), slogan, font=font_slogan)
    ws = bbox_s[2] - bbox_s[0]
    draw.text((cx - ws // 2, 532), slogan, fill='#E4CCB6', font=font_slogan)

    # 5. Guardar optimizado a JPEG (< 300KB)
    out_path = 'assets/images/og-image.jpg'
    img.save(out_path, 'JPEG', quality=92, subsampling=0)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"PASS: og-image.jpg generado con el LOGO oficial ({size_kb:.2f} KB) - 1200x630")

if __name__ == '__main__':
    create_og_logo_image()
