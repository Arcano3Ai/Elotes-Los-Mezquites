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

    # 5. Doritos con Elote (Vertical -> Card 1200x800 con presentación impecable)
    print("Procesando Doritos con Elote...")
    im_doritos = Image.open(os.path.join(menu_dir, 'doritosconelote.jpg')).convert('RGB')
    # Versión completa original para modal lightbox
    im_doritos.save(os.path.join(out_menu, 'doritos-elote-full.jpg'), 'JPEG', quality=92, subsampling=0)
    
    # Para la card: lienzo 1200x800 que contiene la imagen vertical completa sin cortar la bolsa ni el elote,
    # con fondo desenfocado y viñeta sutil del mismo ambiente rústico.
    bg = ImageOps.fit(im_doritos, (1200, 800), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=25))
    # Diminuir brillo del fondo para que resalte el producto al centro
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Brightness(bg)
    bg = enhancer.enhance(0.55)
    
    # Escalar la imagen de doritos para que entre en 800 de alto
    h_target = 800
    w_target = int(im_doritos.width * (h_target / im_doritos.height))
    fg = im_doritos.resize((w_target, h_target), Image.Resampling.LANCZOS)
    x_pos = (1200 - w_target) // 2
    bg.paste(fg, (x_pos, 0))
    bg.save(os.path.join(out_menu, 'doritos-elote.jpg'), 'JPEG', quality=90, subsampling=0)
    bg.save(os.path.join(out_menu, 'doritos-elote.webp'), 'WEBP', quality=85)

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
