"""
Script integral para:
1. Generar la imagen del Vaso de Hielo Seco Blanco de 1/2 litro (Esquites / Vaso Mediano).
2. Generar las imágenes de los especiales con su bolsa oficial de frituras + elote:
   - Tostitos + elote
   - Conchitas Encanto + elote
   - Doritos + elote
   - Cheetos Flamin' Hot + elote
   - Ruffles + elote
   - Takis Fuego + elote
3. Generar la imagen OpenGraph (og-image.jpg) de 1200x630 (< 300 KB) optimizada para compartir la URL en WhatsApp.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

base_dir = r'c:\Users\sergi\MisArchivosLocales\Elotes Los Mezquites'
menu_dir = os.path.join(base_dir, 'assets', 'images', 'menu')
images_dir = os.path.join(base_dir, 'assets', 'images')
brain_dir = r'C:\Users\sergi\.gemini\antigravity\brain\428d142d-1b00-4443-a0e5-615ab2482cea'

# Helper de fuentes
def get_font(size, bold=False):
    font_names = [
        'arialbd.ttf' if bold else 'arial.ttf',
        'calibrib.ttf' if bold else 'calibri.ttf',
        'segoeuib.ttf' if bold else 'segoeui.ttf'
    ]
    for fn in font_names:
        fp = os.path.join(r'C:\Windows\Fonts', fn)
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

# --------------------------------------------------------------------------
# 1. VASO DE HIELO SECO BLANCO DE MEDIO LITRO (16 oz / 500 ml)
# --------------------------------------------------------------------------
print("=== Generando Vaso de Hielo Seco Blanco de Medio Litro ===")
# Base: la foto de alta resolución con la mesa rústica y el elote
ref_vaso = os.path.join(brain_dir, 'esquites_vaso_1795136097714.jpg')
if not os.path.exists(ref_vaso):
    ref_vaso = os.path.join(images_dir, 'esquites-vaso.jpg')

with Image.open(ref_vaso) as base_im:
    w, h = base_im.size
    vaso_img = base_im.convert('RGBA')
    
    # Creamos un overlay que transforma el vaso en el icónico vaso térmico blanco de hielo seco
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Coordenadas del vaso en el centro inferior
    # Vaso de medio litro: tronco cónico blanco con textura de unicel
    cup_top_y = int(h * 0.44)
    cup_bot_y = int(h * 0.94)
    cup_top_w = int(w * 0.36)
    cup_bot_w = int(w * 0.26)
    center_x = int(w * 0.50)
    
    top_l = (center_x - cup_top_w // 2, cup_top_y)
    top_r = (center_x + cup_top_w // 2, cup_top_y)
    bot_r = (center_x + cup_bot_w // 2, cup_bot_y)
    bot_l = (center_x - cup_bot_w // 2, cup_bot_y)
    
    # Dibujar cuerpo del vaso de hielo seco blanco con gradiente de iluminación
    # Lado izquierdo con sombra sutil, centro blanco luminoso, lado derecho luz cálida de fogata
    steps = 100
    for s in range(steps):
        t0 = s / steps
        t1 = (s + 1) / steps
        
        # Interpolar trapezoide vertical
        x_top_start = top_l[0] + (top_r[0] - top_l[0]) * t0
        x_top_end = top_l[0] + (top_r[0] - top_l[0]) * t1
        x_bot_start = bot_l[0] + (bot_r[0] - bot_l[0]) * t0
        x_bot_end = bot_l[0] + (bot_r[0] - bot_l[0]) * t1
        
        # Color del unicel blanco con curvatura cilíndrica 3D
        # Curvatura: coseno para simular cilindro iluminado
        norm_x = (t0 - 0.5) * 2  # -1 a 1
        brightness = math.cos(norm_x * 1.2)
        
        r = int(245 * brightness + 10)
        g = int(242 * brightness + 8)
        b = int(238 * brightness + 5)
        alpha = int(235 * min(1.0, math.sqrt(1 - (norm_x*0.9)**2) if abs(norm_x*0.9) < 1 else 0.5))
        
        slice_poly = [
            (x_top_start, cup_top_y),
            (x_top_end, cup_top_y),
            (x_bot_end, cup_bot_y),
            (x_bot_start, cup_bot_y)
        ]
        draw.polygon(slice_poly, fill=(r, g, b, min(240, alpha + 80)))
    
    # Borde superior redondeado característico del vaso de unicel (lip rim)
    lip_rect = [top_l[0] - 6, cup_top_y - 8, top_r[0] + 6, cup_top_y + 10]
    draw.ellipse(lip_rect, fill=(255, 252, 248, 250), outline=(215, 210, 200, 240), width=2)
    
    # Líneas de textura y relieve horizontal clásico del vaso de hielo seco
    for ring_y_pct in [0.55, 0.68, 0.80]:
        y_pos = int(h * ring_y_pct)
        # Ancho en esa altura
        pct_h = (y_pos - cup_top_y) / (cup_bot_y - cup_top_y)
        w_cur = int(cup_top_w - (cup_top_w - cup_bot_w) * pct_h)
        x_l = center_x - w_cur // 2
        x_r = center_x + w_cur // 2
        draw.arc([x_l, y_pos - 4, x_r, y_pos + 4], 0, 180, fill=(200, 195, 188, 140), width=2)
    
    # Inscripción sutil "1/2 L" y marca de capacidad en el vaso de unicel
    font_cup = get_font(20, bold=True)
    draw.text((center_x, int(h * 0.72)), "1/2 LITRO", fill=(185, 178, 168, 160), font=font_cup, anchor="mm")
    
    # Mezclamos con la base para que el grano de elote, el queso cotija, la crema y el chile se desborden de la parte superior del vaso
    combined = Image.alpha_composite(vaso_img, overlay)
    
    # Recortar de la imagen original la parte superior del elote, queso y chile para que caiga naturalmente SOBRE el vaso
    top_elote_box = (0, 0, w, int(h * 0.49))
    top_elote = base_im.crop(top_elote_box).convert('RGBA')
    combined.paste(top_elote, (0, 0), top_elote)
    
    final_vaso = combined.convert('RGB')
    
    # Guardamos en jpg y webp
    final_vaso.save(os.path.join(images_dir, 'esquites-vaso.jpg'), 'JPEG', quality=88, optimize=True)
    final_vaso.save(os.path.join(images_dir, 'esquites-vaso.webp'), 'WEBP', quality=85)
    print("Vaso de hielo seco guardado con éxito!")


# --------------------------------------------------------------------------
# 2. FOTOGRAFÍAS DE LOS ESPECIALES CON LA BOLSA OFICIAL DE FRITURAS + ELOTE
# --------------------------------------------------------------------------
print("=== Generando Fotos de Especiales con la Bolsa de la Fritura + Elote ===")

ref_base_food = os.path.join(brain_dir, 'tostitos_con_elote_1795136131169.jpg')
if not os.path.exists(ref_base_food):
    ref_base_food = os.path.join(menu_dir, 'tostitos-elote.jpg')

specials_config = [
    {
        'id': 'tostitos-elote',
        'brand_name': 'TOSTITOS',
        'sub_name': 'SALSA VERDE',
        'bag_color_top': (20, 130, 50),     # Verde salsa verde
        'bag_color_bot': (10, 85, 30),
        'accent_color': (244, 181, 45),     # Dorado totopo
        'slogan': 'PARA COMPARTIR'
    },
    {
        'id': 'conchitas-elote',
        'brand_name': 'CONCHITAS',
        'sub_name': 'ENCANTO',
        'bag_color_top': (200, 16, 46),     # Rojo Encanto
        'bag_color_bot': (140, 10, 30),
        'accent_color': (253, 184, 19),    # Amarillo dorado Encanto
        'slogan': 'MTY DESDE 1957'
    },
    {
        'id': 'doritos-elote',
        'brand_name': 'DORITOS',
        'sub_name': 'NACHO',
        'bag_color_top': (222, 78, 28),     # Rojo fuego nacho
        'bag_color_bot': (160, 40, 10),
        'accent_color': (254, 165, 21),    # Amarillo queso nacho
        'slogan': 'FOR THE BOLD'
    },
    {
        'id': 'cheetos-flamin-elote',
        'brand_name': 'CHEETOS',
        'sub_name': "FLAMIN' HOT",
        'bag_color_top': (216, 30, 5),      # Rojo flamin
        'bag_color_bot': (247, 146, 57),    # Naranja cheeto
        'accent_color': (255, 241, 0),     # Amarillo queso
        'slogan': 'DANGEROUSLY CHEESY'
    },
    {
        'id': 'ruffles-elote',
        'brand_name': 'RUFFLES',
        'sub_name': 'ONDULADAS',
        'bag_color_top': (0, 113, 178),     # Azul Ruffles
        'bag_color_bot': (0, 70, 120),
        'accent_color': (237, 28, 36),     # Rojo Ruffles
        'slogan': 'CON RIDGES'
    },
    {
        'id': 'takis-elote',
        'brand_name': 'TAKIS',
        'sub_name': 'FUEGO',
        'bag_color_top': (78, 21, 136),     # Morado Takis
        'bag_color_bot': (40, 10, 70),
        'accent_color': (255, 222, 0),     # Amarillo neón
        'slogan': 'FUEGO INTENSO'
    }
]

with Image.open(ref_base_food) as food_im:
    w, h = food_im.size
    
    for item in specials_config:
        plate = food_im.convert('RGBA')
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Dibujamos la bolsa de frituras abierta horizontalmente (presentación tradicional mexicana)
        # o colocada estilísticamente en la parte superior-izquierda junto al elote preparado
        # Ancho bolsa: 380px, Alto: 320px
        bag_x = int(w * 0.08)
        bag_y = int(h * 0.12)
        bag_w = int(w * 0.32)
        bag_h = int(h * 0.48)
        
        # Puntos de la bolsa estilizada 3D con pliegues realistas de empaque metalizado
        p_tl = (bag_x + 30, bag_y)
        p_tr = (bag_x + bag_w - 20, bag_y + 15)
        p_br = (bag_x + bag_w, bag_y + bag_h)
        p_bl = (bag_x, bag_y + bag_h - 10)
        
        # Sombra de la bolsa en la mesa de madera
        shadow_poly = [
            (p_tl[0] - 10, p_tl[1] + 15),
            (p_tr[0] + 15, p_tr[1] + 15),
            (p_br[0] + 25, p_br[1] + 25),
            (p_bl[0] - 15, p_bl[1] + 25)
        ]
        draw.polygon(shadow_poly, fill=(0, 0, 0, 140))
        
        # Relleno con gradiente de la bolsa
        steps = 60
        for s in range(steps):
            f = s / steps
            cur_top_x = p_tl[0] + (p_tr[0] - p_tl[0]) * f
            cur_top_y = p_tl[1] + (p_tr[1] - p_tl[1]) * f
            cur_bot_x = p_bl[0] + (p_br[0] - p_bl[0]) * f
            cur_bot_y = p_bl[1] + (p_br[1] - p_bl[1]) * f
            
            # Color con reflejo metálico brillante en el centro
            shine = math.sin(f * math.pi) ** 2
            cr = int(item['bag_color_top'][0] * (1 - f) + item['bag_color_bot'][0] * f + 60 * shine)
            cg = int(item['bag_color_top'][1] * (1 - f) + item['bag_color_bot'][1] * f + 60 * shine)
            cb = int(item['bag_color_top'][2] * (1 - f) + item['bag_color_bot'][2] * f + 60 * shine)
            cr = min(255, cr)
            cg = min(255, cg)
            cb = min(255, cb)
            
            draw.line([(cur_top_x, cur_top_y), (cur_bot_x, cur_bot_y)], fill=(cr, cg, cb, 255), width=7)
        
        # Borde metalizado superior en zigzag (sellado de bolsa)
        zigzag_y = p_tl[1]
        for zx in range(int(p_tl[0]), int(p_tr[0]), 8):
            draw.line([(zx, zigzag_y), (zx + 4, zigzag_y + 4), (zx + 8, zigzag_y)], fill=(230, 230, 230, 230), width=2)
            
        # Logotipo / Tipografía oficial de la marca en la bolsa
        font_brand = get_font(36, bold=True)
        font_sub = get_font(18, bold=True)
        font_slogan = get_font(13, bold=False)
        
        center_bag_x = bag_x + bag_w // 2
        center_bag_y = bag_y + bag_h // 2
        
        # Caja de contraste para el logo
        draw.rectangle([center_bag_x - 110, center_bag_y - 45, center_bag_x + 110, center_bag_y + 45],
                       fill=(15, 10, 8, 170), outline=item['accent_color'], width=2)
                       
        # Texto de la marca
        draw.text((center_bag_x, center_bag_y - 20), item['brand_name'], fill=(255, 255, 255, 255),
                  font=font_brand, anchor="mm")
        draw.text((center_bag_x, center_bag_y + 12), item['sub_name'], fill=item['accent_color'],
                  font=font_sub, anchor="mm")
        draw.text((center_bag_x, center_bag_y + 30), item['slogan'], fill=(240, 235, 225, 230),
                  font=font_slogan, anchor="mm")
        
        # Insignia "+ ELOTE PREPARADO" que une la botana con los esquites
        plus_box_y = bag_y + bag_h - 25
        draw.rounded_rectangle([center_bag_x - 120, plus_box_y, center_bag_x + 120, plus_box_y + 34],
                               radius=17, fill=(244, 181, 45, 245), outline=(36, 22, 15, 255), width=2)
        font_plus = get_font(14, bold=True)
        draw.text((center_bag_x, plus_box_y + 17), "+ ELOTE & ESQUITES", fill=(36, 22, 15, 255),
                  font=font_plus, anchor="mm")
                  
        # Combinar el overlay de la bolsa sobre la fotografía del elote
        combined_special = Image.alpha_composite(plate, overlay).convert('RGB')
        
        jpg_dest = os.path.join(menu_dir, item['id'] + '.jpg')
        webp_dest = os.path.join(menu_dir, item['id'] + '.webp')
        combined_special.save(jpg_dest, 'JPEG', quality=88, optimize=True)
        combined_special.save(webp_dest, 'WEBP', quality=85)
        print(f"Especial guardado: {item['id']} con bolsa oficial ({os.path.getsize(jpg_dest)} B)")


# --------------------------------------------------------------------------
# 3. IMAGEN OPEN GRAPH (og-image.jpg) PARA COMPARTIR EN WHATSAPP (< 300 KB)
# --------------------------------------------------------------------------
print("=== Generando Imagen OpenGraph Oficial para WhatsApp (1200x630, <300KB) ===")
target_w, target_h = 1200, 630
og_canvas = Image.new('RGBA', (target_w, target_h), (36, 22, 15, 255))

# Usamos la fotografía cinematográfica de fondo
with Image.open('assets/images/hero-mezquites.jpg') as hero_bg:
    bg_w, bg_h = hero_bg.size
    # Crop central 1200x630
    aspect_target = target_w / target_h
    aspect_curr = bg_w / bg_h
    if aspect_curr > aspect_target:
        new_w = int(bg_h * aspect_target)
        crop_box = ((bg_w - new_w) // 2, 0, (bg_w + new_w) // 2, bg_h)
    else:
        new_h = int(bg_w / aspect_target)
        crop_box = (0, (bg_h - new_h) // 2, bg_w, (bg_h + new_h) // 2)
    cropped_bg = hero_bg.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
    og_canvas.paste(cropped_bg, (0, 0))

# Capa de oscurecimiento rústica y viñeta lateral para legibilidad
draw_og = ImageDraw.Draw(og_canvas)
vignette = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
v_draw = ImageDraw.Draw(vignette)
for x in range(target_w):
    alpha = int(140 + 70 * (x / target_w))
    v_draw.line([(x, 0), (x, target_h)], fill=(20, 12, 8, min(230, alpha)))
og_canvas = Image.alpha_composite(og_canvas, vignette)
draw_og = ImageDraw.Draw(og_canvas)

# Marco artesanal dorado
draw_og.rectangle([25, 25, target_w - 25, target_h - 25], outline=(244, 181, 45, 180), width=3)
draw_og.rectangle([35, 35, target_w - 35, target_h - 35], outline=(245, 232, 206, 60), width=1)

# Textos de Marca Oficiales
font_title = get_font(58, bold=True)
font_sub = get_font(30, bold=True)
font_slogan = get_font(22, bold=False)
font_badge = get_font(18, bold=True)

# Badge superior
badge_text = "🌽 ESPACIO GASTRONÓMICO MEXICANO · AGUA FRÍA, APODACA"
draw_og.rounded_rectangle([70, 75, 780, 115], radius=20, fill=(217, 145, 36, 230), outline=(244, 181, 45), width=2)
draw_og.text((425, 95), badge_text, fill=(36, 22, 15), font=get_font(15, bold=True), anchor="mm")

# Título Principal
draw_og.text((70, 175), "ELOTES", fill=(244, 181, 45), font=font_title)
draw_og.text((70, 240), "LOS MEZQUITES", fill=(245, 232, 206), font=font_title)

# Slogan
draw_og.text((72, 330), '"Entre mezquites sabe mejor."', fill=(244, 181, 45), font=font_sub)
draw_og.text((72, 375), "Tradición mexicana a las brasas, fogatas y convivencia al aire libre.", fill=(245, 232, 206, 220), font=font_slogan)

# Menú destacado
menu_features = [
    "🔥 Elotes Asados a las Brasas ($50)",
    "🥣 Elote en Vaso de Hielo Seco ($45 - $60)",
    "🌶️ Especiales: Tostitos, Conchitas, Doritos y Takis ($85)",
    "🚗 Pide en Línea y Recoge de Pasada (Mercado Pago)"
]

card_y = 425
for feat in menu_features:
    draw_og.text((72, card_y), feat, fill=(245, 232, 206), font=get_font(17, bold=True))
    card_y += 32

# Badge de Ubicación y Teléfono en la esquina inferior derecha
draw_og.rounded_rectangle([780, 520, target_w - 70, target_h - 60], radius=14, fill=(36, 22, 15, 240), outline=(244, 181, 45, 200), width=2)
draw_og.text((950, 545), "📍 Morelos 654, Agua Fría, Apodaca, N.L.", fill=(245, 232, 206), font=get_font(14, bold=True), anchor="mm")
draw_og.text((950, 570), "📞 WhatsApp: 81 2191 2778", fill=(244, 181, 45), font=get_font(14, bold=True), anchor="mm")

# Guardar y validar peso estricto < 300KB
og_dest = os.path.join(images_dir, 'og-image.jpg')
og_rgb = og_canvas.convert('RGB')
og_rgb.save(og_dest, 'JPEG', quality=84, optimize=True)
og_size_kb = os.path.getsize(og_dest) / 1024
print(f"og-image.jpg generado con éxito: {og_size_kb:.2f} KB (cumple < 300 KB: {og_size_kb < 300})")
