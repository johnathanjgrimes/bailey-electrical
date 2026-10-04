(function () {
  var CFG = window.BE_CONFIG || {}, PHONE = CFG.phone || '', PR = window.BE_PRICING || { enabled: false };
  var S = {
    miles: null, type: null, beds: 3, age: null, scope: null, occupancy: null,
    partial: {}, rooms: [], extras: {}, name: '', phone: '', email: '', postcode: '', when: 'Within a month', notes: ''
  };
  var TYPES = [['Flat', 'fa-building'], ['Terraced house', 'fa-house'], ['Semi-detached house', 'fa-house-chimney'], ['Detached house', 'fa-house-chimney-window'], ['Bungalow', 'fa-house-flag']];
  var AGES = ['Before 1960', '1960 – 1990', 'After 1990', 'Not sure'];
  var SCOPES = [['Full rewire', 'The whole property, including a new consumer unit.'], ['Partial rewire', 'Just some rooms or circuits.'], ['Not sure yet', 'We’ll advise when we visit.']];
  var OCC = ['We’ll be living in it', 'It’s empty', 'It’s mid-renovation'];
  var PARTIAL_ROOMS = ['Kitchen', 'Living room', 'Dining room', 'Bedrooms', 'Bathroom', 'Hallway & landing', 'Loft', 'Garage / outbuilding', 'Garden'];
  var LIGHTS = ['Standard ceiling lights', 'Downlights', 'Downlights + LED feature lighting'];
  var EXTRAS = [
    ['cu', 'New consumer unit', 'Modern metal board with RCBO protection', 'fa-bolt'],
    ['alarms', 'Mains smoke & heat alarms', 'Interlinked, with battery back-up', 'fa-bell'],
    ['usb', 'USB sockets', 'In bedrooms, kitchen and living room', 'fa-plug'],
    ['cooker', 'Cooker / hob circuit', 'Dedicated circuit for an electric oven or induction hob', 'fa-fire-burner'],
    ['shower', 'Electric shower circuit', 'Dedicated high-power circuit', 'fa-shower'],
    ['fans', 'Extractor fans', 'Kitchen and bathroom', 'fa-fan'],
    ['ufh', 'Electric underfloor heating', 'Bathroom, kitchen or extension', 'fa-temperature-arrow-up'],
    ['data', 'TV & data points', 'Aerial and network points in chosen rooms', 'fa-wifi'],
    ['outlight', 'Outdoor lighting', 'Patio, garden, steps or driveway', 'fa-tree'],
    ['outsocket', 'Outdoor socket', 'Weatherproof socket for the garden', 'fa-plug-circle-check'],
    ['office', 'Garden office / outbuilding supply', 'New supply to a garden room or garage', 'fa-warehouse']
  ];
  // Sockets aren't allowed in rooms with a bath or shower
  function noSockets(r) { return /^(Bathroom|En-suite)/.test(r.n); }
  var STEPS = ['Property', 'Scope', 'Rooms', 'Extras', 'Your details'];
  var step = 0;

  function defaultRooms() {
    var r = [{ n: 'Kitchen', s: 6, l: 1 }, { n: 'Living room', s: 5, l: 0 }];
    if (S.beds >= 3 && S.type !== 'Flat') r.push({ n: 'Dining room', s: 3, l: 0 });
    for (var i = 1; i <= S.beds; i++) r.push({ n: 'Bedroom ' + i, s: i === 1 ? 4 : 3, l: 0 });
    r.push({ n: 'Bathroom', s: 0, l: 1 });
    r.push({ n: S.type === 'Flat' || S.type === 'Bungalow' ? 'Hallway' : 'Hallway & landing', s: 2, l: 0 });
    return r;
  }
  function roomsFromPartial() {
    var r = [];
    PARTIAL_ROOMS.forEach(function (n) {
      if (!S.partial[n]) return;
      if (n === 'Bedrooms') { for (var i = 1; i <= S.beds; i++) r.push({ n: 'Bedroom ' + i, s: 3, l: 0 }); }
      else if (n === 'Garden') { S.extras.outlight = true; }
      else r.push({ n: n, s: { 'Kitchen': 6, 'Living room': 5, 'Dining room': 3, 'Bathroom': 0, 'Loft': 3, 'Garage / outbuilding': 2 }[n] || 2, l: n === 'Kitchen' || n === 'Bathroom' ? 1 : 0 });
    });
    return r;
  }
  function el(h) { var d = document.createElement('div'); d.innerHTML = h.trim(); return d.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function choice(name, label, sub, icon, selected) {
    return '<button type="button" data-' + name + '="' + esc(label) + '" class="qb-choice text-left rounded-xl border-2 p-4 transition ' +
      (selected ? 'border-amber-500 bg-amber-50' : 'border-slate-200 hover:border-amber-300 bg-white') + '" aria-pressed="' + (selected ? 'true' : 'false') + '">' +
      (icon ? '<i class="fas ' + icon + ' text-amber-500 text-2xl mb-2 block" aria-hidden="true"></i>' : '') +
      '<span class="block font-bold text-gray-900">' + esc(label) + '</span>' + (sub ? '<span class="block text-sm text-gray-500 mt-1">' + esc(sub) + '</span>' : '') + '</button>';
  }
  function nav(canNext, nextLabel) {
    return '<div class="flex justify-between items-center mt-8 pt-6 border-t border-slate-200">' +
      (step > 0 ? '<button type="button" id="qb-back" class="px-5 py-3 rounded-lg font-semibold text-gray-700 hover:bg-slate-100"><i class="fas fa-arrow-left mr-2" aria-hidden="true"></i>Back</button>' : '<span></span>') +
      '<button type="button" id="qb-next" class="cta-button text-white px-7 py-3 rounded-lg font-bold ' + (canNext ? '' : 'opacity-50 cursor-not-allowed') + '"' + (canNext ? '' : ' disabled') + '>' + (nextLabel || 'Next') + ' <i class="fas fa-arrow-right ml-2" aria-hidden="true"></i></button></div>';
  }

  function renderProgress() {
    var p = document.getElementById('qb-progress');
    p.innerHTML = STEPS.map(function (s, i) {
      var done = i < step, cur = i === step;
      return '<li class="flex-1 flex flex-col items-center relative">' +
        (i > 0 ? '<span class="absolute top-4 right-1/2 w-full h-0.5 ' + (i <= step ? 'bg-amber-500' : 'bg-slate-300') + '" aria-hidden="true"></span>' : '') +
        '<span class="relative z-10 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ' +
        (done ? 'bg-slate-900 text-white' : cur ? 'bg-amber-500 text-white' : 'bg-white border-2 border-slate-300 text-slate-400') + '">' + (done ? '<i class="fas fa-check" aria-hidden="true"></i>' : (i + 1)) + '</span>' +
        '<span class="mt-2 text-xs ' + (cur ? 'text-gray-900 font-semibold' : 'text-gray-500') + ' hidden sm:block">' + s + '</span></li>';
    }).join('');
  }

  function renderSummary() {
    var out = [];
    function row(k, v) { out.push('<div class="flex justify-between gap-3"><span class="text-gray-500">' + k + '</span><span class="font-semibold text-right">' + esc(v) + '</span></div>'); }
    if (S.type) row('Property', S.type + (S.type ? ', ' + S.beds + (S.beds >= 5 ? '+' : '') + ' bed' : ''));
    if (S.age) row('Built', S.age);
    if (S.scope) row('Scope', S.scope);
    if (S.occupancy) row('During work', S.occupancy);
    if (S.rooms.length) {
      var sockets = S.rooms.reduce(function (a, r) { return a + r.s; }, 0);
      row('Rooms', S.rooms.length);
      row('Double sockets', sockets);
      var dl = S.rooms.filter(function (r) { return r.l > 0; }).length;
      if (dl) row('Rooms with downlights', dl);
      var wl = S.rooms.filter(function (r) { return r.w; }).length;
      if (wl) row('Rooms with wall lights', wl);
    }
    var ex = EXTRAS.filter(function (e) { return S.extras[e[0]]; }).map(function (e) { return e[1]; });
    if (ex.length) out.push('<div><span class="text-gray-500 block mb-1">Extras</span><ul class="space-y-1">' + ex.map(function (x) { return '<li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>' + esc(x) + '</li>'; }).join('') + '</ul></div>');
    var est = estimate();
    if (est) out.push('<div class="rounded-lg bg-amber-50 border border-amber-200 p-3 mt-2"><span class="block text-xs uppercase tracking-wide text-amber-700 font-semibold">Guide price</span><span class="block text-xl font-bold text-gray-900">' + gbp(est.lo) + ' \u2013 ' + gbp(est.hi) + '</span><span class="block text-xs text-gray-500">' + (PR.vatIncluded ? 'Including VAT. ' : 'Excluding VAT. ') + 'Confirmed after a survey visit.</span></div>');
    document.getElementById('qb-summary').innerHTML = out.length ? out.join('') : '<p class="text-gray-500">Your choices will appear here as you go.</p>';
  }

  function render() {
    renderProgress(); renderSummary();
    var P = document.getElementById('qb-panel'), h = '';
    if (step === 0) {
      h += '<h2 class="text-2xl font-bold text-gray-900 mb-1">What type of property is it?</h2><p class="text-gray-500 mb-6">Pick the closest match.</p>';
      h += '<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">' + TYPES.map(function (t) { return choice('type', t[0], '', t[1], S.type === t[0]); }).join('') + '</div>';
      h += '<h3 class="font-bold text-gray-900 mb-3">How many bedrooms?</h3><div class="flex flex-wrap gap-2 mb-8">' +
        [1, 2, 3, 4, 5].map(function (b) { return '<button type="button" data-beds="' + b + '" class="w-14 h-12 rounded-lg border-2 font-bold ' + (S.beds === b ? 'border-amber-500 bg-amber-50' : 'border-slate-200 bg-white hover:border-amber-300') + '" aria-pressed="' + (S.beds === b) + '">' + b + (b === 5 ? '+' : '') + '</button>'; }).join('') + '</div>';
      h += '<h3 class="font-bold text-gray-900 mb-3">Roughly when was it built?</h3><div class="grid grid-cols-2 sm:grid-cols-4 gap-3">' + AGES.map(function (a) { return choice('age', a, '', '', S.age === a); }).join('') + '</div>';
      h += nav(!!(S.type && S.age));
    } else if (step === 1) {
      h += '<h2 class="text-2xl font-bold text-gray-900 mb-1">Full or partial rewire?</h2><p class="text-gray-500 mb-6">Not sure? That’s fine &mdash; we’ll check when we visit.</p>';
      h += '<div class="grid sm:grid-cols-3 gap-3 mb-8">' + SCOPES.map(function (s) { return choice('scope', s[0], s[1], '', S.scope === s[0]); }).join('') + '</div>';
      if (S.scope === 'Partial rewire') {
        h += '<h3 class="font-bold text-gray-900 mb-3">Which areas?</h3><div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-8">' + PARTIAL_ROOMS.map(function (r) {
          return '<label class="flex items-center gap-3 rounded-lg border border-slate-200 p-3 cursor-pointer hover:border-amber-300"><input type="checkbox" data-partial="' + esc(r) + '" class="w-5 h-5 accent-amber-500"' + (S.partial[r] ? ' checked' : '') + '><span>' + esc(r) + '</span></label>';
        }).join('') + '</div>';
      }
      h += '<h3 class="font-bold text-gray-900 mb-3">Will anyone be living there during the work?</h3><div class="grid sm:grid-cols-3 gap-3">' + OCC.map(function (o) { return choice('occ', o, '', '', S.occupancy === o); }).join('') + '</div>';
      var partialOk = S.scope !== 'Partial rewire' || Object.keys(S.partial).some(function (k) { return S.partial[k]; });
      h += nav(!!(S.scope && S.occupancy && partialOk));
    } else if (step === 2) {
      h += '<h2 class="text-2xl font-bold text-gray-900 mb-1">Sockets &amp; lighting, room by room</h2><p class="text-gray-500 mb-6">We’ve suggested a typical number of double sockets. Adjust to suit how you use each room.</p>';
      h += '<div class="space-y-3">' + S.rooms.map(function (r, i) {
        return '<div class="rounded-xl border border-slate-200 p-4 grid sm:grid-cols-12 gap-3 items-center">' +
          '<div class="sm:col-span-4 font-bold text-gray-900">' + esc(r.n) + (i >= 0 ? ' <button type="button" data-remove="' + i + '" class="ml-2 text-xs font-normal text-gray-400 hover:text-red-600" aria-label="Remove ' + esc(r.n) + '">remove</button>' : '') + '</div>' +
          (noSockets(r)
            ? '<div class="sm:col-span-4 text-sm text-gray-500"><i class="fas fa-ban text-slate-400 mr-2" aria-hidden="true"></i>No sockets &ndash; not allowed in bathrooms</div>'
            : '<div class="sm:col-span-4 flex items-center gap-2"><span class="text-sm text-gray-500 w-16">Sockets</span>' +
              '<button type="button" data-dec="' + i + '" class="w-9 h-9 rounded-lg border border-slate-300 font-bold hover:bg-slate-100" aria-label="Fewer sockets in ' + esc(r.n) + '">&minus;</button>' +
              '<span class="w-8 text-center font-bold" aria-live="polite">' + r.s + '</span>' +
              '<button type="button" data-inc="' + i + '" class="w-9 h-9 rounded-lg border border-slate-300 font-bold hover:bg-slate-100" aria-label="More sockets in ' + esc(r.n) + '">+</button></div>') +
          '<div class="sm:col-span-4"><label class="sr-only" for="light-' + i + '">Lighting in ' + esc(r.n) + '</label><select id="light-' + i + '" data-light="' + i + '" class="field">' +
          LIGHTS.map(function (l, j) { return '<option value="' + j + '"' + (r.l === j ? ' selected' : '') + '>' + l + '</option>'; }).join('') + '</select>' +
          (noSockets(r) ? '' : '<label class="mt-2 flex items-center gap-2 text-sm text-gray-700 cursor-pointer"><input type="checkbox" data-wall="' + i + '" class="w-4 h-4 accent-amber-500"' + (r.w ? ' checked' : '') + '>Add wall lights (extra)</label>') +
          '</div></div>';
      }).join('') + '</div>';
      h += '<div class="mt-4 flex flex-wrap gap-2 items-center"><span class="text-sm text-gray-500 mr-2">Add a room:</span>' +
        ['Utility room', 'Study / office', 'Conservatory', 'Loft', 'Garage', 'WC / cloakroom', 'En-suite'].map(function (n) { return '<button type="button" data-add="' + n + '" class="text-sm rounded-full border border-slate-300 px-3 py-1 hover:border-amber-400 hover:bg-amber-50">+ ' + n + '</button>'; }).join('') + '</div>';
      h += nav(S.rooms.length > 0);
    } else if (step === 3) {
      h += '<h2 class="text-2xl font-bold text-gray-900 mb-1">Anything else?</h2><p class="text-gray-500 mb-6">A rewire is the cheapest time to add these, before the walls are made good.</p>';
      h += '<div class="grid sm:grid-cols-2 gap-3">' + EXTRAS.map(function (e) {
        var on = !!S.extras[e[0]];
        return '<button type="button" data-extra="' + e[0] + '" class="text-left rounded-xl border-2 p-4 flex gap-3 items-start transition ' + (on ? 'border-amber-500 bg-amber-50' : 'border-slate-200 bg-white hover:border-amber-300') + '" aria-pressed="' + on + '">' +
          '<i class="fas ' + e[3] + ' text-amber-500 text-xl mt-1 w-6 text-center" aria-hidden="true"></i><span><span class="block font-bold text-gray-900">' + e[1] + '</span><span class="block text-sm text-gray-500">' + e[2] + '</span></span>' +
          '<i class="fas ' + (on ? 'fa-square-check text-amber-500' : 'fa-square text-slate-300') + ' ml-auto text-xl" aria-hidden="true"></i></button>';
      }).join('') + '</div>';
      h += nav(true);
    } else if (step === 4) {
      h += '<h2 class="text-2xl font-bold text-gray-900 mb-1">Where should we send your quote?</h2><p class="text-gray-500 mb-6">We’ll get in touch to arrange a visit and give you a fixed written price.</p>';
      h += '<div class="grid sm:grid-cols-2 gap-4">' +
        '<div><label for="qb-name" class="block text-sm font-semibold mb-1">Name *</label><input id="qb-name" data-f="name" class="field" autocomplete="name" value="' + esc(S.name) + '"></div>' +
        '<div><label for="qb-phone" class="block text-sm font-semibold mb-1">Phone *</label><input id="qb-phone" data-f="phone" type="tel" class="field" autocomplete="tel" value="' + esc(S.phone) + '"></div>' +
        '<div><label for="qb-email" class="block text-sm font-semibold mb-1">Email</label><input id="qb-email" data-f="email" type="email" class="field" autocomplete="email" value="' + esc(S.email) + '"></div>' +
        '<div><label for="qb-postcode" class="block text-sm font-semibold mb-1">Property postcode *</label><input id="qb-postcode" data-f="postcode" class="field" autocomplete="postal-code" placeholder="e.g. CF14 4AA" value="' + esc(S.postcode) + '"><p id="qb-area" class="text-sm text-gray-600 mt-2"></p></div>' +
        '<div><label for="qb-when" class="block text-sm font-semibold mb-1">When do you need it?</label><select id="qb-when" data-f="when" class="field">' +
        ['Within a month', '1–3 months', '3+ months / planning stage', 'Just getting prices'].map(function (w) { return '<option' + (S.when === w ? ' selected' : '') + '>' + w + '</option>'; }).join('') + '</select></div>' +
        '<div class="sm:col-span-2"><label for="qb-notes" class="block text-sm font-semibold mb-1">Anything else we should know?</label><textarea id="qb-notes" data-f="notes" rows="3" class="field" placeholder="e.g. new kitchen going in, loft conversion planned, access notes">' + esc(S.notes) + '</textarea></div></div>';
      h += '<p id="qb-msg" class="text-sm text-gray-500 mt-4" role="status"></p>';
      h += '<div class="flex flex-wrap justify-between items-center gap-3 mt-8 pt-6 border-t border-slate-200">' +
        '<button type="button" id="qb-back" class="px-5 py-3 rounded-lg font-semibold text-gray-700 hover:bg-slate-100"><i class="fas fa-arrow-left mr-2" aria-hidden="true"></i>Back</button>' +
        '<div class="flex flex-wrap gap-3"><button type="button" id="qb-copy" class="px-5 py-3 rounded-lg font-semibold border-2 border-slate-300 hover:border-amber-400"><i class="fas fa-copy mr-2" aria-hidden="true"></i>Copy summary</button>' +
        '<button type="button" id="qb-send" class="cta-button text-white px-7 py-3 rounded-lg font-bold"><i class="fas fa-paper-plane mr-2" aria-hidden="true"></i>Send for a quote</button></div></div>';
    }
    P.innerHTML = h;
    wire(P);
  }

  function spec() {
    var L = [];
    L.push('REWIRE QUOTE REQUEST');
    L.push('Name: ' + S.name, 'Phone: ' + S.phone, 'Email: ' + (S.email || '-'), 'Postcode: ' + S.postcode.toUpperCase(), 'Timescale: ' + S.when, '');
    L.push('Property: ' + S.type + ', ' + S.beds + (S.beds >= 5 ? '+' : '') + ' bedrooms, built ' + S.age);
    L.push('Scope: ' + S.scope + (S.scope === 'Partial rewire' ? ' (' + Object.keys(S.partial).filter(function (k) { return S.partial[k]; }).join(', ') + ')' : ''));
    L.push('During work: ' + S.occupancy, '');
    L.push('ROOMS (double sockets / lighting)');
    S.rooms.forEach(function (r) { L.push('- ' + r.n + ': ' + (noSockets(r) ? 'no sockets' : r.s + ' sockets') + ', ' + LIGHTS[r.l] + (r.w ? ' + wall lights' : '')); });
    L.push('Total double sockets: ' + S.rooms.reduce(function (a, r) { return a + r.s; }, 0), '');
    var ex = EXTRAS.filter(function (e) { return S.extras[e[0]]; }).map(function (e) { return e[1]; });
    L.push('EXTRAS: ' + (ex.length ? ex.join(', ') : 'none'));
    var est = estimate(); if (est) L.push('', 'Guide price shown: ' + gbp(est.lo) + ' - ' + gbp(est.hi));
    if (S.miles) L.push('Distance from Cardiff: ~' + S.miles + ' miles');
    if (S.notes) L.push('', 'NOTES: ' + S.notes);
    return L.join('\n');
  }

  function estimate() {
    if (!PR.enabled || !S.type || !S.rooms.length) return null;
    var t = (PR.base[S.type] || 0) + S.rooms.length * (PR.perRoom || 0);
    S.rooms.forEach(function (r) { t += r.s * (PR.perSocket || 0) + (PR.lighting[LIGHTS[r.l]] || 0) + (r.w ? PR.perRoomWallLights || 0 : 0); });
    EXTRAS.forEach(function (e) { if (S.extras[e[0]]) t += PR.extras[e[0]] || 0; });
    if (S.occupancy === OCC[0]) t *= 1 + (PR.occupiedUplift || 0);
    if (S.scope === 'Not sure yet' || t <= 0) return null;
    var sp = PR.spread || 0.15, lo = Math.round(t * (1 - sp) / 50) * 50, hi = Math.round(t * (1 + sp) / 50) * 50;
    return { lo: lo, hi: hi };
  }
  function gbp(n) { return '\u00a3' + n.toLocaleString('en-GB'); }

  function wire(P) {
    P.querySelectorAll('[data-type]').forEach(function (b) { b.onclick = function () { S.type = b.dataset.type; render(); }; });
    P.querySelectorAll('[data-beds]').forEach(function (b) { b.onclick = function () { S.beds = +b.dataset.beds; render(); }; });
    P.querySelectorAll('[data-age]').forEach(function (b) { b.onclick = function () { S.age = b.dataset.age; render(); }; });
    P.querySelectorAll('[data-scope]').forEach(function (b) { b.onclick = function () { S.scope = b.dataset.scope; render(); }; });
    P.querySelectorAll('[data-occ]').forEach(function (b) { b.onclick = function () { S.occupancy = b.dataset.occ; render(); }; });
    P.querySelectorAll('[data-partial]').forEach(function (c) { c.onchange = function () { S.partial[c.dataset.partial] = c.checked; render(); }; });
    P.querySelectorAll('[data-inc]').forEach(function (b) { b.onclick = function () { S.rooms[+b.dataset.inc].s = Math.min(20, S.rooms[+b.dataset.inc].s + 1); render(); }; });
    P.querySelectorAll('[data-dec]').forEach(function (b) { b.onclick = function () { S.rooms[+b.dataset.dec].s = Math.max(0, S.rooms[+b.dataset.dec].s - 1); render(); }; });
    P.querySelectorAll('[data-light]').forEach(function (s) { s.onchange = function () { S.rooms[+s.dataset.light].l = +s.value; renderSummary(); }; });
    P.querySelectorAll('[data-wall]').forEach(function (c) { c.onchange = function () { S.rooms[+c.dataset.wall].w = c.checked; renderSummary(); }; });
    P.querySelectorAll('[data-remove]').forEach(function (b) { b.onclick = function () { S.rooms.splice(+b.dataset.remove, 1); render(); }; });
    P.querySelectorAll('[data-add]').forEach(function (b) { b.onclick = function () { var r = { n: b.dataset.add, s: 3, l: 0 }; if (noSockets(r)) r.s = 0; S.rooms.push(r); render(); }; });
    P.querySelectorAll('[data-extra]').forEach(function (b) { b.onclick = function () { S.extras[b.dataset.extra] = !S.extras[b.dataset.extra]; render(); }; });
    P.querySelectorAll('[data-f]').forEach(function (i) { i.oninput = i.onchange = function () { S[i.dataset.f] = i.value; }; });
    var pcIn = P.querySelector('#qb-postcode');
    if (pcIn && window.BE && BE.checkPostcode) {
      var pcT, pcRun = function () { BE.checkPostcode(pcIn.value).then(function (r) { S.miles = r ? r.miles : null; var o = P.querySelector('#qb-area'); if (o) o.innerHTML = BE.areaMessage(r); }); };
      pcIn.addEventListener('blur', pcRun); pcIn.addEventListener('input', function () { clearTimeout(pcT); pcT = setTimeout(pcRun, 700); });
      if (S.postcode) pcRun();
    }
    var back = P.querySelector('#qb-back'), next = P.querySelector('#qb-next');
    if (back) back.onclick = function () { step--; render(); top(); };
    if (next) next.onclick = function () {
      if (step === 1) {
        S.rooms = S.scope === 'Partial rewire' ? roomsFromPartial() : defaultRooms();
        if (S.scope !== 'Partial rewire') S.extras.cu = true;
      }
      step++; render(); top();
    };
    var send = P.querySelector('#qb-send'), copy = P.querySelector('#qb-copy'), msg = P.querySelector('#qb-msg');
    function valid() {
      if (!S.name.trim() || !S.phone.trim() || !S.postcode.trim()) { msg.textContent = 'Please add your name, phone number and postcode.'; msg.className = 'text-sm text-red-600 mt-4'; return false; }
      return true;
    }
    if (send) send.onclick = function () {
      if (!valid()) return;
      var subject = 'Rewire quote request - ' + S.type + ', ' + S.beds + ' bed - ' + S.postcode.toUpperCase();
      msg.textContent = 'Sending\u2026'; msg.className = 'text-sm text-gray-600 mt-4';
      BE.send(subject, spec(), { Name: S.name, Phone: S.phone, Email: S.email, Postcode: S.postcode, 'Type of work': 'Rewire (quote builder)' }).then(function (r) {
        if (r.via === 'form') {
          P.innerHTML = '<div class="text-center py-10"><i class="fas fa-circle-check text-green-600 text-5xl mb-4" aria-hidden="true"></i><h2 class="text-2xl font-bold text-gray-900 mb-2">Thanks ' + esc(S.name.split(' ')[0]) + ' \u2013 we\u2019ve got your rewire details</h2><p class="text-gray-600 max-w-md mx-auto">We\u2019ll look through everything and be in touch to arrange a survey visit. If it\u2019s urgent, call ' + PHONE + '.</p></div>';
        } else {
          msg.textContent = 'Your email app should open with everything filled in. If it doesn\u2019t, use \u201cCopy summary\u201d and text it to ' + PHONE + '.'; msg.className = 'text-sm text-gray-600 mt-4';
        }
      });
    };
    if (copy) copy.onclick = function () {
      var t = spec();
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
        msg.textContent = 'Copied. You can paste it into a text or WhatsApp to ' + PHONE + '.'; msg.className = 'text-sm text-gray-600 mt-4';
      }, function () { window.prompt('Copy your summary:', t); });
    };
  }
  function top() { var p = document.getElementById('qb-progress'); if (p && p.getBoundingClientRect().top < 0) p.scrollIntoView({ behavior: 'smooth' }); }
  render();
})();