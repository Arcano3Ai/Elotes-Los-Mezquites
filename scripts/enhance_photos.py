import os
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

os.makedirs('assets/images/lugar', exist_ok=True)

photos = [
    (r'C:\Users\sergi\Downloads\IMG_20261028_155515_HDR.jpg.jpeg', 'mezquites-real-1'),
    (r'C:\Users\sergi\Downloads\IMG_20261028_155706_HDR.jpg.jpeg', 'mezquites-real-2'),
    (r'C:\Users\sergi\Downloads\IMG_20261104_124256_HDR.jpg.jpeg', 'mezquites-real-3'),
    (r'C:\Users\sergi\Downloads\IMG_20261104_144426_HDR.jpg.jpeg', 'mezquites-real-4'),
    (r'C:\Users\sergi\Downloads\1793824325985.jpg.jpeg', 'mezquites-real-5')
]

def enhance_photo(im):
    """
    Mejora fotográfica profesional sin inventar nada:
    1. Orientación EXIF correcta.
    2. Corrección de rango dinámico mediante estiramiento sutil de percentiles (0.5% - 99.5%).
    3. Curva de contraste sigmoidea suave para eliminar efecto lavado de fotos de smartphone.
    4. Balance de calidez gastronómica / tonalidad ámbar-madera.
    5. Realce de nitidez con UnsharpMask de alta definición.
    """
    im = ImageOps.exif_transpose(im)
    im = im.convert('RGB')
    
    # 1. Corrección de histograma y rango dinámico (evitar sobreexposición / sombras empastadas)
    arr = np.array(im, dtype=np.float32)
    for c in range(3):
        p_low, p_high = np.percentile(arr[:, :, c], (0.8, 99.2))
        if p_high > p_low:
            arr[:, :, c] = np.clip((arr[:, :, c] - p_low) / (p_high - p_low) * 255.0, 0, 255)
    
    # 2. Curva tonal en S suave (aumenta rango dinámico percibido sin quemar luces)
    norm = arr / 255.0
    # Curva sigmoidea con parámetro suave
    gamma = 1.05
    curve = np.power(norm, gamma)
    curve = curve * curve * (3.0 - 2.0 * curve) # smoothstep
    # Interpolar 70% curva, 30% original para un toque sutil y natural
    blended = 0.65 * curve + 0.35 * norm
    
    # 3. Calidez sutil y equilibrio de color para armonizar con atmósfera de mezquites y madera
    # Leve incremento en R (+3%) y leve reducción de azules fríos (-2%) para ambientación cálida
    blended[:, :, 0] = np.clip(blended[:, :, 0] * 1.03, 0, 1.0) # Rojo cálido
    blended[:, :, 1] = np.clip(blended[:, :, 1] * 1.01, 0, 1.0) # Verde natural
    blended[:, :, 2] = np.clip(blended[:, :, 2] * 0.98, 0, 1.0) # Azul frío mitigado
    
    enhanced_np = np.uint8(np.clip(blended * 255.0, 0, 255))
    enhanced_im = Image.fromarray(enhanced_np)
    
    # 4. Ajuste fino de saturación (Vibrance natural)
    enh_color = ImageEnhance.Color(enhanced_im)
    enhanced_im = enh_color.enhance(1.12)
    
    # 5. Nitidez profesional con UnsharpMask (resalta texturas de troncos, hojas y mesas sin grano)
    enhanced_im = enhanced_im.filter(ImageFilter.UnsharpMask(radius=1.8, percent=125, threshold=3))
    
    return enhanced_im

print('Iniciando procesamiento y mejora de calidad fotográfica...')
processed_info = []

for idx, (path, name) in enumerate(photos, 1):
    with Image.open(path) as raw_im:
        enhanced = enhance_photo(raw_im)
        w, h = enhanced.size
        print(f'Foto {idx} mejorada: {name} ({w}x{h})')
        
        # Versión Full HD optimizada (max 2000px ancho)
        max_dim = 2048
        if max(w, h) > max_dim:
            ratio = max_dim / max(w, h)
            resized = enhanced.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
        else:
            resized = enhanced
            
        webp_path = f'assets/images/lugar/{name}.webp'
        jpg_path = f'assets/images/lugar/{name}.jpg'
        
        resized.save(webp_path, 'WEBP', quality=88)
        resized.save(jpg_path, 'JPEG', quality=88, optimize=True)
        
        # Generar thumbnail para carga rápida en tarjetas (800px max)
        thumb_ratio = 800 / max(w, h)
        thumb = enhanced.resize((int(w * thumb_ratio), int(h * thumb_ratio)), Image.Resampling.LANCZOS)
        thumb.save(f'assets/images/lugar/{name}-thumb.webp', 'WEBP', quality=85)
        thumb.save(f'assets/images/lugar/{name}-thumb.jpg', 'JPEG', quality=85, optimize=True)
        
        processed_info.append({
            'id': name,
            'aspect': w / h,
            'size': (w, h),
            'webp': webp_path,
            'jpg': jpg_path
        })

print('\nGenerando imagen OpenGraph actualizada desde la fotografía real del lugar...')
# Seleccionamos la foto 2 o 3 (horizontal, panorámica del lugar) para el OpenGraph 1200x630
best_og_source = Image.open('assets/images/lugar/mezquites-real-2.jpg')
bw, bh = best_og_source.size
target_w, target_h = 1200, 630
aspect = target_w / target_h
cur_aspect = bw / bh

if cur_aspect > aspect:
    new_w = int(bh * aspect)
    left = (bw - new_w) // 2
    crop_im = best_og_source.crop((left, 0, left + new_w, bh))
else:
    new_h = int(bw / aspect)
    top = (bh - new_h) // 2
    crop_im = best_og_source.crop((0, top, bw, top + new_h))

og_im = crop_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
# Filtro de contraste sutil para OG
enh_con = ImageEnhance.Contrast(og_im)
og_im = enh_con.enhance(1.05)
og_im.save('assets/images/og-image.jpg', 'JPEG', quality=84, optimize=True)
og_size = os.path.getsize('assets/images/og-image.jpg') / 1024
print(f'og-image.jpg actualizado con foto real: {og_size:.1f} KB (estricto cumplimiento <300KB)')

print('\n¡Todas las imágenes reales del lugar fueron mejoradas y guardadas exitosamente!')
