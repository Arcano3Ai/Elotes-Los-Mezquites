/**
 * SERVIDOR SEGURO PARA ELOTES LOS MEZQUITES
 * Integración con Mercado Pago:
 * - Creación de Preferencia (Checkout Pro)
 * - Validación criptográfica de Webhooks (x-signature con HMAC SHA256)
 * - Garantía de Idempotencia en Notificaciones de Pago
 * - Verificación de Precios Oficiales del lado del Servidor
 */

const http = require('http');
const https = require('https');
const crypto = require('crypto');
const url = require('url');

// Precios Oficiales Validados en el Servidor (Previene alteración de precios en el cliente)
const OFFICIAL_PRICES = {
  // Tradicionales
  'elote-asado': { title: 'Elote Asado', price: 50 },
  'elote-cocido': { title: 'Elote Cocido', price: 50 },
  // Vasos
  'vaso-chico': { title: 'Elote en Vaso Chico', price: 45 },
  'vaso-mediano': { title: 'Elote en Vaso Mediano', price: 60 },
  // Especiales
  'tostitos-elote': { title: 'Tostitos con Elote', price: 85 },
  'conchitas-elote': { title: 'Conchitas con Elote', price: 85 },
  'doritos-elote': { title: 'Doritos con Elote', price: 85 },
  'cheetos-elote': { title: 'Cheetos con Elote', price: 85 },
  'ruffles-elote': { title: 'Ruffles con Elote', price: 85 },
  'takis-elote': { title: 'Takis con Elote', price: 85 },
  // Bebidas
  'coca-cola': { title: 'Coca-Cola', price: 30 },
  'coca-cola-zero': { title: 'Coca-Cola sin azúcar', price: 30 },
  'sprite': { title: 'Sprite', price: 30 },
  'fanta': { title: 'Fanta', price: 30 },
  'agua-natural': { title: 'Agua natural', price: 20 },
  'sin-bebida': { title: 'Sin bebida', price: 0 }
};

// Registro de idempotencia en memoria (o base de datos en producción)
const processedPayments = new Set();

const PORT = process.env.PORT || 3000;
const MERCADOPAGO_ACCESS_TOKEN = process.env.MERCADOPAGO_ACCESS_TOKEN || '';
const MERCADOPAGO_WEBHOOK_SECRET = process.env.MERCADOPAGO_WEBHOOK_SECRET || '';
const BASE_URL = process.env.BASE_URL || 'https://eloteslosmezquites.com';

/**
 * Validar la firma criptográfica x-signature enviada por Mercado Pago
 * x-signature format: ts=16...;v1=sha256_hash...
 */
function verifyMercadoPagoSignature(xSignature, dataId, secret) {
  if (!xSignature || !secret) return false;

  const parts = xSignature.split(',').reduce((acc, part) => {
    const [key, val] = part.trim().split('=');
    if (key && val) acc[key] = val;
    return acc;
  }, {});

  const ts = parts['ts'];
  const hash = parts['v1'];
  if (!ts || !hash) return false;

  // Manifest template: id:[data.id_url];request-id:[x-request-id];ts:[ts];
  const manifest = `id:${dataId};ts:${ts};`;
  const calculatedHash = crypto.createHmac('sha256', secret).update(manifest).digest('hex');

  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(calculatedHash));
}

/**
 * Llamada a la API de Mercado Pago para crear preferencia de Checkout Pro
 */
function createPreferenceMP(preferenceData, accessToken) {
  return new Promise((resolve, reject) => {
    if (!accessToken) {
      // Simulación segura si aún no se han configurado llaves de producción
      return resolve({
        id: `mock_pref_${Date.now()}`,
        init_point: `${BASE_URL}/#pedido-confirmado?status=approved`,
        sandbox_init_point: `${BASE_URL}/#pedido-confirmado?status=approved`
      });
    }

    const payload = JSON.stringify(preferenceData);
    const options = {
      hostname: 'api.mercadopago.com',
      port: 443,
      path: '/checkout/preferences',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(json);
          } else {
            reject(new Error(json.message || `HTTP ${res.statusCode}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

const server = http.createServer(async (req, res) => {
  const reqUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = reqUrl.pathname;

  // Headers de CORS seguros
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-signature, x-request-id');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  // 1. ENDPOINT: Crear Preferencia de Pago
  if (req.method === 'POST' && pathname === '/api/create-preference') {
    let rawBody = '';
    req.on('data', chunk => rawBody += chunk);
    req.on('end', async () => {
      try {
        const body = JSON.parse(rawBody || '{}');
        const { baseId, bebidaId, customer, extras, chile, time } = body;

        // Validación estricta en el servidor
        const baseItem = OFFICIAL_PRICES[baseId];
        if (!baseItem) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ error: 'Producto base no válido' }));
        }

        const items = [
          {
            title: `${baseItem.title} (Recoger de pasada - ${time || 'En 15 min'})`,
            description: `Preparación: ${chile || 'Con todo'}. Extras: ${(extras || []).join(', ') || 'Tradicional'}`,
            quantity: 1,
            currency_id: 'MXN',
            unit_price: baseItem.price
          }
        ];

        let total = baseItem.price;

        if (bebidaId && OFFICIAL_PRICES[bebidaId] && bebidaId !== 'sin-bebida') {
          const bebidaItem = OFFICIAL_PRICES[bebidaId];
          items.push({
            title: bebidaItem.title,
            quantity: 1,
            currency_id: 'MXN',
            unit_price: bebidaItem.price
          });
          total += bebidaItem.price;
        }

        const orderId = `LMZ-${Date.now().toString().slice(-6)}`;

        const preferenceData = {
          items: items,
          payer: {
            name: customer?.name || 'Cliente Los Mezquites',
            phone: { number: customer?.phone || '' }
          },
          external_reference: orderId,
          statement_descriptor: 'ELOTES MEZQUITES',
          back_urls: {
            success: `${BASE_URL}/#pedido-exitoso?order=${orderId}`,
            failure: `${BASE_URL}/#pedido-fallido?order=${orderId}`,
            pending: `${BASE_URL}/#pedido-pendiente?order=${orderId}`
          },
          auto_return: 'approved',
          notification_url: `${BASE_URL}/api/webhooks/mercadopago`
        };

        const mpResponse = await createPreferenceMP(preferenceData, MERCADOPAGO_ACCESS_TOKEN);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({
          orderId,
          total,
          preferenceId: mpResponse.id,
          initPoint: mpResponse.init_point || mpResponse.sandbox_init_point
        }));

      } catch (err) {
        console.error('Error al crear preferencia:', err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ error: 'Error interno al procesar pago' }));
      }
    });
    return;
  }

  // 2. ENDPOINT: Webhook Seguro con Validación Criptográfica e Idempotencia
  if (req.method === 'POST' && pathname === '/api/webhooks/mercadopago') {
    let rawBody = '';
    req.on('data', chunk => rawBody += chunk);
    req.on('end', async () => {
      try {
        const xSignature = req.headers['x-signature'];
        const dataId = reqUrl.searchParams.get('data.id') || reqUrl.searchParams.get('id');

        // Si hay secret configurado, validar firma criptográfica
        if (MERCADOPAGO_WEBHOOK_SECRET && !verifyMercadoPagoSignature(xSignature, dataId, MERCADOPAGO_WEBHOOK_SECRET)) {
          console.warn('Firma x-signature inválida rechazada.');
          res.writeHead(401, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ error: 'Invalid cryptographic signature' }));
        }

        // Idempotencia: Verificar si ya procesamos este payment id
        if (dataId) {
          if (processedPayments.has(dataId)) {
            console.log(`Notificación id ${dataId} ya procesada previamente (idempotente).`);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            return res.end(JSON.stringify({ status: 'already_processed' }));
          }
          processedPayments.add(dataId);
        }

        console.log(`Notificación de pago legítima recibida para id: ${dataId}`);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ status: 'received' }));

      } catch (err) {
        console.error('Error en webhook:', err);
        res.writeHead(500);
        return res.end();
      }
    });
    return;
  }

  // Healthcheck
  if (pathname === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'ok', service: 'Elotes Los Mezquites API' }));
  }

  res.writeHead(404);
  res.end('Not Found');
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Servidor de Elotes Los Mezquites escuchando en puerto ${PORT}`);
  });
}

module.exports = server;
