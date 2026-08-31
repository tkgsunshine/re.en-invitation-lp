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
  // 6. Pre-Registration Modal & Event Interceptor
  // ==========================================
  
  // Dynamically inject modal HTML if not already present
  if (!document.getElementById('register-modal')) {
    const modalHTML = `
    <div id="register-modal" class="modal" aria-hidden="true">
      <div class="modal__backdrop"></div>
      <div class="modal__container glass-card" style="border-radius: 12px; border: 1px solid var(--color-border); background: rgba(18, 18, 20, 0.97); backdrop-filter: blur(16px);">
        <button class="modal__close js-close-modal" aria-label="モーダルを閉じる" style="border-radius: 50%; font-size: 1.2rem;">&times;</button>
        <div class="modal__body" style="padding: 36px 28px;">
          
          <!-- Step 1: Entry Form -->
          <div id="modal-step-form" class="modal__step-panel modal__step-panel--active">
            <div class="modal__header" style="margin-bottom: 24px;">
              <div style="font-family: var(--font-serif); font-size: 1.1rem; color: var(--color-primary); margin-bottom: 4px; letter-spacing: 0.15em; font-weight: 700;">Re.en</div>
              <h3 class="modal__title" style="font-size: 1.35rem; font-weight: 700; margin-bottom: 6px;">創設メンバー 事前エントリー</h3>
              <p class="modal__subtitle" style="font-size: 0.82rem; color: var(--color-text-muted);">2026年冬グランドオープン予定（優先招待・事前受付中）</p>
            </div>

            <form id="js-preregister-form" onsubmit="return false;">
              <!-- Gender -->
              <div class="form-group" style="margin-bottom: 18px;">
                <label class="form-group__label" style="margin-bottom: 8px;">
                  性別 <span class="form-group__required" style="border-radius: 2px;">必須</span>
                </label>
                <div class="form-group__select-grid" style="grid-template-columns: 1fr 1fr; gap: 10px;">
                  <div class="form-group__select-card js-select-gender form-group__select-card--selected" data-value="男性" style="text-align: center; cursor: pointer; padding: 12px; font-weight: 500; font-size: 0.9rem; border-radius: 6px;">
                    男性
                  </div>
                  <div class="form-group__select-card js-select-gender" data-value="女性" style="text-align: center; cursor: pointer; padding: 12px; font-weight: 500; font-size: 0.9rem; border-radius: 6px;">
                    女性
                  </div>
                </div>
              </div>

              <!-- Age & Income -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 18px;">
                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-group__label" style="margin-bottom: 8px;">年代 <span class="form-group__required" style="border-radius: 2px;">必須</span></label>
                  <select id="prereg-age" class="form-group__input" style="background: var(--color-bg-alt); color: var(--color-text-white); cursor: pointer; padding: 12px 14px; border-radius: 6px; font-size: 0.88rem;">
                    <option value="" selected disabled>選択してください</option>
                    <option value="10代">10代</option>
                    <option value="20代">20代</option>
                    <option value="30代">30代</option>
                    <option value="40代">40代</option>
                    <option value="50代以上">50代以上</option>
                  </select>
                </div>
                
                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-group__label" style="margin-bottom: 8px;">年収 <span class="form-group__required" style="border-radius: 2px;">必須</span></label>
                  <select id="prereg-income" class="form-group__input" style="background: var(--color-bg-alt); color: var(--color-text-white); cursor: pointer; padding: 12px 14px; border-radius: 6px; font-size: 0.88rem;">
                    <option value="" selected disabled>選択してください</option>
                    <option value="〜500万円未満">〜500万円未満</option>
                    <option value="500万円〜800万円">500万円〜800万円</option>
                    <option value="800万円〜1,000万円">800万円〜1,000万円</option>
                    <option value="1,000万円〜1,500万円">1,000万円〜1,500万円</option>
                    <option value="1,500万円〜2,000万円">1,500万円〜2,000万円</option>
                    <option value="2,000万円〜3,000万円">2,000万円〜3,000万円</option>
                    <option value="3,000万円〜5,000万円">3,000万円〜5,000万円</option>
                    <option value="5,000万円〜1億円">5,000万円〜1億円</option>
                    <option value="1億円以上">1億円以上</option>
                  </select>
                </div>
              </div>

              <!-- Email -->
              <div class="form-group" style="margin-bottom: 18px;">
                <label class="form-group__label" style="margin-bottom: 8px;">
                  通知用メールアドレス <span class="form-group__required" style="border-radius: 2px;">必須</span>
                </label>
                <input type="email" id="prereg-email" class="form-group__input" placeholder="example@domain.com" required style="font-size: 0.95rem; padding: 12px 14px; border-radius: 6px;">
                <div id="prereg-email-error" class="form-group__error" style="font-size: 0.78rem; color: #E25C5C; margin-top: 6px; display: none;">有効なメールアドレスを入力してください。</div>
              </div>

              <!-- Feedback / Requests (Optional) -->
              <div class="form-group" style="margin-bottom: 22px;">
                <label class="form-group__label" style="margin-bottom: 8px;">
                  Re.enへのご要望・ご期待 <span class="form-group__optional" style="font-size: 0.72rem; padding: 2px 6px; background: rgba(255,255,255,0.08); color: var(--color-text-muted); border-radius: 2px; margin-left: 6px;">任意</span>
                </label>
                <textarea id="prereg-feedback" class="form-group__input" rows="3" placeholder="サービスへのご要望や期待すること、ご意見などがあればご自由にご記入ください" style="font-size: 0.88rem; padding: 10px 12px; border-radius: 6px; resize: vertical; min-height: 68px; background: var(--color-bg-alt); color: var(--color-text-white); font-family: inherit;"></textarea>
              </div>

              <button type="submit" id="btn-submit-prereg" class="btn btn--primary btn--large btn--pulse" style="width: 100%; font-weight: 700; font-size: 0.98rem; padding: 14px; border-radius: 6px; justify-content: center;">
                優先インビテーションに申し込む
              </button>
              
              <p style="font-size: 0.72rem; color: var(--color-text-muted); margin-top: 14px; text-align: center; line-height: 1.55;">
                ※ご登録いただいた情報は、リリース日決定のご案内および事前審査結果のご連絡以外の目的には使用いたしません。
              </p>
            </form>
          </div>

          <!-- Step 2: Thank You Page -->
          <div id="modal-step-thankyou" class="modal__step-panel" style="display: none;">
            <div class="modal__header" style="margin-bottom: 20px;">
              <div style="width: 56px; height: 56px; margin: 0 auto 14px; border-radius: 50%; border: 2px solid var(--color-primary); display: flex; align-items: center; justify-content: center; background: rgba(191,169,120,0.12);">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <h3 class="modal__title" style="font-size: 1.25rem; font-weight: 700; color: var(--color-text-white);">事前エントリーが完了いたしました</h3>
            </div>

            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 22px 18px; font-size: 0.86rem; line-height: 1.8; color: var(--color-text-body); margin-bottom: 22px; text-align: left;">
              <p style="margin-bottom: 14px;">ご登録いただき誠にありがとうございます。</p>
              <p style="margin-bottom: 14px;">
                リリース日が確定いたしましたら、ご登録いただいたメールアドレス宛に<strong style="color: var(--color-primary); font-weight: 700;">「リリース日決定のご通知」</strong>をお送りいたします。
              </p>
              <p style="margin-bottom: 0;">
                あわせて、男性会員様には創設メンバー限定特典である<strong style="color: var(--color-primary); font-weight: 700;">「有料サブスクリプション【2ヶ月間】完全無料提供」の事前審査結果</strong>につきましても、リリース日決定通知と共にお送りさせていただきます。<br><br>
                今しばらく楽しみにお待ちくださいませ。
              </p>
            </div>

            <button type="button" class="btn btn--primary js-close-modal" style="width: 100%; text-align: center; justify-content: center; padding: 12px; border-radius: 6px; font-weight: 700;">
              閉じる
            </button>
          </div>

        </div>
      </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
  }

  const registerModal = document.getElementById('register-modal');
  const modalBackdrop = registerModal ? registerModal.querySelector('.modal__backdrop') : null;
  const modalStepForm = document.getElementById('modal-step-form');
  const modalStepThankyou = document.getElementById('modal-step-thankyou');
  const preregForm = document.getElementById('js-preregister-form');
  const emailInput = document.getElementById('prereg-email');
  const emailError = document.getElementById('prereg-email-error');
  const genderCards = document.querySelectorAll('.js-select-gender');

  let selectedGender = '男性';

  genderCards.forEach(card => {
    card.addEventListener('click', () => {
      genderCards.forEach(c => c.classList.remove('form-group__select-card--selected'));
      card.classList.add('form-group__select-card--selected');
      selectedGender = card.dataset.value;
    });
  });

  const openRegisterModal = (e) => {
    if (e) e.preventDefault();
    if (!registerModal) return;
    
    // Reset view to form
    if (modalStepForm) modalStepForm.style.display = 'block';
    if (modalStepThankyou) modalStepThankyou.style.display = 'none';
    if (emailError) emailError.style.display = 'none';
    
    registerModal.classList.add('modal--open');
    document.body.style.overflow = 'hidden';
  };

  const closeRegisterModal = () => {
    if (!registerModal) return;
    const isThankyouActive = modalStepThankyou && modalStepThankyou.style.display !== 'none';
    registerModal.classList.remove('modal--open');
    document.body.style.overflow = '';

    // Scroll to top of page when closing from Thank You screen
    if (isThankyouActive) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Attach modal trigger interceptor to all CTA buttons
  document.querySelectorAll('a[href="/register"], a[href="/login"], a[href="#register"], .js-open-register').forEach(btn => {
    btn.addEventListener('click', openRegisterModal);
  });

  // Attach to close buttons
  document.querySelectorAll('.js-close-modal').forEach(btn => {
    btn.addEventListener('click', closeRegisterModal);
  });
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', closeRegisterModal);
  }

  // Handle Preregistration Submit
  if (preregForm) {
    preregForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!emailInput) return;

      const emailVal = emailInput.value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailVal || !emailRegex.test(emailVal)) {
        if (emailError) {
          emailError.textContent = '有効なメールアドレスを入力してください。';
          emailError.style.display = 'block';
        }
        return;
      }

      const ageVal = document.getElementById('prereg-age') ? document.getElementById('prereg-age').value : '';
      const incomeVal = document.getElementById('prereg-income') ? document.getElementById('prereg-income').value : '';
      const feedbackVal = document.getElementById('prereg-feedback') ? document.getElementById('prereg-feedback').value.trim() : '';

      if (!ageVal) {
        if (emailError) {
          emailError.textContent = '年代を選択してください。';
          emailError.style.display = 'block';
        }
        return;
      }

      if (!incomeVal) {
        if (emailError) {
          emailError.textContent = '年収を選択してください。';
          emailError.style.display = 'block';
        }
        return;
      }

      if (emailError) emailError.style.display = 'none';

      const submitBtn = document.getElementById('btn-submit-prereg');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = '送信中...';
      }

      // Send form data to SSGform via native HTML form submission (hidden iframe)
      try {
        let iframe = document.getElementById('ssgform-target-iframe');
        if (!iframe) {
          iframe = document.createElement('iframe');
          iframe.name = 'ssgform-target-iframe';
          iframe.id = 'ssgform-target-iframe';
          iframe.style.display = 'none';
          document.body.appendChild(iframe);
        }

        const hiddenForm = document.createElement('form');
        hiddenForm.action = 'https://ssgform.com/s/aZL3mBK0p4BM';
        hiddenForm.method = 'POST';
        hiddenForm.target = 'ssgform-target-iframe';

        const fields = {
          '性別': selectedGender,
          '年代': ageVal,
          '年収': incomeVal,
          'メールアドレス': emailVal,
          'ご要望・ご期待': feedbackVal
        };

        for (const [key, val] of Object.entries(fields)) {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = key;
          input.value = val;
          hiddenForm.appendChild(input);
        }

        document.body.appendChild(hiddenForm);
        hiddenForm.submit();
        setTimeout(() => { hiddenForm.remove(); }, 3000);
      } catch (err) {
        console.warn('SSGform submission warning:', err);
      }

      // Save submission data to localStorage backup & API log
      try {
        const entry = {
          gender: selectedGender,
          age: ageVal,
          income: incomeVal,
          email: emailVal,
          feedback: feedbackVal,
          timestamp: new Date().toISOString()
        };
        const existing = JSON.parse(localStorage.getItem('reen_preregistrations') || '[]');
        existing.push(entry);
        localStorage.setItem('reen_preregistrations', JSON.stringify(existing));

        // Dual-logging endpoint
        fetch('/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(entry)
        }).catch(() => {});
      } catch (e) {
        console.error('Failed to save preregistration:', e);
      }

      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '優先インビテーションに申し込む';
      }

      // Switch to Thank You screen
      if (modalStepForm) modalStepForm.style.display = 'none';
      if (modalStepThankyou) modalStepThankyou.style.display = 'block';
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

  // ==========================================
  // 8. Column Pagination, Category Filter, and Search Controller
  // ==========================================
  const columnGrid = document.querySelector('.column-main .column-grid');
  const paginationContainer = document.querySelector('.pagination');

  if (columnGrid && paginationContainer) {
    const cards = Array.from(columnGrid.querySelectorAll('.column-card'));
    const categoryLinks = document.querySelectorAll('.category-nav__link');
    const sidebarCategoryLinks = document.querySelectorAll('.sidebar-list__item a');
    const searchInput = document.querySelector('.sidebar-search__input');
    const searchBtn = document.querySelector('.sidebar-search__btn');

    const getCategoryFromHash = () => {
      const hash = decodeURIComponent(window.location.hash.slice(1));
      const validCategories = ['全て', '出会いのコツ', 'プライバシー対策', 'セカンドパートナー', 'お悩み'];
      return (hash && validCategories.includes(hash)) ? hash : '全て';
    };

    let currentCategory = getCategoryFromHash();
    let searchQuery = '';
    let currentPage = 1;
    const itemsPerPage = 10;

    // Filter, Paginate, and Render
    const updateColumnList = () => {
      // 1. Filter cards based on Category and Search Query
      const filteredCards = cards.filter(card => {
        // Category check
        const badge = card.querySelector('.column-card__badge');
        const badgeText = badge ? badge.textContent.trim() : '';
        const matchesCategory = (currentCategory === '全て' || badgeText === currentCategory);

        // Search check
        let matchesSearch = true;
        if (searchQuery) {
          const title = card.querySelector('.column-card__title').textContent.toLowerCase();
          const excerpt = card.querySelector('.column-card__excerpt').textContent.toLowerCase();
          matchesSearch = title.includes(searchQuery) || excerpt.includes(searchQuery);
        }

        return matchesCategory && matchesSearch;
      });

      // 2. Hide all cards first
      cards.forEach(card => {
        card.style.display = 'none';
      });

      // 3. Paginate the filtered cards
      const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
      if (currentPage > totalPages) currentPage = Math.max(1, totalPages);

      const startIndex = (currentPage - 1) * itemsPerPage;
      const endIndex = Math.min(startIndex + itemsPerPage, filteredCards.length);

      for (let i = startIndex; i < endIndex; i++) {
        const card = filteredCards[i];
        card.style.display = 'flex';
        // Ensure the card is visible (if it was hidden by scroll reveal observer)
        card.classList.add('reveal--visible');
      }

      // 4. Render Pagination Controls
      renderPagination(totalPages);
    };

    // Render Pagination Buttons
    const renderPagination = (totalPages) => {
      paginationContainer.innerHTML = '';
      if (totalPages <= 1) {
        paginationContainer.style.display = 'none';
        return;
      }
      paginationContainer.style.display = 'flex';

      // Page numbers
      for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.href = '#';
        pageLink.className = `pagination__item${i === currentPage ? ' pagination__item--active' : ''}`;
        pageLink.textContent = i;
        pageLink.addEventListener('click', (e) => {
          e.preventDefault();
          currentPage = i;
          updateColumnList();
          scrollToTop();
        });
        paginationContainer.appendChild(pageLink);
      }

      // Next button
      if (currentPage < totalPages) {
        const nextLink = document.createElement('a');
        nextLink.href = '#';
        nextLink.className = 'pagination__item';
        nextLink.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        `;
        nextLink.addEventListener('click', (e) => {
          e.preventDefault();
          currentPage++;
          updateColumnList();
          scrollToTop();
        });
        paginationContainer.appendChild(nextLink);
      }
    };

    // Scroll to the top of column section
    const scrollToTop = () => {
      const targetSection = document.querySelector('.column-container');
      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 90,
          behavior: 'smooth'
        });
      }
    };

    // Sync Category Navigation Active Classes
    const syncCategoryActiveState = () => {
      // Top tabs
      categoryLinks.forEach(link => {
        const linkText = link.textContent.trim();
        if (linkText === currentCategory) {
          link.classList.add('category-nav__link--active');
        } else {
          link.classList.remove('category-nav__link--active');
        }
      });

      // Sidebar items
      sidebarCategoryLinks.forEach(link => {
        // Strip out counts or text modifications (e.g. "全てコラム 20" -> "全て")
        const rawText = link.childNodes[0].textContent.trim();
        const normalizedText = rawText.replace('コラム', '');
        
        // Find parent list item
        const parentLi = link.closest('.sidebar-list__item');
        if (parentLi) {
          if (normalizedText === currentCategory) {
            parentLi.classList.add('sidebar-list__item--active');
            link.style.color = 'var(--color-primary)';
          } else {
            parentLi.classList.remove('sidebar-list__item--active');
            link.style.color = '';
          }
        }
      });
    };

    // Category click handler
    const selectCategory = (categoryName) => {
      currentCategory = categoryName;
      currentPage = 1;

      // Update hash in URL bar without page reload
      if (categoryName === '全て') {
        history.pushState(null, null, window.location.pathname + window.location.search);
      } else {
        history.pushState(null, null, '#' + categoryName);
      }

      syncCategoryActiveState();
      updateColumnList();
    };

    // Hook up Category Nav links
    categoryLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const categoryName = link.textContent.trim();
        selectCategory(categoryName);
      });
    });

    // Hook up Sidebar Category links
    sidebarCategoryLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const rawText = link.childNodes[0].textContent.trim();
        const categoryName = rawText.replace('コラム', '');
        selectCategory(categoryName);
      });
    });

    // Hook up Search Input
    if (searchBtn && searchInput) {
      const executeSearch = () => {
        searchQuery = searchInput.value.trim().toLowerCase();
        currentPage = 1;
        updateColumnList();
      };

      searchBtn.addEventListener('click', (e) => {
        e.preventDefault();
        executeSearch();
      });

      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          executeSearch();
        }
      });

      // Live search on keyup/input
      searchInput.addEventListener('input', () => {
        searchQuery = searchInput.value.trim().toLowerCase();
        currentPage = 1;
        updateColumnList();
      });
    }

    // Listen to hash changes (for browser back/forward buttons and cross-page navigation)
    window.addEventListener('hashchange', () => {
      const newCategory = getCategoryFromHash();
      if (newCategory !== currentCategory) {
        currentCategory = newCategory;
        currentPage = 1;
        syncCategoryActiveState();
        updateColumnList();
      }
    });

    // Initialize display
    syncCategoryActiveState();
    updateColumnList();
  }


  // ==========================================
  // 9. Showcase App Screen Switcher (Auto-cycling & Interactive)
  // ==========================================
  const mockupImages = document.querySelectorAll('.js-mockup-img');
  const mockupDots = document.querySelectorAll('.js-mockup-dot');
  const showcaseItems = document.querySelectorAll('.js-showcase-item');
  const showcaseSection = document.getElementById('showcase');

  if (mockupImages.length > 0) {
    let activeIndex = 0;
    let cycleInterval = null;
    const cycleSpeed = 3500; // 3.5 seconds

    const switchMockup = (index) => {
      if (index === activeIndex) return;
      activeIndex = index;

      // Update images
      mockupImages.forEach((img, idx) => {
        if (idx === index) {
          img.classList.add('showcase__img--active');
        } else {
          img.classList.remove('showcase__img--active');
        }
      });

      // Update dots
      mockupDots.forEach((dot, idx) => {
        if (idx === index) {
          dot.classList.add('showcase__dot--active');
        } else {
          dot.classList.remove('showcase__dot--active');
        }
      });

      // Update feature items
      showcaseItems.forEach((item, idx) => {
        if (idx === index) {
          item.classList.add('showcase__item--active');
        } else {
          item.classList.remove('showcase__item--active');
        }
      });
    };

    // Auto cycling function
    const startCycling = () => {
      if (cycleInterval) return;
      cycleInterval = setInterval(() => {
        const nextIndex = (activeIndex + 1) % mockupImages.length;
        switchMockup(nextIndex);
      }, cycleSpeed);
    };

    const stopCycling = () => {
      if (cycleInterval) {
        clearInterval(cycleInterval);
        cycleInterval = null;
      }
    };

    // Attach click events to dots (reset auto-cycle on click)
    mockupDots.forEach(dot => {
      dot.addEventListener('click', () => {
        const index = parseInt(dot.dataset.index, 10);
        switchMockup(index);
        stopCycling();
        startCycling();
      });
    });

    // Attach click and hover events to feature list items
    showcaseItems.forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.dataset.index, 10);
        switchMockup(index);
        stopCycling();
        startCycling();
      });
      item.addEventListener('mouseenter', () => {
        const index = parseInt(item.dataset.index, 10);
        switchMockup(index);
        stopCycling();
      });
      item.addEventListener('mouseleave', () => {
        startCycling();
      });
    });

    // Start cycling when the section is visible
    if (showcaseSection) {
      const showcaseObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            startCycling();
          } else {
            stopCycling();
          }
        });
      }, { threshold: 0.1 });
      showcaseObserver.observe(showcaseSection);
    } else {
      startCycling();
    }
  }
});
