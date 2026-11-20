import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('assets/images', exist_ok=True)

# 1. Crear lienzo 1200x630
w, h = 1200, 630
img = Image.new('RGB', (w, h), color='#24160F')
draw = ImageDraw.Draw(img)

# 2. Gradiente radial de fondo en tonos café carbón y madera oscura
for r in range(450, 0, -5):
    alpha = int(255 * (1 - (r / 450) ** 1.5))
    # Color madera cálida en el centro (#382116 -> #4a2b1c)
    color = (56 + int(24 * (1 - r/450)), 33 + int(14 * (1 - r/450)), 22 + int(8 * (1 - r/450)))
    draw.ellipse([w//2 - r*1.4, h//2 - r*0.9, w//2 + r*1.4, h//2 + r*0.9], fill=color)

# Marco dorado sutil
draw.rectangle([24, 24, w - 24, h - 24], outline='#D99124', width=2)
draw.rectangle([32, 32, w - 32, h - 32], outline='#382116', width=1)

# Dibujar símbolo del maíz artesanal en el centro superior
cx, cy = w // 2, 210

# Círculo base del emblema
draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill='#382116', outline='#F4B52D', width=3)
draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill='#24160F', outline='#D99124', width=2)

# Mazorca dorada estilizada
draw.polygon([
    (cx, cy - 50),
    (cx + 26, cy - 20),
    (cx + 24, cy + 25),
    (cx, cy + 50),
    (cx - 24, cy + 25),
    (cx - 26, cy - 20)
], fill='#F4B52D')

# Hojas y espigas
draw.line([(cx, cy - 40), (cx, cy + 42)], fill='#D99124', width=3)
draw.line([(cx - 15, cy - 15), (cx + 15, cy - 15)], fill='#D99124', width=3)
draw.line([(cx - 18, cy + 5), (cx + 18, cy + 5)], fill='#D99124', width=3)
draw.line([(cx - 14, cy + 25), (cx + 14, cy + 25)], fill='#D99124', width=3)

# Ramas de mezquite en verde mezquite (#596442) a los lados
draw.arc([cx - 95, cy - 40, cx - 45, cy + 50], 90, 270, fill='#596442', width=4)
draw.arc([cx + 45, cy - 40, cx + 95, cy + 50], 270, 90, fill='#596442', width=4)

# Intentar cargar fuentes del sistema o usar default escalada
def get_font(name, size):
    paths = [
        f'C:/Windows/Fonts/{name}.ttf',
        f'C:/Windows/Fonts/{name}.otf',
        f'C:/Windows/Fonts/{name.lower()}.ttf',
        'C:/Windows/Fonts/georgia.ttf',
        'C:/Windows/Fonts/arial.ttf'
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

font_sub = get_font('georgiab', 22)
font_title = get_font('georgiab', 58)
font_slogan = get_font('georgiai', 32)
font_loc = get_font('arial', 20)

# Textos
# 1. Subtítulo superior
sub_text = "SABORES TRADICIONALES DE NUEVO LEÓN"
bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
sw = bbox_sub[2] - bbox_sub[0]
draw.text(((w - sw) // 2, 335), sub_text, fill='#D99124', font=font_sub)

# 2. Título principal
title_text = "ELOTES LOS MEZQUITES"
bbox_title = draw.textbbox((0, 0), title_text, font=font_title)
tw = bbox_title[2] - bbox_title[0]
draw.text(((w - tw) // 2, 375), title_text, fill='#F5E8CE', font=font_title)

# Línea divisoria decorativa
draw.line([(w // 2 - 180, 455), (w // 2 + 180, 455)], fill='#A94D27', width=3)
draw.ellipse([w // 2 - 6, 455 - 6, w // 2 + 6, 455 + 6], fill='#F4B52D')

# 3. Slogan oficial
slogan_text = '"Entre mezquites sabe mejor."'
bbox_slogan = draw.textbbox((0, 0), slogan_text, font=font_slogan)
slw = bbox_slogan[2] - bbox_slogan[0]
draw.text(((w - slw) // 2, 475), slogan_text, fill='#F4B52D', font=font_slogan)

# 4. Ubicación para SEO local y WhatsApp
loc_text = "📍 Morelos 654, Agua Fría, Apodaca, NL | 📞 81 2191 2778"
bbox_loc = draw.textbbox((0, 0), loc_text, font=font_loc)
lw = bbox_loc[2] - bbox_loc[0]
draw.text(((w - lw) // 2, 545), loc_text, fill='#F5E8CE', font=font_loc)

# Guardar y optimizar para que cumpla estricto peso < 300KB
og_out = 'assets/images/og-image.jpg'
img.save(og_out, 'JPEG', quality=88, optimize=True)
size_kb = os.path.getsize(og_out) / 1024
print(f'og-image.jpg generado con logo: {size_kb:.2f} KB (cumple < 300KB: {size_kb < 300})')
