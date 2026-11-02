// Search for the Sponsorships, In the News and Special pages (built by tools/build_site.py).
// Each page's entries live in assets/data/<list>.json, as an array of objects:
//   { "date": "2026-10-16", "name": "...", "title": "...", "category": "...", "company": "...", "link": "https://..." }
// "name" is the organization or media outlet. "title" and "link" are optional.

// Dates are ISO strings (YYYY-MM-DD), so they compare correctly as text.
function matches(entry, f) {
  return (!f.from || entry.date >= f.from)
    && (!f.to || entry.date <= f.to)
    && (!f.name || entry.name === f.name)
    && (!f.category || entry.category === f.category)
    && (!f.company || entry.company === f.company);
}

function newestFirst(a, b) {
  return (b.date || '').localeCompare(a.date || '');
}

if (typeof module !== 'undefined') {
  module.exports = { matches, newestFirst };
} else {
  (function () {
    var form = document.getElementById('filters');
    var results = document.getElementById('results');
    var status = document.getElementById('status');
    var entries = [];

    function addOption(select, value) {
      var option = document.createElement('option');
      option.textContent = value;
      select.appendChild(option);
    }

    function render() {
      var f = Object.fromEntries(new FormData(form));
      var shown = entries.filter(function (entry) { return matches(entry, f); }).sort(newestFirst);
      results.replaceChildren.apply(results, shown.map(function (entry) {
        var li = document.createElement('li');
        var head = document.createElement('b');
        var headline = entry.title || entry.name;
        if (/^https?:/.test(entry.link || '')) {
          var a = document.createElement('a');
          a.href = entry.link;
          a.target = '_blank';
          a.rel = 'noopener';
          a.textContent = headline;
          head.appendChild(a);
        } else {
          head.textContent = headline;
        }
        var meta = document.createElement('small');
        meta.textContent = [entry.date, entry.title && entry.name, entry.category, entry.company].filter(Boolean).join(' · ');
        li.append(head, meta);
        return li;
      }));
      status.textContent = entries.length ? (shown.length ? '' : 'Nothing matches these filters.') : 'Nothing listed yet.';
    }

    fetch(form.dataset.src).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (data) {
      entries = data;
      var names = Array.from(new Set(entries.map(function (entry) { return entry.name; }))).filter(Boolean).sort();
      names.forEach(function (name) { addOption(form.elements.name, name); });
      // Menu links pass ?category=... to open the page filtered
      var params = new URLSearchParams(location.search);
      ['name', 'category', 'company'].forEach(function (key) {
        var value = params.get(key);
        if (value && Array.from(form.elements[key].options).some(function (o) { return o.value === value; })) {
          form.elements[key].value = value;
        }
      });
      form.addEventListener('input', render);
      form.addEventListener('reset', function () { setTimeout(render); });
      render();
    }).catch(function () {
      status.textContent = 'The list could not be loaded. Please try again.';
    });
  })();
}
