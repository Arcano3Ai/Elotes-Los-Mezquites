import os
import urllib.request
from PIL import Image

os.makedirs('assets/images', exist_ok=True)
os.makedirs('assets/icons', exist_ok=True)

# 1. Process Elotes Los Mezquites.png
ref_path = 'Elotes Los Mezquites.png'
if os.path.exists(ref_path):
    with Image.open(ref_path) as im:
        rgb_im = im.convert('RGB')
        w, h = rgb_im.size
        # Hero webp (max 1920w)
        hero = rgb_im.resize((1920, int(h * 1920 / w)), Image.Resampling.LANCZOS)
        hero.save('assets/images/hero-mezquites.webp', 'WEBP', quality=85)
        hero.save('assets/images/hero-mezquites.jpg', 'JPEG', quality=85)
        print('Saved hero images')
        
        # OG Image: 1200x630
        target_w, target_h = 1200, 630
        aspect = target_w / target_h
        current_aspect = w / h
        if current_aspect > aspect:
            new_w = int(h * aspect)
            left = (w - new_w) // 2
            crop_im = rgb_im.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / aspect)
            top = (h - new_h) // 2
            crop_im = rgb_im.crop((0, top, w, top + new_h))
        og_im = crop_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        og_im.save('assets/images/og-image.jpg', 'JPEG', quality=82)
        og_size_kb = os.path.getsize('assets/images/og-image.jpg') / 1024
        print(f'Saved og-image.jpg ({og_size_kb:.1f} KB - required <300KB)')

# 2. Curate high quality images for gastronomic gallery & essence
images_to_fetch = [
    {
        'name': 'elote-preparado',
        # Delicious street corn with queso and chile
        'url': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=1200&q=80'
    },
    {
        'name': 'elote-asado-chile',
        # Grilled roasted corn
        'url': 'https://images.unsplash.com/photo-1582234372722-50d7ccc30ebd?auto=format&fit=crop&w=1200&q=80'
    },
    {
        'name': 'esquites-vaso',
        # Corn cup
        'url': 'https://images.unsplash.com/photo-1506084868230-bb9d95c24759?auto=format&fit=crop&w=1200&q=80'
    },
    {
        'name': 'salsas-artesanales',
        # Traditional Mexican sauces
        'url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=1200&q=80'
    },
    {
        'name': 'fogata-noche',
        # Campfire
        'url': 'https://images.unsplash.com/photo-1508873696983-2df570464753?auto=format&fit=crop&w=1200&q=80'
    },
    {
        'name': 'convivencia-madera',
        # Warm outdoor seating
        'url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80'
    }
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
for item in images_to_fetch:
    name = item['name']
    raw_path = f'assets/images/{name}_raw.jpg'
    webp_path = f'assets/images/{name}.webp'
    jpg_path = f'assets/images/{name}.jpg'
    try:
        req = urllib.request.Request(item['url'], headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp, open(raw_path, 'wb') as f:
            f.write(resp.read())
        with Image.open(raw_path) as im:
            rgb = im.convert('RGB')
            # Save webp and jpg
            rgb.save(webp_path, 'WEBP', quality=85)
            rgb.save(jpg_path, 'JPEG', quality=85)
        if os.path.exists(raw_path):
            os.remove(raw_path)
        print(f'Successfully downloaded and processed: {name}')
    except Exception as e:
        print(f'Failed to fetch {name}: {e}')
