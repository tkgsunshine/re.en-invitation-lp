/* メールアドレス入力のドメイン候補（#reg-email / #prereg-email）。動的に生成される入力欄にも効くよう document で委譲する */
(function () {
  if (window.__emailSuggestInit) return;
  window.__emailSuggestInit = true;

  var DOMAINS = ['gmail.com', 'yahoo.co.jp', 'icloud.com', 'ezweb.ne.jp', 'docomo.ne.jp', 'softbank.ne.jp', 'outlook.jp', 'hotmail.co.jp'];
  var IDS = { 'reg-email': 1, 'prereg-email': 1 };

  var style = document.createElement('style');
  style.textContent =
    '.email-suggest{position:absolute;left:0;right:0;z-index:50;margin:4px 0 0;padding:4px 0;list-style:none;background:rgba(24,24,28,.98);border:1px solid var(--color-border,rgba(191,169,120,.25));border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.6);max-height:260px;overflow-y:auto;-webkit-overflow-scrolling:touch}' +
    '.email-suggest__item{padding:12px 14px;font-size:16px;line-height:1.3;color:#fff;cursor:pointer;word-break:break-all;-webkit-tap-highlight-color:transparent}' +
    '.email-suggest__item+.email-suggest__item{border-top:1px solid rgba(255,255,255,.06)}' +
    '.email-suggest__item.is-active,.email-suggest__item:hover{background:rgba(191,169,120,.15)}' +
    '.email-suggest__domain{color:#D5C091;font-weight:700}';
  document.head.appendChild(style);

  var list = null, input = null, items = [], active = -1;

  function close() {
    if (list && list.parentNode) list.parentNode.removeChild(list);
    list = null; input = null; items = []; active = -1;
  }

  function highlight(i) {
    active = i;
    for (var k = 0; k < list.children.length; k++) {
      list.children[k].classList.toggle('is-active', k === i);
    }
  }

  function choose(value) {
    if (!input) return;
    var el = input;
    close();
    el.value = value;
    el.focus();
  }

  function render(el) {
    var v = el.value;
    var at = v.indexOf('@');
    if (at < 1) return close();
    var local = v.slice(0, at), typed = v.slice(at + 1).toLowerCase();
    items = DOMAINS.filter(function (d) { return d.indexOf(typed) === 0 && d !== typed; });
    if (!items.length) return close();

    var host = el.parentNode;
    if (!list) {
      list = document.createElement('ul');
      list.className = 'email-suggest';
      list.setAttribute('role', 'listbox');
    }
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    if (list.parentNode !== host) host.appendChild(list);
    list.style.top = (el.offsetTop + el.offsetHeight) + 'px';
    input = el;
    list.innerHTML = '';
    items.forEach(function (d, i) {
      var li = document.createElement('li');
      li.className = 'email-suggest__item';
      li.setAttribute('role', 'option');
      li.appendChild(document.createTextNode(local));
      var s = document.createElement('span');
      s.className = 'email-suggest__domain';
      s.textContent = '@' + d;
      li.appendChild(s);
      li.addEventListener('mousedown', function (e) { e.preventDefault(); });
      li.addEventListener('click', function () { choose(local + '@' + d); });
      list.appendChild(li);
    });
    active = -1;
  }

  document.addEventListener('focusin', function (e) {
    var t = e.target;
    if (t && IDS[t.id] && !t.dataset.emailSuggest) {
      t.dataset.emailSuggest = '1';
      t.setAttribute('autocomplete', 'email');
      t.setAttribute('inputmode', 'email');
      t.setAttribute('autocapitalize', 'none');
      t.setAttribute('autocorrect', 'off');
      t.setAttribute('spellcheck', 'false');
    }
  });
  document.addEventListener('input', function (e) {
    if (e.target && IDS[e.target.id]) render(e.target);
  });
  document.addEventListener('keydown', function (e) {
    if (!list || e.target !== input) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); highlight((active + 1) % items.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); highlight((active - 1 + items.length) % items.length); }
    else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); var v = input.value; choose(v.slice(0, v.indexOf('@')) + '@' + items[active]); }
    else if (e.key === 'Escape' || e.key === 'Tab') close();
  });
  document.addEventListener('focusout', function (e) {
    if (e.target === input) setTimeout(close, 150);
  });
  document.addEventListener('click', function (e) {
    if (list && !list.contains(e.target) && e.target !== input) close();
  });
})();
