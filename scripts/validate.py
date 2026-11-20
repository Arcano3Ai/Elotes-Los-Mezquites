import os
import json
import re

print("=== 1. Validando sintaxis JSON-LD y Schema.org ===")
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
for i, match in enumerate(json_ld_matches):
    try:
        data = json.loads(match.strip())
        print(f"JSON-LD #{i+1} válido: Type={data.get('@type')}, Name={data.get('name')}")
        assert data.get("@type") == "Restaurant"
        assert "telephone" in data
        assert "address" in data
        print("Campos obligatorios de Schema.org Restaurant verificados con éxito.")
    except Exception as e:
        print(f"ERROR en JSON-LD #{i+1}:", e)
        raise e

print("\n=== 2. Validando OpenGraph y peso de imagen ===")
og_image_match = re.search(r'<meta property="og:image" content="(.*?)">', content)
if og_image_match:
    og_url = og_image_match.group(1)
    print("og:image meta:", og_url)
    assert og_url.startswith("https://"), "og:image debe ser URL absoluta https://"
    local_img = "assets/images/og-image.jpg"
    size_kb = os.path.getsize(local_img) / 1024
    print(f"Peso de {local_img}: {size_kb:.2f} KB")
    assert size_kb < 300, f"og:image excede 300KB ({size_kb} KB)"
    print("Cumple regla OpenGraph < 300KB: OK")

print("\n=== 3. Validando existencia de recursos enlazados en index.html ===")
srcs = re.findall(r'src=["\'](assets/[^"\']+)["\']', content)
hrefs = re.findall(r'href=["\'](assets/[^"\']+)["\']', content)
srcsets = re.findall(r'srcset=["\'](assets/[^"\']+)["\']', content)
data_photos = re.findall(r'data-photo=["\'](assets/[^"\']+)["\']', content)

all_assets = sorted(list(set(srcs + hrefs + srcsets + data_photos)))
missing = []
for asset in all_assets:
    if not os.path.exists(asset):
        missing.append(asset)
    else:
        print(f"Recurso OK: {asset}")

if missing:
    print("ERROR - FALTAN RECURSOS:", missing)
    exit(1)
else:
    print(f"\n¡Todos los {len(all_assets)} recursos locales enlazados existen correctamente!")

print("\n=== 4. Validando consistencia NAP, precios y requisitos ===")
assert "Morelos 654" in content, "Dirección Morelos 654 debe estar en el HTML"
assert "Agua Fría, Apodaca" in content, "Agua Fría, Apodaca debe estar en el HTML"
assert "81 2191 2778" in content, "Teléfono 81 2191 2778 debe estar en el HTML"
assert "528121912778" in content, "WhatsApp wa.me debe tener el número correcto"
assert "Entre mezquites sabe mejor" in content, "Nuevo slogan oficial debe estar presente"
assert "$50" in content, "Precio $50 para Elotes Tradicionales debe estar presente"
assert "$45" in content, "Precio $45 para Vaso Chico debe estar presente"
assert "$60" in content, "Precio $60 para Vaso Mediano debe estar presente"
assert "$85" in content, "Precio $85 para Especiales debe estar presente"
assert "$30" in content, "Precio $30 para Refrescos debe estar presente"
assert "$20" in content, "Precio $20 para Agua Natural debe estar presente"
print("Validación NAP, de marca y precios oficiales completada con éxito 100%.")
