/**
 * ELOTES LOS MEZQUITES - APP.JS
 * Lógica interactiva:
 * - Header blur on scroll
 * - Menú móvil off-canvas
 * - Scrollspy nativo con IntersectionObserver
 * - Lightbox modal para galería gastronómica
 * - Copiado de dirección al portapapeles con Toast
 * - Animaciones reveal-on-scroll
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. HEADER SCROLL STATE
  const header = document.getElementById('header');
  const updateHeaderScroll = () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', updateHeaderScroll, { passive: true });
  updateHeaderScroll();

  // 2. MENÚ MÓVIL
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileClose = document.getElementById('mobileClose');
  const mobileLinks = document.querySelectorAll('.mobile-link, .mobile-cta');

  const openMobileMenu = () => {
    mobileMenu.classList.add('active');
    mobileMenu.setAttribute('aria-hidden', 'false');
    mobileToggle.setAttribute('aria-expanded', 'true');
    mobileToggle.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closeMobileMenu = () => {
    mobileMenu.classList.remove('active');
    mobileMenu.setAttribute('aria-hidden', 'true');
    mobileToggle.setAttribute('aria-expanded', 'false');
    mobileToggle.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.contains('active');
      if (isOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    if (mobileClose) {
      mobileClose.addEventListener('click', closeMobileMenu);
    }

    mobileLinks.forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });

    // Cerrar si se hace click fuera del contenedor interno
    mobileMenu.addEventListener('click', (e) => {
      if (e.target === mobileMenu) {
        closeMobileMenu();
      }
    });
  }

  // 3. SCROLLSPY (ACTUALIZAR ENLACE ACTIVO SEGÚN LA SECCIÓN)
  const navLinks = document.querySelectorAll('.nav-desktop .nav-link');
  const sections = document.querySelectorAll('section[id]');

  const sectionObserverOptions = {
    root: null,
    rootMargin: '-30% 0px -60% 0px',
    threshold: 0
  };

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, sectionObserverOptions);

  sections.forEach(section => sectionObserver.observe(section));

  // 4. ANIMACIONES REVEAL-ON-SCROLL
  const reveals = document.querySelectorAll('.reveal-on-scroll');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  reveals.forEach(el => revealObserver.observe(el));

  // 5. LIGHTBOX MODAL PARA GALERÍA GASTRONÓMICA
  const lightboxModal = document.getElementById('lightboxModal');
  const lightboxBackdrop = document.getElementById('lightboxBackdrop');
  const lightboxClose = document.getElementById('lightboxClose');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const photoButtons = document.querySelectorAll('.btn-view-photo');

  const openLightbox = (imgSrc, captionText) => {
    lightboxImg.src = imgSrc;
    lightboxImg.alt = captionText;
    lightboxCaption.textContent = captionText;
    lightboxModal.classList.add('active');
    lightboxModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    lightboxModal.classList.remove('active');
    lightboxModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    setTimeout(() => {
      lightboxImg.src = '';
      lightboxCaption.textContent = '';
    }, 200);
  };

  photoButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const photo = btn.getAttribute('data-photo');
      const caption = btn.getAttribute('data-caption');
      if (photo) openLightbox(photo, caption);
    });
  });

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightboxBackdrop) lightboxBackdrop.addEventListener('click', closeLightbox);

  // 6. TECLA ESCAPE PARA CERRAR MODALES
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (lightboxModal && lightboxModal.classList.contains('active')) {
        closeLightbox();
      }
      if (mobileMenu && mobileMenu.classList.contains('active')) {
        closeMobileMenu();
      }
    }
  });

  // 7. COPIAR DIRECCIÓN AL PORTAPAPELES
  const btnCopyAddress = document.getElementById('btnCopyAddress');
  const copyBtnText = document.getElementById('copyBtnText');
  const toastNotification = document.getElementById('toastNotification');

  const showToast = (message) => {
    if (!toastNotification) return;
    const msgEl = toastNotification.querySelector('.toast-msg');
    if (msgEl) msgEl.textContent = message;
    toastNotification.classList.add('show');
    setTimeout(() => {
      toastNotification.classList.remove('show');
    }, 3200);
  };

  if (btnCopyAddress) {
    const addressToCopy = 'Morelos 654, Agua Fría, Apodaca, Nuevo León, México';
    btnCopyAddress.addEventListener('click', async () => {
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(addressToCopy);
        } else {
          // Fallback para entornos no-https o navegadores antiguos
          const textArea = document.createElement('textarea');
          textArea.value = addressToCopy;
          textArea.style.position = 'fixed';
          textArea.style.left = '-999999px';
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          document.execCommand('copy');
          textArea.remove();
        }

        if (copyBtnText) copyBtnText.textContent = '¡Dirección copiada!';
        showToast('Dirección copiada al portapapeles');

        setTimeout(() => {
          if (copyBtnText) copyBtnText.textContent = 'Copiar dirección';
        }, 2500);
      } catch (err) {
        console.error('Error al copiar dirección:', err);
        showToast('Morelos 654, Agua Fría, Apodaca');
      }
    });
  }

  // 8. CONFIGURADOR DE PEDIDOS "PARA RECOGER DE PASADA"
  const orderForm = document.getElementById('orderForm');
  if (orderForm) {
    const baseRadios = orderForm.querySelectorAll('input[name="baseProduct"]');
    const bebidaRadios = orderForm.querySelectorAll('input[name="bebidaProduct"]');
    const paymentRadios = orderForm.querySelectorAll('input[name="paymentMethod"]');
    
    const summaryBaseName = document.getElementById('summaryBaseName');
    const summaryBasePrice = document.getElementById('summaryBasePrice');
    const summaryBebidaRow = document.getElementById('summaryBebidaRow');
    const summaryBebidaName = document.getElementById('summaryBebidaName');
    const summaryBebidaPrice = document.getElementById('summaryBebidaPrice');
    const summaryTotalPrice = document.getElementById('summaryTotalPrice');
    const btnSubmitText = document.getElementById('btnSubmitText');

    let currentBase = { id: 'elote-asado', name: 'Elote Asado', price: 50 };
    let currentBebida = { id: 'sin-bebida', name: 'Sin bebida', price: 0 };
    let currentPayment = 'mercadopago';

    const updateCalculations = () => {
      // 1. Base seleccionada
      const checkedBase = orderForm.querySelector('input[name="baseProduct"]:checked');
      if (checkedBase) {
        currentBase = {
          id: checkedBase.value,
          name: checkedBase.getAttribute('data-name'),
          price: parseInt(checkedBase.getAttribute('data-price') || '0', 10)
        };
      }

      // 2. Bebida seleccionada
      const checkedBebida = orderForm.querySelector('input[name="bebidaProduct"]:checked');
      if (checkedBebida) {
        currentBebida = {
          id: checkedBebida.value,
          name: checkedBebida.getAttribute('data-name'),
          price: parseInt(checkedBebida.getAttribute('data-price') || '0', 10)
        };
      }

      // 3. Método de pago
      const checkedPayment = orderForm.querySelector('input[name="paymentMethod"]:checked');
      if (checkedPayment) {
        currentPayment = checkedPayment.value;
      }

      // 4. Actualizar interfaz de resumen
      const total = currentBase.price + currentBebida.price;
      if (summaryBaseName) summaryBaseName.textContent = currentBase.name;
      if (summaryBasePrice) summaryBasePrice.textContent = `$${currentBase.price} MXN`;

      if (summaryBebidaRow) {
        if (currentBebida.price > 0) {
          summaryBebidaRow.style.display = 'flex';
          if (summaryBebidaName) summaryBebidaName.textContent = currentBebida.name;
          if (summaryBebidaPrice) summaryBebidaPrice.textContent = `$${currentBebida.price} MXN`;
        } else {
          summaryBebidaRow.style.display = 'none';
        }
      }

      if (summaryTotalPrice) summaryTotalPrice.textContent = `$${total} MXN`;
      if (btnSubmitText) {
        if (currentPayment === 'mercadopago') {
          btnSubmitText.textContent = `PAGAR CON MERCADO PAGO ($${total})`;
        } else {
          btnSubmitText.textContent = `CONFIRMAR Y PAGAR AL RECOGER ($${total})`;
        }
      }
    };

    baseRadios.forEach(r => r.addEventListener('change', updateCalculations));
    bebidaRadios.forEach(r => r.addEventListener('change', updateCalculations));
    paymentRadios.forEach(r => r.addEventListener('change', updateCalculations));
    updateCalculations();

    // Procesar envío del formulario
    orderForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const custName = document.getElementById('custName')?.value.trim();
      const custPhone = document.getElementById('custPhone')?.value.trim();
      const pickupTime = document.getElementById('pickupTime')?.value;
      const orderNotes = document.getElementById('orderNotes')?.value.trim();
      const checkedChile = orderForm.querySelector('input[name="chileLevel"]:checked')?.value || 'Normal';

      const checkedExtras = [];
      orderForm.querySelectorAll('input[name="extras"]:checked').forEach(cb => {
        checkedExtras.push(cb.value);
      });

      if (!custName || !custPhone) {
        alert('Por favor ingresa tu nombre y teléfono para tener tu pedido listo.');
        return;
      }

      const total = currentBase.price + currentBebida.price;
      const orderId = `LMZ-${Math.floor(1000 + Math.random() * 9000)}`;

      // Construir mensaje estructurado para WhatsApp
      const waMsgLines = [
        `¡Hola Elotes Los Mezquites! Quiero hacer un pedido *PARA RECOGER DE PASADA*:`,
        ``,
        `📋 *Folio de Pedido:* #${orderId}`,
        `👤 *Cliente:* ${custName}`,
        `📞 *Teléfono:* ${custPhone}`,
        `⏱️ *Tiempo estimado de llegada:* ${pickupTime}`,
        ``,
        `🌽 *Antojo Principal:* ${currentBase.name} ($${currentBase.price} MXN)`,
        `🌶️ *Nivel de chile:* ${checkedChile}`,
        `🧀 *Ingredientes:* ${checkedExtras.join(', ') || 'Tradicional'}`,
        orderNotes ? `📝 *Notas especiales:* ${orderNotes}` : null,
        currentBebida.price > 0 ? `🥤 *Bebida:* ${currentBebida.name} ($${currentBebida.price} MXN)` : null,
        ``,
        `💳 *Método de pago:* ${currentPayment === 'mercadopago' ? 'Mercado Pago (En línea)' : 'Pagar en efectivo al llegar'}`,
        `💰 *TOTAL A PAGAR:* $${total} MXN`,
        ``,
        `_Favor de confirmar que recibieron mi orden para tenerla calientita. ¡Gracias!_`
      ].filter(line => line !== null);

      const encodedWaMsg = encodeURIComponent(waMsgLines.join('\n'));
      const waUrl = `https://wa.me/528121912778?text=${encodedWaMsg}`;

      // Si seleccionó Mercado Pago, intentar generar preferencia en el backend
      if (currentPayment === 'mercadopago') {
        const btnSubmit = document.getElementById('btnSubmitOrder');
        const originalText = btnSubmitText.textContent;
        btnSubmitText.textContent = 'Conectando con Mercado Pago...';

        try {
          const res = await fetch('/api/create-preference', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              baseId: currentBase.id,
              bebidaId: currentBebida.id,
              customer: { name: custName, phone: custPhone },
              extras: checkedExtras,
              chile: checkedChile,
              time: pickupTime
            })
          });

          if (res.ok) {
            const data = await res.json();
            if (data.initPoint) {
              // Notificar al cliente y abrir pasarela
              showToast(`Orden #${orderId} creada. Abriendo Mercado Pago...`);
              setTimeout(() => {
                window.location.href = data.initPoint;
              }, 800);
              return;
            }
          }
        } catch (err) {
          console.warn('Backend serverless no disponible en modo estático, usando checkout asistido por WhatsApp:', err);
        }

        // Fallback: Si no hay servidor activo en localhost, enviar orden por WhatsApp para pago con link de MP
        btnSubmitText.textContent = originalText;
        showToast(`Orden #${orderId} registrada con éxito`);
        setTimeout(() => {
          window.open(waUrl, '_blank');
        }, 600);
      } else {
        // Pago en efectivo / terminal al llegar
        showToast(`¡Orden #${orderId} enviada a cocina!`);
        setTimeout(() => {
          window.open(waUrl, '_blank');
        }, 600);
      }
    });
  }
});
