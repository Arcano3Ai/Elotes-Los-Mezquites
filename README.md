# 🌽 Elotes Los Mezquites — Landing Page Oficial

> *"Entre mezquites sabe mejor. El sabor de siempre, en un lugar para disfrutar."*

Landing page oficial de **Elotes Los Mezquites**, un espacio gastronómico mexicano en Agua Fría, Apodaca, Nuevo León. Diseñada con una dirección de arte cinematográfica inspirada en la convivencia nocturna bajo los árboles mezquites, las fogatas, la madera rústica y el maíz artesanal.

---

## 🚗 Configurador de Pedidos Express ("Para recoger de pasada")

El sitio cuenta con un **módulo interactivo de pedidos en línea** pensado especialmente para clientes que van de camino y desean que su pedido esté listo al llegar:

1. **Selección de antojo principal:** Elotes asados/cocidos ($50), Vasos ($45/$60) o Especiales con botanas clásicas regias ($85).
2. **Nivel de picante & Preparación:** Sin chile, chile del que pica / del que no pica, limón y sal.
3. **Extras artesanales:** Mayonesa, crema, queso amarillo fundido, queso blanco rallado y mantequilla.
4. **Bebidas frías:** Refrescos y agua purificada ($20 - $30).
5. **Cálculo reactivo en tiempo real:** Desglose visual instantáneo de precios y total.
6. **Métodos de pago flexibles:**
   - **Mercado Pago (Checkout Pro):** Tarjetas de débito/crédito, transferencias y saldo digital.
   - **Pago en efectivo / al recoger:** Pedido enviado directamente a la cocina por WhatsApp con folio único generado `#LMZ-XXXX`.

---

## 💳 Arquitectura de Pagos Segura (Mercado Pago Backend)

Siguiendo las mejores prácticas de ingeniería de software senior:
* **Cero exposición de credenciales privadas:** Ninguna llave `APP_USR-` o token privado vive en el cliente.
* **Precios canónicos validados en backend:** El endpoint `/api/create-preference` valida y recalcula el monto final contra la lista de precios oficial para impedir adulteraciones desde el frontend.
* **Webhooks seguros con validación criptográfica:** El endpoint `/api/webhooks/mercadopago` valida la firma `x-signature` mediante HMAC-SHA256 y previene cobros o duplicados mediante un registro de idempotencia en memoria.

---

## 📱 Optimización Mobile-First & OpenGraph para WhatsApp

* **Barra Fija Inferior (Mobile Sticky Bar):** Diseñada específicamente para pantallas móviles, con acceso rápido a "🚗 ORDENAR AHORA" y "📍 CÓMO LLEGAR".
* **Previsualización OpenGraph enriquecida:** La imagen de previsualización para WhatsApp y redes sociales (`assets/images/og-image.jpg`) incorpora el logotipo oficial de alta resolución, slogan y ubicación, optimizada a **65.84 KB** (cumple estrictamente el límite `< 300KB` para carga inmediata en dispositivos móviles).

---

## 📋 Menú Oficial con Precios

### 01. 🌽 ELOTES TRADICIONALES
| Producto | Descripción | Precio |
|---|---|---|
| **Elote asado** | Elote a las brasas, con limón, sal y chile al gusto. | **$50** |
| **Elote cocido** | Elote tradicional preparado al gusto. | **$50** |

### 02. 🥣 ELOTE EN VASO
| Presentación | Descripción | Precio |
|---|---|---|
| **Vaso chico** | Porción individual con crema, queso y chile al gusto. | **$45** |
| **Vaso mediano** | Abundante grano tierno, caldo aromático y aderezos. | **$60** |

### 03. 🔥 LOS MEZQUITES ESPECIALES
| Producto | Descripción | Precio |
|---|---|---|
| **Tostitos con elote** | Tostitos preparados con esquites, crema, queso y salsa. | **$85** |
| **Conchitas con elote** | Conchitas bañadas con elote, crema y queso *(clásico regio)*. | **$85** |
| **Doritos con elote** | Doritos Nacho con elote preparado. | **$85** |
| **Cheetos con elote** | Cheetos Flamin' Hot con esquites y aderezos. | **$85** |
| **Ruffles con elote** | Ruffles con elote, queso y crema. | **$85** |
| **Takis con elote** | Takis Fuego con esquites y salsa. | **$85** |

### 04. 🥤 BEBIDAS & EXTRAS
* **Coca-Cola:** $30
* **Coca-Cola sin azúcar:** $30
* **Sprite:** $30
* **Fanta:** $30
* **Agua natural:** $20
* **Personaliza tu antojo (Extras):** Mayonesa, Crema, Queso amarillo fundido, Queso blanco rallado, Mantequilla, Limón.

---

## 📸 Fotografías Reales del Establecimiento

El sitio integra las **fotografías reales del lugar** tomadas en Agua Fría, Apodaca, procesadas y optimizadas mediante un pipeline de calibración fotográfica:
* **Hero Limpio:** Fondo a pantalla completa sin opacidades artificiales ni textos duplicados sobre la toma.
* **Grandes Árboles Mezquites:** Follaje y sombra natural del terreno.
* **Mesas al Aire Libre:** Bancos y mesas de madera rústica para convivencia campestre.
* **Espacio Abierto y Tradicional:** Instalaciones auténticas del establecimiento sin elementos ficticios.
* **Visualizador Lightbox:** Las fotos de la carta y del espacio pueden ampliarse en alta resolución con un solo clic.

---

## 🎨 Identidad Visual & Paleta Cromática

| Color | Hex | Aplicación |
|---|---|---|
| **Café carbón** | `#24160F` | Fondos oscuros principales, ambientación nocturna |
| **Madera oscura** | `#382116` | Tarjetas de contenido, secciones intermedias |
| **Ámbar** | `#D99124` | Botones de acción, destellos de fuego |
| **Amarillo maíz** | `#F4B52D` | Títulos destacados, insignias, acentos |
| **Crema** | `#F5E8CE` | Tipografía principal y de lectura |
| **Verde mezquite**| `#596442` | Detalles botánicos e iconografía |
| **Terracota** | `#A94D27` | Divisiones rústicas y matices artesanales |

---

## 📁 Estructura del Proyecto

```text
Elotes-Los-Mezquites/
├── index.html            # Estructura semántica, OpenGraph, Schema.org y Configurador
├── styles.css            # Estilos CSS3, configurador, sticky bar y diseño responsive
├── app.js                # Lógica interactiva del configurador, Lightbox y Toast
├── package.json          # Metadatos del proyecto y scripts npm
├── .env.example          # Plantilla para credenciales de Mercado Pago
├── server/
│   └── app.js            # Servidor API para checkout y webhooks seguros de Mercado Pago
├── assets/
│   ├── icons/
│   │   ├── logo.svg      # Logotipo vectorial de la marca
│   │   └── favicon.svg   # Favicon para el navegador
│   └── images/
│       ├── menu/         # Fotografías de los platillos y botanas del menú
│       ├── lugar/        # Fotografías reales mejoradas del lugar
│       ├── hero-mezquites.webp / .jpg   # Fotografía hero limpia
│       └── og-image.jpg                 # Imagen OpenGraph optimizada con logo (< 300KB)
└── scripts/
    ├── enhance_photos.py # Pipeline de mejora fotográfica digital
    ├── process_assets.py # Compresión y optimización de imágenes
    ├── generate_logo_og.py # Generador de OpenGraph con logo oficial
    └── validate.py       # Suite de verificación técnica y SEO
```

---

## 🚀 Puesta en Marcha & Despliegue

### 1. Despliegue Estático (GitHub Pages / Vercel / Netlify)
El frontend funciona de forma 100% autónoma. Cuando no hay backend de Mercado Pago configurado, el configurador genera un **ticket estructurado con folio automático** y lo transfiere a WhatsApp para atención inmediata en cocina.

1. Ve a los **Settings** del repositorio en GitHub.
2. En la sección **Pages**, selecciona la rama `main` y la carpeta `/ (root)`.
3. Guarda los cambios. Tu sitio estará disponible en minutos en:
   `https://arcano3ai.github.io/Elotes-Los-Mezquites/`

### 2. Ejecutar Servidor Backend Localmente con Mercado Pago
```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Editar .env e ingresar MP_ACCESS_TOKEN y MP_WEBHOOK_SECRET

# 2. Iniciar servidor
npm start
# El servidor estará escuchando en http://localhost:3000
```

---

## 📍 Información del Establecimiento (NAP)

* **Nombre:** Elotes Los Mezquites
* **Dirección:** Morelos 654, Agua Fría, Apodaca, Nuevo León, México
* **Teléfono:** 81 2191 2778
* **WhatsApp:** [Chatear por WhatsApp](https://wa.me/528121912778?text=%C2%A1Hola!%20Quiero%20informaci%C3%B3n%20sobre%20Elotes%20Los%20Mezquites.)

---

© 2026 Elotes Los Mezquites. Desarrollado con los más altos estándares por [Arcano Solutions](https://github.com/Arcano3Ai).
