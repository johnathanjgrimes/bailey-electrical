/* Bailey Electrical – shared site script: menu, enquiry sending, postcode area check. */
(function () {
  var C = window.BE_CONFIG || {};
  var BE = (window.BE = window.BE || {});

  // ---- Mobile menu -------------------------------------------------------
  var mb = document.getElementById('menu-btn'), mm = document.getElementById('mobile-menu');
  if (mb && mm) {
    mb.addEventListener('click', function () { var hidden = mm.classList.toggle('hidden'); mb.setAttribute('aria-expanded', String(!hidden)); });
    mm.addEventListener('click', function (e) { if (e.target.tagName === 'A') mm.classList.add('hidden'); });
  }
  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

  // ---- Postcode → distance from Cardiff (postcodes.io, free, no key) ---------
  function miles(a, b, c, d) {
    var R = 3958.8, r = Math.PI / 180, dLat = (c - a) * r, dLng = (d - b) * r;
    var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a * r) * Math.cos(c * r) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  var cache = {};
  BE.checkPostcode = function (raw) {
    var pc = String(raw || '').toUpperCase().replace(/\s+/g, '');
    if (pc.length < 2) return Promise.resolve(null);
    if (cache[pc]) return Promise.resolve(cache[pc]);
    var full = pc.length >= 5 && /\d[A-Z]{2}$/.test(pc);
    var url = full ? 'https://api.postcodes.io/postcodes/' + encodeURIComponent(pc) : 'https://api.postcodes.io/outcodes/' + encodeURIComponent(pc);
    return fetch(url).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!j || !j.result || j.result.latitude == null) return null;
      var base = C.base || { lat: 51.4816, lng: -3.1791 };
      var m = miles(base.lat, base.lng, j.result.latitude, j.result.longitude);
      var place = j.result.admin_district ? (Array.isArray(j.result.admin_district) ? j.result.admin_district[0] : j.result.admin_district) : '';
      var tier = m <= (C.coreRadiusMiles || 12) ? 'core' : m <= (C.serviceRadiusMiles || 22) ? 'area' : 'far';
      var res = { miles: Math.round(m), place: place, tier: tier };
      cache[pc] = res; return res;
    }).catch(function () { return null; });
  };
  BE.areaMessage = function (res) {
    if (!res) return '';
    var where = res.place ? res.place + ', ' : '';
    if (res.tier === 'core') return '<i class="fas fa-circle-check text-green-600 mr-1"></i> ' + where + 'about ' + res.miles + ' miles from Cardiff &ndash; right in our area.';
    if (res.tier === 'area') return '<i class="fas fa-circle-check text-green-600 mr-1"></i> ' + where + 'about ' + res.miles + ' miles from Cardiff &ndash; within the area we cover.';
    return '<i class="fas fa-route text-amber-600 mr-1"></i> ' + where + 'about ' + res.miles + ' miles from Cardiff. We travel this far for larger projects such as rewires, extensions and renovations.';
  };
  document.querySelectorAll('[data-postcode-check]').forEach(function (inp) {
    var out = document.getElementById(inp.getAttribute('data-postcode-check'));
    var t;
    function run() {
      BE.checkPostcode(inp.value).then(function (res) {
        inp.dataset.miles = res ? res.miles : '';
        if (out) out.innerHTML = BE.areaMessage(res);
      });
    }
    inp.addEventListener('blur', run);
    inp.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 700); });
  });

  // ---- Sending enquiries -------------------------------------------------------
  // Uses Web3Forms when an access key is configured (free, works on GitHub Pages),
  // otherwise opens the visitor's email app with everything filled in.
  BE.send = function (subject, bodyText, fields) {
    function mailto() {
      window.location.href = 'mailto:' + C.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(bodyText);
      return Promise.resolve({ ok: true, via: 'email' });
    }
    if (!C.web3formsKey) { BE.track('generate_lead', { form: subject.split(':')[0], via: 'email' }); return mailto(); }
    var payload = Object.assign({ access_key: C.web3formsKey, subject: subject, from_name: 'Bailey Electrical website', message: bodyText, botcheck: '' }, fields || {});
    return fetch('https://api.web3forms.com/submit', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload)
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (j && j.success) { BE.track('generate_lead', { form: subject.split(':')[0] }); return { ok: true, via: 'form' }; }
      return mailto();
    }).catch(mailto);
  };
  BE.track = function (name, params) {
    try { if (window.gtag) window.gtag('event', name, params || {}); } catch (e) {}
    try { if (window.posthog) window.posthog.capture(name, params || {}); } catch (e) {}
  };

  // Phone and email taps are leads too
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
    if (a) BE.track(a.href.indexOf('tel:') === 0 ? 'phone_click' : 'email_click', { page: location.pathname });
  });

  // ---- Generic enquiry forms (class="enquiry-form") ------------------------------
  document.querySelectorAll('form.enquiry-form').forEach(function (f) {
    try {
      var qs = new URLSearchParams(location.search);
      if (qs.get('job') && f.elements.job) Array.prototype.forEach.call(f.elements.job.options, function (o) { if (o.text === qs.get('job')) f.elements.job.value = o.value; });
      if (qs.get('details') && f.elements.details) f.elements.details.value = qs.get('details');
      if (qs.get('customer') && f.elements.customer) f.elements.customer.value = qs.get('customer');
    } catch (err) {}
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = f.querySelector('.form-msg');
      if (f.elements.botcheck && f.elements.botcheck.checked) return;
      var missing = Array.prototype.filter.call(f.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
      if (missing.length) { msg.textContent = 'Please fill in the fields marked *.'; msg.className = 'form-msg text-sm text-red-600'; missing[0].focus(); return; }
      var lines = [], fields = {};
      Array.prototype.forEach.call(f.querySelectorAll('[data-label]'), function (el) {
        var v;
        if (el.type === 'checkbox') { if (!el.checked) return; v = el.value; }
        else v = el.value.trim();
        if (!v) return;
        var k = el.getAttribute('data-label');
        fields[k] = fields[k] ? fields[k] + ', ' + v : v;
      });
      var pcEl = f.querySelector('[data-postcode-check]');
      if (pcEl && pcEl.dataset.miles) fields['Distance from Cardiff'] = pcEl.dataset.miles + ' miles';
      Object.keys(fields).forEach(function (k) { lines.push(k + ': ' + fields[k]); });
      var subject = (f.getAttribute('data-subject') || 'Enquiry') + ': ' + (fields['Type of work'] || '') + ' - ' + (fields['Postcode'] || '').toUpperCase();
      var btn = f.querySelector('button[type=submit]'); if (btn) btn.disabled = true;
      msg.textContent = 'Sending…'; msg.className = 'form-msg text-sm text-gray-600';
      BE.send(subject, lines.join('\n'), fields).then(function (r) {
        if (btn) btn.disabled = false;
        if (r.via === 'form') {
          f.innerHTML = '<div class="sm:col-span-2 text-center py-8"><i class="fas fa-circle-check text-green-600 text-5xl mb-4"></i><h3 class="text-2xl font-bold text-gray-900 mb-2">Thanks &ndash; we’ve got your enquiry</h3><p class="text-gray-600">We’ll be in touch soon. If it’s urgent, call ' + C.phone + '.</p></div>';
        } else {
          msg.textContent = 'Your email app should open now with the details filled in. If it doesn’t, call us on ' + C.phone + '.'; msg.className = 'form-msg text-sm text-gray-600';
        }
      });
    });
  });

  // Pre-select customer type from buttons with data-customer
  document.querySelectorAll('[data-customer]').forEach(function (a) {
    a.addEventListener('click', function () { var s = document.querySelector('form.enquiry-form [name=customer]'); if (s) s.value = a.dataset.customer; });
  });
})();
