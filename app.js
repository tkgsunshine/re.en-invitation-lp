document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  // 0. Char-by-Char Text Animation (Headline)
  // ==========================================
  const headlineParts = document.querySelectorAll('.hero__headline-part');
  headlineParts.forEach((part, partIdx) => {
    const text = part.textContent.trim();
    part.innerHTML = '';
    
    [...text].forEach((char, charIdx) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.classList.add('char');
      
      const baseDelay = partIdx === 0 ? 0.6 : 1.0;
      const charDelay = baseDelay + charIdx * 0.05;
      span.style.animationDelay = `${charDelay}s`;
      
      part.appendChild(span);
    });
  });

  // ==========================================
  // 1. Header Scrolled State
  // ==========================================
  const header = document.querySelector('.js-header');
  const handleScroll = () => {
    if (!header) return;
    if (window.scrollY > 50) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Initial check

  // ==========================================
  // 2. Mobile Menu Toggle
  // ==========================================
  const menuBtn = document.querySelector('.js-menu-toggle');
  const mobileMenu = document.querySelector('.js-mobile-menu');
  const mobileLinks = document.querySelectorAll('.mobile-nav__link');

  const toggleMenu = () => {
    if (!menuBtn || !mobileMenu) return;
    const isOpen = menuBtn.classList.toggle('menu-toggle--open');
    mobileMenu.classList.toggle('header__mobile-menu--open');
    menuBtn.setAttribute('aria-expanded', isOpen);
  };

  if (menuBtn) {
    menuBtn.addEventListener('click', toggleMenu);
  }
  
  // Close menu when clicking nav links
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (mobileMenu && mobileMenu.classList.contains('header__mobile-menu--open')) {
        toggleMenu();
      }
    });
  });

  // ==========================================
  // 3. Scroll Reveal Observer
  // ==========================================
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal--visible');
        revealObserver.unobserve(entry.target); // Reveal only once
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));

  // ==========================================
  // 3.1 Profile Charts Animation
  // ==========================================
  const ageBars = document.querySelectorAll('.bar-chart__bar');
  const doughnutSegments = document.querySelectorAll('.circular-chart .circle');
  const chartsSection = document.querySelector('.charts-wrapper');

  // Store target values and reset to 0
  const ageBarTargets = [];
  ageBars.forEach((bar, idx) => {
    ageBarTargets[idx] = bar.style.width;
    bar.style.width = '0%';
  });

  const doughnutTargets = [];
  doughnutSegments.forEach((seg, idx) => {
    doughnutTargets[idx] = seg.getAttribute('stroke-dasharray');
    seg.setAttribute('stroke-dasharray', '0, 100');
  });

  // Animate charts when scrolled into view
  const animateCharts = () => {
    // Animate age bars
    ageBars.forEach((bar, idx) => {
      setTimeout(() => {
        bar.style.width = ageBarTargets[idx];
      }, idx * 60); // cascade animation
    });

    // Animate doughnut segments
    doughnutSegments.forEach((seg, idx) => {
      setTimeout(() => {
        seg.setAttribute('stroke-dasharray', doughnutTargets[idx]);
      }, 300);
    });
  };

  if (chartsSection) {
    const chartsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCharts();
          chartsObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.4
    });
    chartsObserver.observe(chartsSection);
  }

  // ==========================================
  // 4. Photo Blur Simulator
  // ==========================================
  const blurSlider = document.getElementById('blur-slider');
  const blurImage = document.getElementById('blur-image');
  const blurValueText = document.getElementById('blur-value');
  const presetBtns = document.querySelectorAll('.js-preset-btn');

  const updateBlur = (value) => {
    // Map slider 0-100 to blur 0-5px
    const blurPx = (value / 100) * 5;
    if (blurImage) blurImage.style.filter = `blur(${blurPx}px)`;
    
    // Update value text
    if (blurValueText) {
      if (value == 0) {
        blurValueText.textContent = '公開(0%)';
        blurValueText.style.color = 'var(--color-text-light)';
      } else if (value == 100) {
        blurValueText.textContent = 'MAX (完全保護)';
        blurValueText.style.color = 'var(--color-primary)';
      } else {
        blurValueText.textContent = `保護率 ${value}%`;
        blurValueText.style.color = 'var(--color-primary)';
      }
    }

    // Sync slider value
    if (blurSlider) blurSlider.value = value;

    // Highlight matching preset button
    presetBtns.forEach(btn => {
      const btnVal = parseInt(btn.dataset.value, 10);
      if (btnVal === parseInt(value, 10)) {
        btn.classList.add('simulator__preset-btn--active');
      } else {
        btn.classList.remove('simulator__preset-btn--active');
      }
    });
  };

  // Autoplay blur animation
  let autoplayInterval = null;
  let autoplayDirection = 1; // 1 = increasing, -1 = decreasing
  let autoplayDelayTimeout = null;
  let isAutoplayActive = true;
  
  const stopAutoplay = () => {
    isAutoplayActive = false;
    if (autoplayInterval) {
      clearInterval(autoplayInterval);
      autoplayInterval = null;
    }
    if (autoplayDelayTimeout) {
      clearTimeout(autoplayDelayTimeout);
      autoplayDelayTimeout = null;
    }
  };

  const startAutoplay = () => {
    let currentValue = 0;
    updateBlur(currentValue);

    const step = () => {
      if (!isAutoplayActive) return;
      
      if (autoplayDirection === 1) {
        currentValue += 1;
        if (currentValue >= 85) {
          currentValue = 85;
          updateBlur(currentValue);
          autoplayDirection = -1;
          // Pause at max blur (85%)
          clearInterval(autoplayInterval);
          autoplayInterval = null;
          autoplayDelayTimeout = setTimeout(() => {
            if (isAutoplayActive) {
              autoplayInterval = setInterval(step, 24);
            }
          }, 1500);
          return;
        }
      } else {
        currentValue -= 1;
        if (currentValue <= 0) {
          currentValue = 0;
          updateBlur(currentValue);
          autoplayDirection = 1;
          // Pause at min blur (0%)
          clearInterval(autoplayInterval);
          autoplayInterval = null;
          autoplayDelayTimeout = setTimeout(() => {
            if (isAutoplayActive) {
              autoplayInterval = setInterval(step, 20);
            }
          }, 1200);
          return;
        }
      }
      updateBlur(currentValue);
    };

    // Delay start of autoplay by 0.8 seconds
    autoplayDelayTimeout = setTimeout(() => {
      if (isAutoplayActive) {
        autoplayInterval = setInterval(step, 24);
      }
    }, 800);
  };

  // Slider input event
  if (blurSlider) {
    blurSlider.addEventListener('input', (e) => {
      stopAutoplay();
      updateBlur(e.target.value);
    });
    blurSlider.addEventListener('mousedown', stopAutoplay);
    blurSlider.addEventListener('touchstart', stopAutoplay);
  }

  // Preset button clicks
  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      stopAutoplay();
      const val = btn.dataset.value;
      updateBlur(val);
    });
  });

  // Observe Privacy section to trigger autoplay
  const privacySection = document.getElementById('privacy');
  if (privacySection) {
    const privacyObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          startAutoplay();
          privacyObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15
    });
    privacyObserver.observe(privacySection);
  } else {
    startAutoplay();
  }

  // ==========================================
  // 5. FAQ Accordion
  // ==========================================
  const faqTriggers = document.querySelectorAll('.faq-item__trigger');

  faqTriggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const faqItem = trigger.closest('.faq-item');
      const content = faqItem.querySelector('.faq-item__content');
      const isActive = faqItem.classList.contains('faq-item--active');

      // Close all other FAQs first for a clean accordion behavior
      document.querySelectorAll('.faq-item').forEach(item => {
        if (item !== faqItem) {
          item.classList.remove('faq-item--active');
          item.querySelector('.faq-item__content').style.maxHeight = null;
        }
      });

      // Toggle current FAQ
      if (isActive) {
        faqItem.classList.remove('faq-item--active');
        content.style.maxHeight = null;
      } else {
        faqItem.classList.add('faq-item--active');
        content.style.maxHeight = content.scrollHeight + 'px';
      }
    });
  });

  // ==========================================
  // 6. Registration Multi-Step Modal
  // ==========================================
  const openModalBtns = document.querySelectorAll('.js-open-register');
  const closeModalBtns = document.querySelectorAll('.js-close-modal');
  const registerModal = document.getElementById('register-modal');
  const modalBackdrop = registerModal ? registerModal.querySelector('.modal__backdrop') : null;

  const stepPanels = document.querySelectorAll('.modal__step-panel');
  const progressSteps = document.querySelectorAll('.modal__progress-step');
  
  // Navigation Buttons
  const nextStep1Btn = document.getElementById('btn-next-step1');
  const nextStep2Btn = document.getElementById('btn-next-step2');
  const prevStep2Btn = document.getElementById('btn-prev-step2');
  const prevStep3Btn = document.getElementById('btn-prev-step3');
  const submitBtn = document.getElementById('btn-submit-register');

  // Input Fields & Errors
  const genderCards = document.querySelectorAll('.js-gender-card');
  const birthDateInput = document.getElementById('reg-birthdate');
  const nicknameInput = document.getElementById('reg-nickname');
  const passwordInput = document.getElementById('reg-password');
  const purposeCards = document.querySelectorAll('.js-purpose-card');

  const errorBirthdate = document.getElementById('err-birthdate');
  const errorNickname = document.getElementById('err-nickname');
  const errorPassword = document.getElementById('err-password');

  // Registration Form State
  let currentStep = 0; // 0: Step 1, 1: Step 2, 2: Step 3
  let regFormState = {
    gender: 'female', // default selected
    birthdate: '',
    nickname: '',
    password: '',
    purpose: 'friend' // default selected
  };

  // Open/Close Modal functions
  const openRegisterModal = (e) => {
    if (e) e.preventDefault();
    if (!registerModal) return;
    registerModal.classList.add('modal--open');
    document.body.style.overflow = 'hidden'; // Lock background scroll
    goToStep(0); // Reset to first step
  };

  const closeRegisterModal = () => {
    if (!registerModal) return;
    registerModal.classList.remove('modal--open');
    document.body.style.overflow = ''; // Unlock scroll
  };

  // Event listeners for modal toggle
  openModalBtns.forEach(btn => btn.addEventListener('click', openRegisterModal));
  closeModalBtns.forEach(btn => btn.addEventListener('click', closeRegisterModal));
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', closeRegisterModal);
  }

  // Go to step function
  const goToStep = (stepIndex) => {
    currentStep = stepIndex;
    
    // Update active panels
    stepPanels.forEach((panel, idx) => {
      if (idx === stepIndex) {
        panel.classList.add('modal__step-panel--active');
      } else {
        panel.classList.remove('modal__step-panel--active');
      }
    });

    // Update progress steps
    progressSteps.forEach((progress, idx) => {
      if (idx <= stepIndex) {
        progress.classList.add('modal__progress-step--active');
      } else {
        progress.classList.remove('modal__progress-step--active');
      }
    });
  };

  // Gender Card Selector
  genderCards.forEach(card => {
    card.addEventListener('click', () => {
      genderCards.forEach(c => c.classList.remove('form-group__select-card--selected'));
      card.classList.add('form-group__select-card--selected');
      regFormState.gender = card.dataset.gender;
    });
  });

  // Purpose Card Selector
  purposeCards.forEach(card => {
    card.addEventListener('click', () => {
      purposeCards.forEach(c => c.classList.remove('form-group__select-card--selected'));
      card.classList.add('form-group__select-card--selected');
      regFormState.purpose = card.dataset.purpose;
    });
  });

  // Step 1 validation & Next
  if (nextStep1Btn) {
    nextStep1Btn.addEventListener('click', () => {
      if (!birthDateInput) return;
      const birthdateVal = birthDateInput.value;
      if (!birthdateVal) {
        if (errorBirthdate) {
          errorBirthdate.textContent = '生年月日を入力してください。';
          errorBirthdate.style.display = 'block';
        }
        return;
      }

      // Calculate age (must be >= 18)
      const birthdate = new Date(birthdateVal);
      const today = new Date();
      let age = today.getFullYear() - birthdate.getFullYear();
      const m = today.getMonth() - birthdate.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birthdate.getDate())) {
        age--;
      }

      if (age < 18) {
        if (errorBirthdate) {
          errorBirthdate.textContent = '18歳未満の方はご利用いただけません。';
          errorBirthdate.style.display = 'block';
        }
        return;
      }

      if (errorBirthdate) errorBirthdate.style.display = 'none';
      regFormState.birthdate = birthdateVal;
      goToStep(1);
    });
  }

  // Step 2 validation & Next
  if (nextStep2Btn) {
    nextStep2Btn.addEventListener('click', () => {
      if (!nicknameInput || !passwordInput) return;
      let isValid = true;
      const nicknameVal = nicknameInput.value.trim();
      const passwordVal = passwordInput.value;

      if (!nicknameVal) {
        if (errorNickname) {
          errorNickname.textContent = 'ニックネームを入力してください。';
          errorNickname.style.display = 'block';
        }
        isValid = false;
      } else {
        if (errorNickname) errorNickname.style.display = 'none';
      }

      if (passwordVal.length < 8) {
        if (errorPassword) {
          errorPassword.textContent = 'パスワードは8文字以上で入力してください。';
          errorPassword.style.display = 'block';
        }
        isValid = false;
      } else {
        if (errorPassword) errorPassword.style.display = 'none';
      }

      if (!isValid) return;

      regFormState.nickname = nicknameVal;
      regFormState.password = passwordVal;
      goToStep(2);
    });
  }

  // Back Buttons
  if (prevStep2Btn) {
    prevStep2Btn.addEventListener('click', () => goToStep(0));
  }
  if (prevStep3Btn) {
    prevStep3Btn.addEventListener('click', () => goToStep(1));
  }

  // Submit / Finish
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      // Show success dialog
      alert(`登録が完了しました！\n\nニックネーム: ${regFormState.nickname}\n目的: ${regFormState.purpose}\n\nRe.en（リエン）で素晴らしい出会いをお楽しみください。`);
      
      // Clear form inputs
      if (birthDateInput) birthDateInput.value = '';
      if (nicknameInput) nicknameInput.value = '';
      if (passwordInput) passwordInput.value = '';
      genderCards.forEach((c, idx) => {
        if (idx === 0) c.classList.add('form-group__select-card--selected');
        else c.classList.remove('form-group__select-card--selected');
      });
      purposeCards.forEach((c, idx) => {
        if (idx === 0) c.classList.add('form-group__select-card--selected');
        else c.classList.remove('form-group__select-card--selected');
      });

      closeRegisterModal();
    });
  }

  // ==========================================
  // 7. Scroll Progress Bar
  // ==========================================
  const progressBar = document.getElementById('scroll-progress');
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (progressBar) {
      progressBar.style.width = scrollPercent + '%';
    }
  });
});
