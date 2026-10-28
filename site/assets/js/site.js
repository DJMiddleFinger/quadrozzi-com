/* Shared page behavior for GBX and Helping Hoof Initiative: phone menu and inquiry forms */
(function () {
  // Phone menu: the top-left button slides the sidebar in
  const toggle = document.querySelector('.menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const content = document.getElementById('content');
  if (toggle && sidebar) {
    const isOpen = function () { return document.body.classList.contains('nav-open'); };
    const setNav = function (open) {
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (content) content.inert = open;
    };
    toggle.addEventListener('click', function () { setNav(!isOpen()); });
    document.addEventListener('click', function (e) {
      if (isOpen() && !sidebar.contains(e.target) && !toggle.contains(e.target)) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) { setNav(false); toggle.focus(); }
    });
    matchMedia('(max-width: 900px)').addEventListener('change', function () { setNav(false); });
  }

  // Inquiry forms.
  // The page sets window.INQUIRY = { email, endpoint, subject } before loading this file.
  // With no endpoint, submitting opens the visitor's email app with every answer filled in.
  const form = document.querySelector('form[data-inquiry]');
  const cfg = window.INQUIRY;
  if (!form || !cfg) return;

  const status = form.querySelector('.form-status');
  const note = form.querySelector('.form-note');
  document.querySelectorAll('[data-inquiry-email]').forEach(function (a) {
    a.href = 'mailto:' + cfg.email;
    a.textContent = cfg.email;
  });
  if (cfg.endpoint && note) note.textContent = 'We reply to every inquiry, usually within two business days.';

  // Links like "Plan an event" arrive as ?type=Event or ?areas=… and preselect those options
  const params = new URLSearchParams(location.search);
  ['type', 'areas'].forEach(function (name) {
    const wanted = params.getAll(name);
    form.querySelectorAll('input[name="' + name + '"]').forEach(function (input) {
      if (wanted.indexOf(input.value) !== -1) input.checked = true;
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
          show('The form couldn’t be sent. Please email ' + cfg.email + ' directly.');
        });
      return;
    }

    const subject = [cfg.subject, d.get('type'), d.get('name')].filter(Boolean).join(' — ');
    window.location.href = 'mailto:' + cfg.email +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(lines.concat([''], notes).join('\n'));
    show('Your email app should now be open with your message filled in. Just press send. If nothing opened, email ' + cfg.email + '.');
  });
})();
