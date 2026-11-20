import os
from PIL import Image, ImageFilter, ImageOps

def process_all_menu_images():
    menu_dir = 'Menu'
    out_menu = 'assets/images/menu'
    os.makedirs(out_menu, exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)

    # 1. Cheetos Flamin' Hot con Elote
    print("Procesando Cheetos con Elote...")
    im_cheetos = Image.open(os.path.join(menu_dir, 'cheetosconelote.jpg')).convert('RGB')
    im_cheetos_opt = ImageOps.fit(im_cheetos, (1200, 800), Image.Resampling.LANCZOS)
    im_cheetos_opt.save(os.path.join(out_menu, 'cheetos-flamin-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    im_cheetos_opt.save(os.path.join(out_menu, 'cheetos-flamin-elote.webp'), 'WEBP', quality=85)

    # 1.1 Tostitos con Elote
    if os.path.exists(os.path.join(menu_dir, 'tostitosconelote.jpg')):
        print("Procesando Tostitos con Elote...")
        im_tostitos = Image.open(os.path.join(menu_dir, 'tostitosconelote.jpg')).convert('RGB')
        im_tostitos.save(os.path.join(out_menu, 'tostitos-elote-full.jpg'), 'JPEG', quality=92, subsampling=0)
        im_tostitos_opt = ImageOps.fit(im_tostitos, (1200, 800), Image.Resampling.LANCZOS)
        im_tostitos_opt.save(os.path.join(out_menu, 'tostitos-elote.jpg'), 'JPEG', quality=90, subsampling=0)
        im_tostitos_opt.save(os.path.join(out_menu, 'tostitos-elote.webp'), 'WEBP', quality=85)

    # 2. Conchitas Encanto con Elote
    print("Procesando Conchitas con Elote...")
    im_conchitas = Image.open(os.path.join(menu_dir, 'conchitasconelote.jpg')).convert('RGB')
    im_conchitas_opt = ImageOps.fit(im_conchitas, (1200, 800), Image.Resampling.LANCZOS)
    im_conchitas_opt.save(os.path.join(out_menu, 'conchitas-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    im_conchitas_opt.save(os.path.join(out_menu, 'conchitas-elote.webp'), 'WEBP', quality=85)

    # 3. Ruffles con Elote
    print("Procesando Ruffles con Elote...")
    im_ruffles = Image.open(os.path.join(menu_dir, 'rufflesconelote.jpg')).convert('RGB')
    im_ruffles_opt = ImageOps.fit(im_ruffles, (1200, 800), Image.Resampling.LANCZOS)
    im_ruffles_opt.save(os.path.join(out_menu, 'ruffles-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    im_ruffles_opt.save(os.path.join(out_menu, 'ruffles-elote.webp'), 'WEBP', quality=85)

    # 4. Takis Fuego con Elote
    print("Procesando Takis con Elote...")
    im_takis = Image.open(os.path.join(menu_dir, 'takisconelote.jpg')).convert('RGB')
    im_takis_opt = ImageOps.fit(im_takis, (1200, 800), Image.Resampling.LANCZOS)
    im_takis_opt.save(os.path.join(out_menu, 'takis-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    im_takis_opt.save(os.path.join(out_menu, 'takis-elote.webp'), 'WEBP', quality=85)

    # 5. Doritos con Elote (Card 1200x800 panorámica impecable y continua sin barras oscuras)
    print("Procesando Doritos con Elote...")
    im_doritos_raw = Image.open(os.path.join(menu_dir, 'doritosconelote.jpg')).convert('RGB')
    im_doritos_raw.save(os.path.join(out_menu, 'doritos-elote-full.jpg'), 'JPEG', quality=92, subsampling=0)

    # Base horizontal 1920x1280 del mismo entorno y mesa rústica
    bg_base = Image.open(os.path.join(menu_dir, 'tostitosconelote.jpg')).convert('RGB')
    
    # Recorte del encuadre clave de Doritos: desde parte superior de bolsa hasta tazón y mesa (y=380 a 1880)
    crop_d = im_doritos_raw.crop((0, 380, im_doritos_raw.width, 1880))
    target_h = 1280
    target_w = 1920
    fg_w = int(crop_d.width * (target_h / crop_d.height)) # 1119 px
    fg_doritos = crop_d.resize((fg_w, target_h), Image.Resampling.LANCZOS)
    x_pos = (target_w - fg_w) // 2

    # Máscara con desvanecimiento suave (feathering) en los bordes izquierdo y derecho
    import numpy as np
    mask = np.ones((target_h, fg_w), dtype=np.float32)
    feather = 100
    for x in range(feather):
        alpha = 0.5 - 0.5 * np.cos(np.pi * x / feather)
        mask[:, x] = alpha
        mask[:, fg_w - 1 - x] = alpha
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))

    canvas_doritos = bg_base.copy()
    canvas_doritos.paste(fg_doritos, (x_pos, 0), mask_img)

    # Versión para card en 1200x800 idéntica a Conchitas y Tostitos
    doritos_card = canvas_doritos.resize((1200, 800), Image.Resampling.LANCZOS)
    doritos_card.save(os.path.join(out_menu, 'doritos-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    doritos_card.save(os.path.join(out_menu, 'doritos-elote.webp'), 'WEBP', quality=85)

    # 6. Vaso Chico (1600x1600)
    print("Procesando Vaso Chico...")
    im_vaso_chico = Image.open(os.path.join(menu_dir, 'vaso chico elote.jpg')).convert('RGB')
    # Full para lightbox
    im_vaso_chico.save(os.path.join(out_menu, 'vaso-chico-full.jpg'), 'JPEG', quality=92, subsampling=0)
    # Card 1200x900 (4:3) encuadrando el vaso
    im_vc_card = ImageOps.fit(im_vaso_chico, (1200, 900), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    im_vc_card.save(os.path.join(out_menu, 'vaso-chico.jpg'), 'JPEG', quality=90, subsampling=0)
    im_vc_card.save(os.path.join(out_menu, 'vaso-chico.webp'), 'WEBP', quality=85)

    # 7. Vaso Medio Litro (1600x1600)
    print("Procesando Vaso Medio Litro...")
    im_vaso_mediano = Image.open(os.path.join(menu_dir, 'vaso medio litro elote.jpg')).convert('RGB')
    # Full para lightbox
    im_vaso_mediano.save(os.path.join(out_menu, 'vaso-mediano-full.jpg'), 'JPEG', quality=92, subsampling=0)
    # Card 1200x900 (4:3) encuadrando el vaso mediano
    im_vm_card = ImageOps.fit(im_vaso_mediano, (1200, 900), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    im_vm_card.save(os.path.join(out_menu, 'vaso-mediano.jpg'), 'JPEG', quality=90, subsampling=0)
    im_vm_card.save(os.path.join(out_menu, 'vaso-mediano.webp'), 'WEBP', quality=85)
    # También actualizar assets/images/esquites-vaso.jpg/webp para compatibilidad general
    im_vm_card.save('assets/images/esquites-vaso.jpg', 'JPEG', quality=90, subsampling=0)
    im_vm_card.save('assets/images/esquites-vaso.webp', 'WEBP', quality=85)

    print("\n¡Todas las imágenes del menú fueron procesadas exitosamente!")

if __name__ == '__main__':
    process_all_menu_images()
