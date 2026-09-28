/* Quadrozzi — shared page behavior: sticky header, mobile menu, reveals, footer year */
(function () {
  // Header: solid after leaving the hero
  const header = document.getElementById('header');
  const onScroll = function () { header.classList.toggle('is-solid', window.scrollY > 40); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    const setMenu = function (open) {
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    toggle.addEventListener('click', function () { setMenu(!document.body.classList.contains('menu-open')); });
    document.querySelectorAll('.nav-links a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  // Hero cascade + scroll reveals
  requestAnimationFrame(function () { requestAnimationFrame(function () {
    document.querySelectorAll('.cascade').forEach(function (el) { el.classList.add('is-in'); });
  }); });
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Inquiry forms (GBX booking, Helping Hooves get-involved).
  // The page sets window.INQUIRY = { email, endpoint, subject } before loading this file.
  // With no endpoint, submitting opens the visitor's email app with every answer filled in.
  const form = document.querySelector('form[data-inquiry]');
  const cfg = window.INQUIRY;
  if (form && cfg) {
    const status = form.querySelector('.form-status');
    const note = form.querySelector('.form-note');
    document.querySelectorAll('[data-inquiry-email]').forEach(function (a) {
      a.href = 'mailto:' + cfg.email;
      a.textContent = cfg.email;
    });
    if (cfg.endpoint && note) note.textContent = 'We reply to every inquiry, usually within two business days.';

    // Buttons like "Start a Film Inquiry" preselect the matching option
    document.querySelectorAll('a[data-type]').forEach(function (a) {
      a.addEventListener('click', function () {
        const r = form.querySelector('input[name="type"][value="' + a.dataset.type + '"]');
        if (r) r.checked = true;
      });
    });

    const show = function (msg) { status.textContent = msg; status.classList.add('is-shown'); };
    const clean = function (t) { return t.replace('*', '').replace(/\s+/g, ' ').trim(); };
    const labelOf = function (el) {
      if ((el.type === 'radio' || el.type === 'checkbox') && el.closest('fieldset')) {
        return clean(el.closest('fieldset').querySelector('legend').textContent);
      }
      const lab = el.id && form.querySelector('label[for="' + el.id + '"]');
      return lab ? clean(lab.textContent) : el.name;
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const d = new FormData(form);
      const lines = [];
      const notes = [];
      const seen = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || seen[el.name]) return;
        seen[el.name] = true;
        const value = d.getAll(el.name).filter(Boolean).join(', ');
        if (el.tagName === 'TEXTAREA') notes.push(value);
        else lines.push(labelOf(el) + ': ' + (value || '—'));
      });

      if (cfg.endpoint) {
        fetch(cfg.endpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
          .then(function (r) {
            if (!r.ok) throw new Error(r.status);
            form.reset();
            show('Thank you. Your message has been sent, and we’ll be in touch.');
          })
          .catch(function () {
            show('Something went wrong sending the form. Please email ' + cfg.email + ' directly.');
          });
        return;
      }

      const subject = [cfg.subject, d.get('type'), d.get('name')].filter(Boolean).join(' — ');
      window.location.href = 'mailto:' + cfg.email +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.concat([''], notes).join('\n'));
      show('Your email app should now be open with your message filled in. Just press send. If nothing opened, email ' + cfg.email + '.');
    });
  }
})();
