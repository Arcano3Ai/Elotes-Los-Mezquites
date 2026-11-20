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

  // 8. CONFIGURADOR Y CHECKOUT UNIFICADO DESDE EL MENÚ
  const orderForm = document.getElementById('orderForm');
  if (orderForm) {
    const paymentRadios = orderForm.querySelectorAll('input[name="paymentMethod"]');
    
    // Elementos de la comanda (carrito)
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const cartCountBadge = document.getElementById('cartCountBadge');
    const btnClearCart = document.getElementById('btnClearCart');
    const summaryItemsList = document.getElementById('summaryItemsList');
    const summaryTotalPrice = document.getElementById('summaryTotalPrice');
    const btnSubmitText = document.getElementById('btnSubmitText');
    const stickyBarCount = document.getElementById('stickyBarCount');

    // Modal de personalización de producto
    const customizerModal = document.getElementById('customizerModal');
    const customizerBackdrop = document.getElementById('customizerBackdrop');
    const customizerClose = document.getElementById('customizerClose');
    const customizerTitle = document.getElementById('customizerTitle');
    const customizerPriceBadge = document.getElementById('customizerPriceBadge');
    const customizerNotes = document.getElementById('customizerNotes');
    const mBtnQtyMinus = document.getElementById('mBtnQtyMinus');
    const mBtnQtyPlus = document.getElementById('mBtnQtyPlus');
    const mQtyDisplay = document.getElementById('mQtyDisplay');
    const mBtnConfirmAdd = document.getElementById('mBtnConfirmAdd');
    const mBtnAddText = document.getElementById('mBtnAddText');

    // Botones de acción en la carta
    const openCustomizerButtons = document.querySelectorAll('.btn-open-customizer');
    const addBebidaButtons = document.querySelectorAll('.btn-add-bebida');

    // Estado del carrito y modal
    let orderCart = [];
    let currentPayment = 'mercadopago';
    let modalSelectedProduct = null;
    let modalQty = 1;

    // Abrir Modal de Personalización
    const openCustomizer = (product) => {
      modalSelectedProduct = product;
      modalQty = 1;

      if (customizerTitle) customizerTitle.textContent = product.name;
      if (customizerPriceBadge) customizerPriceBadge.textContent = `$${product.price} MXN`;
      if (mQtyDisplay) mQtyDisplay.textContent = '1';
      if (customizerNotes) customizerNotes.value = '';

      // Resetear chile a Normal
      const normalChile = customizerModal.querySelector('input[name="mChile"][value="Normal"]');
      if (normalChile) normalChile.checked = true;

      // Resetear extras a todos marcados por defecto
      customizerModal.querySelectorAll('input[name="mExtras"]').forEach(cb => {
        cb.checked = true;
      });

      updateModalAddBtn();

      customizerModal.classList.add('active');
      customizerModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    };

    // Cerrar Modal de Personalización
    const closeCustomizer = () => {
      if (!customizerModal) return;
      customizerModal.classList.remove('active');
      customizerModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      modalSelectedProduct = null;
    };

    const updateModalAddBtn = () => {
      if (!modalSelectedProduct || !mBtnAddText) return;
      const subtotal = modalSelectedProduct.price * modalQty;
      mBtnAddText.textContent = `AGREGAR AL PEDIDO ($${subtotal} MXN)`;
    };

    // Controles de cantidad en el modal
    if (mBtnQtyMinus && mBtnQtyPlus && mQtyDisplay) {
      mBtnQtyMinus.addEventListener('click', () => {
        if (modalQty > 1) {
          modalQty--;
          mQtyDisplay.textContent = modalQty;
          updateModalAddBtn();
        }
      });

      mBtnQtyPlus.addEventListener('click', () => {
        if (modalQty < 50) {
          modalQty++;
          mQtyDisplay.textContent = modalQty;
          updateModalAddBtn();
        }
      });
    }

    if (customizerClose) customizerClose.addEventListener('click', closeCustomizer);
    if (customizerBackdrop) customizerBackdrop.addEventListener('click', closeCustomizer);

    // Conectar botones de la carta para abrir el modal
    openCustomizerButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const id = btn.getAttribute('data-id');
        const name = btn.getAttribute('data-name');
        const price = parseInt(btn.getAttribute('data-price') || '0', 10);
        openCustomizer({ id, name, price });
      });
    });

    // Confirmar agregar producto desde el modal
    if (mBtnConfirmAdd) {
      mBtnConfirmAdd.addEventListener('click', () => {
        if (!modalSelectedProduct) return;

        const checkedChile = customizerModal.querySelector('input[name="mChile"]:checked')?.value || 'Normal';
        const checkedExtras = [];
        customizerModal.querySelectorAll('input[name="mExtras"]:checked').forEach(cb => {
          checkedExtras.push(cb.value);
        });
        const notes = customizerNotes ? customizerNotes.value.trim() : '';

        orderCart.push({
          id: modalSelectedProduct.id,
          name: modalSelectedProduct.name,
          price: modalSelectedProduct.price,
          quantity: modalQty,
          chile: checkedChile,
          extras: checkedExtras,
          notes: notes
        });

        showToast(`¡Agregado al pedido! (${modalQty}x ${modalSelectedProduct.name})`);
        closeCustomizer();
        renderCart();

        // Si es el primer producto, hacer scroll suave a la comanda
        const orderSection = document.getElementById('pedir');
        if (orderCart.length === 1 && orderSection) {
          setTimeout(() => {
            orderSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }, 350);
        }
      });
    }

    // Botones directos para agregar bebidas desde la carta
    addBebidaButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const id = btn.getAttribute('data-id');
        const name = btn.getAttribute('data-name');
        const price = parseInt(btn.getAttribute('data-price') || '0', 10);

        // Si ya está esa bebida en el carrito, incrementar cantidad
        const existing = orderCart.find(item => item.id === id);
        if (existing) {
          existing.quantity++;
        } else {
          orderCart.push({
            id: id,
            name: name,
            price: price,
            quantity: 1,
            chile: 'N/A',
            extras: [],
            notes: 'Bien fría'
          });
        }

        showToast(`¡Bebida agregada! (1x ${name})`);
        renderCart();
      });
    });

    // Renderizar comanda dinámica y calcular totales
    const renderCart = () => {
      // Método de pago
      const checkedPayment = orderForm.querySelector('input[name="paymentMethod"]:checked');
      if (checkedPayment) {
        currentPayment = checkedPayment.value;
      }

      let total = 0;
      let totalItemsCount = 0;

      if (orderCart.length === 0) {
        if (cartItemsContainer) {
          cartItemsContainer.innerHTML = `
            <div class="cart-empty-notice" style="padding: 1.8rem 1rem; text-align: center; color: var(--color-text-muted);">
              <p style="margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 600; color: #fff;">🛒 Tu comanda está vacía</p>
              <p style="margin: 0 0 1rem 0; font-size: 0.9rem;">Elige arriba en el menú tu elote, vaso o botana favorita y pulsa <strong>"Ordenar"</strong>.</p>
              <a href="#menu" class="btn btn-secondary" style="padding: 0.55rem 1.25rem; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.4rem;">
                <span>🌽 Ver la carta completa</span>
              </a>
            </div>
          `;
        }

        if (cartCountBadge) cartCountBadge.textContent = '0 productos';
        if (summaryItemsList) {
          summaryItemsList.innerHTML = `
            <div class="summary-row" style="color: var(--color-text-muted);">
              <span>Aún no hay productos</span>
              <span class="summary-val">$0 MXN</span>
            </div>
          `;
        }

        if (summaryTotalPrice) summaryTotalPrice.textContent = '$0 MXN';
        if (stickyBarCount) stickyBarCount.textContent = '0 productos agregados';
        if (btnSubmitText) btnSubmitText.textContent = 'SELECCIONA PRODUCTOS DEL MENÚ';
        return;
      }

      // Si hay productos en el carrito
      if (cartItemsContainer) {
        cartItemsContainer.innerHTML = '';
      }

      let summaryHtml = '';

      orderCart.forEach((item, index) => {
        const itemSubtotal = item.price * item.quantity;
        total += itemSubtotal;
        totalItemsCount += item.quantity;

        // Fila en comanda
        if (cartItemsContainer) {
          const row = document.createElement('div');
          row.className = 'cart-item-row';
          row.innerHTML = `
            <div class="cart-item-info">
              <span class="cart-item-title"><strong>${item.quantity}x</strong> ${item.name}</span>
              <span class="cart-item-details">
                ${item.chile !== 'N/A' ? `🌶️ ${item.chile}` : ''}
                ${item.extras && item.extras.length > 0 ? ` • ${item.extras.join(', ')}` : ''}
                ${item.notes ? ` • <em>"${item.notes}"</em>` : ''}
              </span>
            </div>
            <div class="cart-item-price-wrap">
              <span class="cart-item-subtotal">$${itemSubtotal} MXN</span>
              <button type="button" class="btn-remove-item" data-index="${index}" title="Eliminar este producto" aria-label="Eliminar producto">
                ✕
              </button>
            </div>
          `;
          cartItemsContainer.appendChild(row);
        }

        // Fila en resumen de pago
        summaryHtml += `
          <div class="summary-row">
            <span>${item.quantity}x ${item.name}</span>
            <span class="summary-val">$${itemSubtotal} MXN</span>
          </div>
        `;
      });

      // Listeners de eliminación
      if (cartItemsContainer) {
        const removeButtons = cartItemsContainer.querySelectorAll('.btn-remove-item');
        removeButtons.forEach(btn => {
          btn.addEventListener('click', (e) => {
            const idx = parseInt(e.currentTarget.getAttribute('data-index'), 10);
            if (!isNaN(idx) && idx >= 0 && idx < orderCart.length) {
              const removed = orderCart.splice(idx, 1)[0];
              showToast(`Eliminado: ${removed.name}`);
              renderCart();
            }
          });
        });
      }

      if (cartCountBadge) {
        cartCountBadge.textContent = `${totalItemsCount} ${totalItemsCount === 1 ? 'producto' : 'productos'}`;
      }

      if (summaryItemsList) {
        summaryItemsList.innerHTML = summaryHtml;
      }

      if (summaryTotalPrice) {
        summaryTotalPrice.textContent = `$${total} MXN`;
      }

      if (stickyBarCount) {
        stickyBarCount.textContent = `${totalItemsCount} ${totalItemsCount === 1 ? 'producto' : 'productos'} • $${total} MXN`;
      }

      if (btnSubmitText) {
        btnSubmitText.textContent = currentPayment === 'mercadopago'
          ? `PAGAR CON MERCADO PAGO ($${total})`
          : `CONFIRMAR Y PAGAR AL RECOGER ($${total})`;
      }
    };

    // Botón Vaciar Comanda
    if (btnClearCart) {
      btnClearCart.addEventListener('click', () => {
        if (orderCart.length > 0) {
          orderCart = [];
          showToast('Comanda vaciada');
          renderCart();
        }
      });
    }

    // Tecla Escape para cerrar también el modal de personalización
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && customizerModal && customizerModal.classList.contains('active')) {
        closeCustomizer();
      }
    });

    // Listeners de método de pago
    paymentRadios.forEach(r => r.addEventListener('change', renderCart));
    renderCart();

    // Procesar envío del formulario (Checkout)
    orderForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (orderCart.length === 0) {
        alert('Por favor selecciona al menos un elote o botana desde el menú arriba antes de confirmar tu pedido.');
        const menuSec = document.getElementById('menu');
        if (menuSec) menuSec.scrollIntoView({ behavior: 'smooth' });
        return;
      }

      const custName = document.getElementById('custName')?.value.trim();
      const custPhone = document.getElementById('custPhone')?.value.trim();
      const pickupTime = document.getElementById('pickupTime')?.value || 'En 15 minutos';

      if (!custName || !custPhone) {
        alert('Por favor ingresa tu nombre y teléfono para tener tu pedido listo.');
        return;
      }

      // Calcular total de la orden
      let total = 0;
      orderCart.forEach(item => {
        total += item.price * item.quantity;
      });

      const orderId = `LMZ-${Math.floor(1000 + Math.random() * 9000)}`;

      // Construir desglose estructurado de productos para WhatsApp
      const itemsTextLines = orderCart.map((item, idx) => {
        const itemTotal = item.price * item.quantity;
        let line = `${idx + 1}. *${item.quantity}x ${item.name}* ($${itemTotal} MXN)`;
        if (item.chile && item.chile !== 'N/A') {
          line += `\n   🌶️ Chile: ${item.chile}`;
        }
        if (item.extras && item.extras.length > 0) {
          line += `\n   🧀 Preparación: ${item.extras.join(', ')}`;
        }
        if (item.notes) {
          line += `\n   📝 Nota: ${item.notes}`;
        }
        return line;
      });

      // Construir mensaje estructurado completo para WhatsApp
      const waMsgLines = [
        `¡Hola Elotes Los Mezquites! Quiero hacer un pedido *PARA RECOGER DE PASADA*:`,
        ``,
        `📋 *Folio de Pedido:* #${orderId}`,
        `👤 *Cliente:* ${custName}`,
        `📞 *Teléfono:* ${custPhone}`,
        `⏱️ *Tiempo estimado de llegada:* ${pickupTime}`,
        ``,
        `🌽 *DETALLE DEL PEDIDO:*`,
        itemsTextLines.join('\n\n'),
        ``,
        `💳 *Método de pago:* ${currentPayment === 'mercadopago' ? 'Mercado Pago (En línea)' : 'Pagar en efectivo al llegar'}`,
        `💰 *TOTAL A PAGAR:* $${total} MXN`,
        ``,
        `_Favor de confirmar que recibieron mi orden para tenerla calientita. ¡Muchas gracias!_`
      ];

      const encodedWaMsg = encodeURIComponent(waMsgLines.join('\n'));
      const waUrl = `https://wa.me/528121912778?text=${encodedWaMsg}`;

      // Si seleccionó Mercado Pago, generar preferencia en el backend
      if (currentPayment === 'mercadopago') {
        const originalText = btnSubmitText ? btnSubmitText.textContent : '';
        if (btnSubmitText) btnSubmitText.textContent = 'Conectando con Mercado Pago...';

        try {
          const res = await fetch('/api/create-preference', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              items: orderCart.map(item => ({
                id: item.id,
                name: item.name,
                price: item.price,
                quantity: item.quantity,
                chile: item.chile,
                extras: item.extras,
                notes: item.notes
              })),
              customer: { name: custName, phone: custPhone },
              time: pickupTime
            })
          });

          if (res.ok) {
            const data = await res.json();
            if (data.initPoint) {
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

        // Fallback si corre como sitio puramente estático:
        if (btnSubmitText) btnSubmitText.textContent = originalText;
        showToast(`Orden #${orderId} registrada. Abriendo WhatsApp...`);
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
