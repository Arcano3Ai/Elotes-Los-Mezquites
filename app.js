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
});
