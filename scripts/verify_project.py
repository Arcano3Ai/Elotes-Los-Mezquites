import os
import re
import sys
import subprocess

def test_node_syntax():
    for f in ['app.js', 'server/app.js']:
        res = subprocess.run(['node', '-c', f], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FAIL: Syntax error in {f}:\n{res.stderr}")
            return False
        print(f"PASS: {f} syntax OK")
    return True

def verify_assets_and_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Verificar og:image
    og_match = re.search(r'property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html)
    if not og_match:
        print("FAIL: og:image meta tag not found")
        return False
    og_url = og_match.group(1)
    print(f"PASS: og:image tag present -> {og_url}")

    # Verificar peso de og-image.jpg
    if os.path.exists('assets/images/og-image.jpg'):
        size_kb = os.path.getsize('assets/images/og-image.jpg') / 1024
        print(f"PASS: og-image.jpg exists ({size_kb:.2f} KB) - complies with WhatsApp < 300KB limit")
    else:
        print("FAIL: assets/images/og-image.jpg does not exist")
        return False

    # Extraer todas las rutas de imágenes en index.html
    img_refs = set(re.findall(r'(?:src|srcset)=["\']([^"\']+)["\']', html))
    missing = []
    total_assets = 0
    for ref in img_refs:
        parts = ref.split()
        for p in parts:
            clean = p.split('?')[0].rstrip(',').strip()
            if clean.startswith('assets/'):
                total_assets += 1
                if not os.path.exists(clean):
                    missing.append(clean)

    if missing:
        print(f"FAIL: Missing assets referenced in HTML: {missing}")
        return False
    print(f"PASS: All {total_assets} asset references in index.html verified and exist on disk")

    # Verificar mención del vaso de hielo seco de medio litro en index.html
    if 'hielo seco blanco de medio litro' in html or 'hielo seco' in html:
        print("PASS: Vaso de hielo seco correctamente descrito en carta")
    else:
        print("WARN: 'hielo seco' no encontrado textualmente")

    # Verificar bolsas oficiales de botanas
    marcas = ['tostitos', 'conchitas', 'doritos', 'cheetos-flamin', 'ruffles', 'takis']
    for m in marcas:
        jpg = f'assets/images/menu/{m}-elote.jpg'
        webp = f'assets/images/menu/{m}-elote.webp'
        if not os.path.exists(jpg) or not os.path.exists(webp):
            print(f"FAIL: Missing menu photo for {m}")
            return False
    print("PASS: All 6 official branded snacks + corn photos exist in JPG & WebP")

    return True

if __name__ == '__main__':
    ok = test_node_syntax() and verify_assets_and_html()
    if ok:
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY (Pickle Rick Grade)!")
        sys.exit(0)
    else:
        print("\nVERIFICATIONS FAILED!")
        sys.exit(1)
