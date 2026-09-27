"""Interactive tools: Rewire Quote Builder and 'Do I need a rewire?' checker.

Each tool returns (body_html, script_js). Crawlable explanatory text sits below each tool
so search engines and AI assistants can read it even though the tool itself is JavaScript.
"""
from content import EMAIL, PHONE_DISPLAY, PHONE_TEL

# ---------------------------------------------------------------------------
# Rewire Quote Builder
# ---------------------------------------------------------------------------
QB_BODY = """
    <header class="hero-gradient text-white py-12 md:py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav aria-label="Breadcrumb" class="text-sm text-gray-400 mb-5"><a href="/" class="hover:text-amber-400">Home</a> <span class="mx-2">/</span> <span class="text-gray-200">Rewire quote builder</span></nav>
            <p class="text-amber-400 font-semibold tracking-wide uppercase text-sm mb-3">Free online tool</p>
            <h1 class="text-4xl md:text-5xl font-bold mb-4 leading-tight">Build your rewire quote</h1>
            <p class="text-lg text-gray-300 max-w-2xl">Tell us about your home room by room &mdash; sockets, lighting and extras &mdash; and we&rsquo;ll send back a proper written quote. It takes about two minutes.</p>
        </div>
    </header>

    <section class="bg-gray-50 py-10 md:py-14">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <ol id="qb-progress" class="flex items-center justify-between max-w-3xl mx-auto mb-10" aria-label="Progress"></ol>
            <div class="grid lg:grid-cols-3 gap-8 items-start">
                <div class="lg:col-span-2 card rounded-xl p-6 md:p-8" id="qb-panel" aria-live="polite"></div>
                <aside class="card rounded-xl p-6 lg:sticky lg:top-24">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="icon-tile w-11 h-11 rounded-lg flex items-center justify-center"><i class="fas fa-clipboard-list text-white" aria-hidden="true"></i></span>
                        <h2 class="font-bold text-gray-900 text-lg">Your rewire</h2>
                    </div>
                    <div id="qb-summary" class="text-sm text-gray-700 space-y-3"></div>
                    <p class="text-xs text-gray-500 mt-5 pt-4 border-t border-slate-200">Every home is different, so we&rsquo;ll confirm the scope and give you a fixed written price after a visit.</p>
                </aside>
            </div>
        </div>
    </section>
"""

QB_SCRIPT = r"""
<script>
(function () {
  var EMAIL = '__EMAIL__', PHONE = '__PHONE__';
  var S = {
    type: null, beds: 3, age: null, scope: null, occupancy: null,
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
    }
    var ex = EXTRAS.filter(function (e) { return S.extras[e[0]]; }).map(function (e) { return e[1]; });
    if (ex.length) out.push('<div><span class="text-gray-500 block mb-1">Extras</span><ul class="space-y-1">' + ex.map(function (x) { return '<li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>' + esc(x) + '</li>'; }).join('') + '</ul></div>');
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
          '<div class="sm:col-span-4 flex items-center gap-2"><span class="text-sm text-gray-500 w-16">Sockets</span>' +
          '<button type="button" data-dec="' + i + '" class="w-9 h-9 rounded-lg border border-slate-300 font-bold hover:bg-slate-100" aria-label="Fewer sockets in ' + esc(r.n) + '">&minus;</button>' +
          '<span class="w-8 text-center font-bold" aria-live="polite">' + r.s + '</span>' +
          '<button type="button" data-inc="' + i + '" class="w-9 h-9 rounded-lg border border-slate-300 font-bold hover:bg-slate-100" aria-label="More sockets in ' + esc(r.n) + '">+</button></div>' +
          '<div class="sm:col-span-4"><label class="sr-only" for="light-' + i + '">Lighting in ' + esc(r.n) + '</label><select id="light-' + i + '" data-light="' + i + '" class="field">' +
          LIGHTS.map(function (l, j) { return '<option value="' + j + '"' + (r.l === j ? ' selected' : '') + '>' + l + '</option>'; }).join('') + '</select></div></div>';
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
        '<div><label for="qb-postcode" class="block text-sm font-semibold mb-1">Property postcode *</label><input id="qb-postcode" data-f="postcode" class="field" autocomplete="postal-code" placeholder="e.g. CF14" value="' + esc(S.postcode) + '"></div>' +
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
    L.push('Name: ' + S.name, 'Phone: ' + S.phone, 'Postcode: ' + S.postcode.toUpperCase(), 'Timescale: ' + S.when, '');
    L.push('Property: ' + S.type + ', ' + S.beds + (S.beds >= 5 ? '+' : '') + ' bedrooms, built ' + S.age);
    L.push('Scope: ' + S.scope + (S.scope === 'Partial rewire' ? ' (' + Object.keys(S.partial).filter(function (k) { return S.partial[k]; }).join(', ') + ')' : ''));
    L.push('During work: ' + S.occupancy, '');
    L.push('ROOMS (double sockets / lighting)');
    S.rooms.forEach(function (r) { L.push('- ' + r.n + ': ' + r.s + ' sockets, ' + LIGHTS[r.l]); });
    L.push('Total double sockets: ' + S.rooms.reduce(function (a, r) { return a + r.s; }, 0), '');
    var ex = EXTRAS.filter(function (e) { return S.extras[e[0]]; }).map(function (e) { return e[1]; });
    L.push('EXTRAS: ' + (ex.length ? ex.join(', ') : 'none'));
    if (S.notes) L.push('', 'NOTES: ' + S.notes);
    return L.join('\n');
  }

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
    P.querySelectorAll('[data-remove]').forEach(function (b) { b.onclick = function () { S.rooms.splice(+b.dataset.remove, 1); render(); }; });
    P.querySelectorAll('[data-add]').forEach(function (b) { b.onclick = function () { S.rooms.push({ n: b.dataset.add, s: 3, l: 0 }); render(); }; });
    P.querySelectorAll('[data-extra]').forEach(function (b) { b.onclick = function () { S.extras[b.dataset.extra] = !S.extras[b.dataset.extra]; render(); }; });
    P.querySelectorAll('[data-f]').forEach(function (i) { i.oninput = i.onchange = function () { S[i.dataset.f] = i.value; }; });
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
      window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(spec());
      msg.textContent = 'Your email app should open with everything filled in. If it doesn’t, use “Copy summary” and text it to ' + PHONE + '.'; msg.className = 'text-sm text-gray-600 mt-4';
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
</script>
""".replace("__EMAIL__", EMAIL).replace("__PHONE__", PHONE_DISPLAY)

QB_SECTIONS = [
    ("What affects the cost of a rewire?", """
<p>Every rewire is priced on the property, but these are the things that make the biggest difference:</p>
<ul class="list">
<li><strong>Size of the property</strong> &mdash; the number of rooms and circuits.</li>
<li><strong>Number of sockets and lights</strong> &mdash; most older homes need far more sockets than they have.</li>
<li><strong>Lighting</strong> &mdash; downlights and LED feature lighting take longer than standard ceiling lights.</li>
<li><strong>Whether the house is empty</strong> &mdash; working around furniture and people takes longer than an empty or mid-renovation house.</li>
<li><strong>Access</strong> &mdash; floor types, lofts and solid walls all affect how cables are run.</li>
<li><strong>Extras</strong> &mdash; a new consumer unit, smoke and heat alarms, outdoor lighting, shower and cooker circuits.</li>
</ul>
<p>That&rsquo;s why the quote builder asks about each room. It gives us enough to understand the job before we visit, so the written quote you get is accurate.</p>"""),
    ("What happens after you send it?", """
<ol class="list">
<li>We look through your requirements and get in touch to arrange a visit.</li>
<li>We check the existing installation, access and anything that affects the work.</li>
<li>You get a fixed written quote with a clear scope of work.</li>
<li>We agree dates that work around you or your builder.</li>
</ol>"""),
]

QB_FAQ = [
    ("How much does it cost to rewire a house in Cardiff?",
     "The price depends mainly on the size of the property, how many sockets and lights you want, whether the house is occupied, and access. Use the quote builder to tell us what you need and we'll give you a fixed written quote after a visit."),
    ("How many sockets should each room have?",
     "As a rough guide: kitchens around six double sockets, living rooms four to six, main bedrooms three to four, other bedrooms two to three, and a couple in the hallway. It depends on how you use each room, which is why the builder lets you adjust them."),
    ("Is a new consumer unit included in a full rewire?",
     "Yes, a full rewire normally includes a new consumer unit, and the builder adds it automatically. For a partial rewire we'll check whether your existing board is suitable."),
    ("Can I use the quote builder for a partial rewire?",
     "Yes. Choose 'Partial rewire' and tick the areas you want doing, such as a kitchen, extension or loft."),
]

# ---------------------------------------------------------------------------
# Do I need a rewire? checker
# ---------------------------------------------------------------------------
RC_BODY = """
    <header class="hero-gradient text-white py-12 md:py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav aria-label="Breadcrumb" class="text-sm text-gray-400 mb-5"><a href="/" class="hover:text-amber-400">Home</a> <span class="mx-2">/</span> <span class="text-gray-200">Do I need a rewire?</span></nav>
            <p class="text-amber-400 font-semibold tracking-wide uppercase text-sm mb-3">Free 1-minute check</p>
            <h1 class="text-4xl md:text-5xl font-bold mb-4 leading-tight">Does my house need rewiring?</h1>
            <p class="text-lg text-gray-300 max-w-2xl">Answer seven quick questions about your home and we&rsquo;ll tell you whether your electrics are likely fine, due a check, or likely to need a rewire.</p>
        </div>
    </header>
    <section class="bg-gray-50 py-10 md:py-14">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="mb-6"><div class="flex justify-between text-sm text-gray-500 mb-2"><span id="rc-count"></span><span id="rc-pct"></span></div>
                <div class="h-2 bg-slate-200 rounded-full overflow-hidden"><div id="rc-bar" class="h-full bg-amber-500 transition-all" style="width:0%"></div></div></div>
            <div id="rc-panel" class="card rounded-xl p-6 md:p-8" aria-live="polite"></div>
            <p class="text-xs text-gray-500 mt-4 text-center">This is a guide, not an inspection. Only testing by a qualified electrician (an EICR) can confirm the condition of your wiring.</p>
        </div>
    </section>
"""

RC_SCRIPT = r"""
<script>
(function () {
  var Q = [
    { id: 'age', q: 'How old is the wiring, as far as you know?', opts: [
      ['Less than 25 years old', 0], ['25 – 40 years old', 1], ['Over 40 years, or original to an older house', 3], ['No idea', 1]] },
    { id: 'board', q: 'What does your fuse box look like?', help: 'It’s usually under the stairs, in a hallway cupboard or by the front door.', opts: [
      ['Modern unit with a row of switches and a “test” button', 0], ['Old board with pull-out fuses (with fuse wire inside)', 3], ['A mix of old boxes and switches', 2], ['Not sure', 1]] },
    { id: 'cable', q: 'If you’ve seen the cables (in the loft, under floors or at the fuse box), what are they like?', opts: [
      ['Grey or white plastic-covered', 0], ['Black rubber, fabric-covered, or metal-sheathed', 5], ['Haven’t seen them', 1]] },
    { id: 'sockets', q: 'What are your sockets and switches like?', multi: true, opts: [
      ['Round-pin sockets anywhere in the house', 5], ['Sockets fitted in skirting boards', 2], ['Brown or black (bakelite) switches and sockets', 2], ['Not enough sockets – extension leads everywhere', 1], ['A normal light switch inside the bathroom', 1], ['None of these', 0]] },
    { id: 'signs', q: 'Have you noticed any of these?', multi: true, opts: [
      ['Burning smell, scorch marks or sockets that feel warm', 10], ['A tingle or shock from a switch, socket or appliance', 10], ['Lights flickering or dimming', 1], ['Fuses blowing or the trip switch going regularly', 2], ['None of these', 0]] },
    { id: 'tested', q: 'When were the electrics last tested (an EICR)?', opts: [
      ['In the last 10 years, and it was satisfactory', -1], ['More than 10 years ago', 1], ['Never, or I don’t know', 1], ['It came back unsatisfactory', 3]] },
    { id: 'reno', q: 'Are you planning any building work?', opts: [
      ['Yes – extension, new kitchen or bathroom, or a renovation', 0], ['No, not at the moment', 0]] }
  ];
  var A = {}, i = 0;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function progress() {
    var n = Math.min(i, Q.length);
    document.getElementById('rc-count').textContent = i < Q.length ? 'Question ' + (i + 1) + ' of ' + Q.length : 'Your result';
    document.getElementById('rc-pct').textContent = Math.round(n / Q.length * 100) + '%';
    document.getElementById('rc-bar').style.width = (n / Q.length * 100) + '%';
  }
  function render() {
    progress();
    var P = document.getElementById('rc-panel');
    if (i >= Q.length) return result(P);
    var q = Q[i], sel = A[q.id] || (q.multi ? [] : null), h = '';
    h += '<h2 class="text-2xl font-bold text-gray-900 mb-2">' + q.q + '</h2>';
    h += '<p class="text-gray-500 mb-6">' + (q.help || (q.multi ? 'Tick all that apply.' : 'Choose one.')) + '</p><div class="space-y-3">';
    q.opts.forEach(function (o, k) {
      var on = q.multi ? sel.indexOf(k) > -1 : sel === k;
      h += '<button type="button" data-k="' + k + '" class="w-full text-left rounded-xl border-2 p-4 flex items-center gap-3 transition ' + (on ? 'border-amber-500 bg-amber-50' : 'border-slate-200 bg-white hover:border-amber-300') + '" aria-pressed="' + on + '">' +
        '<i class="fas ' + (q.multi ? (on ? 'fa-square-check' : 'fa-square') : (on ? 'fa-circle-dot' : 'fa-circle')) + ' ' + (on ? 'text-amber-500' : 'text-slate-300') + ' text-xl" aria-hidden="true"></i><span class="font-semibold text-gray-900">' + esc(o[0]) + '</span></button>';
    });
    h += '</div><div class="flex justify-between mt-8 pt-6 border-t border-slate-200">' +
      (i > 0 ? '<button type="button" id="rc-back" class="px-5 py-3 rounded-lg font-semibold text-gray-700 hover:bg-slate-100"><i class="fas fa-arrow-left mr-2" aria-hidden="true"></i>Back</button>' : '<span></span>');
    var ok = q.multi ? sel.length > 0 : sel !== null;
    h += '<button type="button" id="rc-next" class="cta-button text-white px-7 py-3 rounded-lg font-bold ' + (ok ? '' : 'opacity-50 cursor-not-allowed') + '"' + (ok ? '' : ' disabled') + '>' + (i === Q.length - 1 ? 'See my result' : 'Next') + ' <i class="fas fa-arrow-right ml-2" aria-hidden="true"></i></button></div>';
    P.innerHTML = h;
    P.querySelectorAll('[data-k]').forEach(function (b) {
      b.onclick = function () {
        var k = +b.dataset.k;
        if (q.multi) {
          var none = q.opts.length - 1, cur = (A[q.id] || []).slice();
          if (k === none) cur = [none];
          else { cur = cur.filter(function (x) { return x !== none; }); var p = cur.indexOf(k); if (p > -1) cur.splice(p, 1); else cur.push(k); }
          A[q.id] = cur;
        } else { A[q.id] = k; setTimeout(function () { i++; render(); }, 180); }
        render();
      };
    });
    var back = P.querySelector('#rc-back'), next = P.querySelector('#rc-next');
    if (back) back.onclick = function () { i--; render(); };
    if (next) next.onclick = function () { i++; render(); };
  }
  function score() {
    var s = 0, urgent = false;
    Q.forEach(function (q) {
      var a = A[q.id]; if (a === undefined || a === null) return;
      (q.multi ? a : [a]).forEach(function (k) { s += q.opts[k][1]; if (q.opts[k][1] >= 10) urgent = true; });
    });
    return { s: s, urgent: urgent };
  }
  function result(P) {
    var r = score(), reno = A.reno === 0, h, job, title, cls, icon, body, cta;
    var reasons = [];
    Q.forEach(function (q) { var a = A[q.id]; (q.multi ? (a || []) : [a]).forEach(function (k) { if (k !== null && k !== undefined && q.opts[k][1] >= 2) reasons.push(q.opts[k][0]); }); });
    if (r.urgent) {
      title = 'Get this checked urgently'; cls = 'bg-red-50 border-red-300'; icon = 'fa-triangle-exclamation text-red-600';
      body = 'A burning smell, scorch marks, warm sockets or a tingle from a switch can mean a dangerous fault. Stop using the affected socket or appliance, switch off that circuit at the fuse box if it’s safe to do so, and get a qualified electrician to look at it as soon as possible. Call us on __PHONE__ – if we can’t get to you quickly, we’ll tell you straight away so you can get someone who can.';
      job = 'Fault finding / repair'; cta = 'Call __PHONE__';
    } else if (r.s >= 6) {
      title = 'A rewire is likely'; cls = 'bg-amber-50 border-amber-300'; icon = 'fa-plug-circle-exclamation text-amber-600';
      body = 'Your answers include signs of old wiring or an out-of-date fuse box, which usually means a full or partial rewire. The next step is an inspection so we can confirm what’s needed and give you a fixed written quote.';
      job = 'Rewire (full or partial)'; cta = 'Build your rewire quote';
    } else if (r.s >= 2) {
      title = 'Your electrics are due a check'; cls = 'bg-sky-50 border-sky-300'; icon = 'fa-clipboard-check text-sky-600';
      body = 'Nothing you’ve told us points clearly to a rewire, but there are enough unknowns that an Electrical Installation Condition Report (EICR) is worth doing. It will show exactly what condition the wiring is in and whether anything needs attention.';
      job = 'EICR / landlord certificate'; cta = 'Book an EICR';
    } else {
      title = 'Your electrics sound in good shape'; cls = 'bg-green-50 border-green-300'; icon = 'fa-circle-check text-green-600';
      body = 'From your answers, your wiring sounds modern and well looked after. For owner-occupied homes an EICR is generally recommended every 10 years, so keep that in mind – and get in touch if anything changes.';
      job = 'EICR / landlord certificate'; cta = 'Get in touch';
    }
    h = '<div class="rounded-xl border-2 p-6 mb-6 ' + cls + '"><div class="flex items-start gap-4"><i class="fas ' + icon + ' text-3xl" aria-hidden="true"></i><div><h2 class="text-2xl font-bold text-gray-900 mb-2">' + title + '</h2><p class="text-gray-700 leading-relaxed">' + body + '</p></div></div></div>';
    if (reasons.length && !r.urgent) h += '<h3 class="font-bold text-gray-900 mb-2">What stood out</h3><ul class="list-disc pl-5 text-gray-700 space-y-1 mb-6">' + reasons.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>';
    if (reno && !r.urgent) h += '<div class="rounded-xl bg-slate-50 border border-slate-200 p-5 mb-6"><h3 class="font-bold text-gray-900 mb-1"><i class="fas fa-trowel-bricks text-amber-500 mr-2" aria-hidden="true"></i>Planning building work?</h3><p class="text-gray-600 text-sm">The best time to rewire or upgrade the electrics is before plastering and decorating. We can plan the electrics alongside your builder. <a href="/extensions-renovations-electrician-cardiff/" class="text-amber-700 font-semibold underline">Renovation electrics</a></p></div>';
    var details = 'From the "Do I need a rewire?" checker. Result: ' + title + '.' + (reasons.length ? ' Answers: ' + reasons.join('; ') + '.' : '') + (reno ? ' Planning building work.' : '');
    var href = r.urgent ? 'tel:__TEL__' : (job === 'Rewire (full or partial)' ? '/rewire-quote-builder/' : '/?job=' + encodeURIComponent(job) + '&details=' + encodeURIComponent(details) + '#quote');
    h += '<div class="flex flex-wrap gap-3"><a href="' + href + '" class="cta-button text-white px-7 py-3 rounded-lg font-bold">' + cta + ' <i class="fas fa-arrow-right ml-2" aria-hidden="true"></i></a>' +
      '<a href="tel:__TEL__" class="px-6 py-3 rounded-lg font-bold border-2 border-slate-300 hover:border-amber-400"><i class="fas fa-phone mr-2" aria-hidden="true"></i>__PHONE__</a>' +
      '<button type="button" id="rc-restart" class="px-5 py-3 rounded-lg font-semibold text-gray-600 hover:bg-slate-100">Start again</button></div>';
    P.innerHTML = h;
    P.querySelector('#rc-restart').onclick = function () { A = {}; i = 0; render(); };
  }
  render();
})();
</script>
""".replace("__PHONE__", PHONE_DISPLAY).replace("__TEL__", PHONE_TEL)

RC_SECTIONS = [
    ("Signs your house needs rewiring", """
<p>You can&rsquo;t tell for certain without testing, but these are the most common signs that a home&rsquo;s wiring is at the end of its life:</p>
<ul class="list">
<li><strong>Old cable types</strong> &mdash; black rubber, fabric-covered or lead-sheathed cables were used before the 1960s and the insulation becomes brittle with age.</li>
<li><strong>An old fuse box</strong> &mdash; a board with pull-out rewireable fuses and no RCD protection.</li>
<li><strong>Round-pin sockets</strong>, sockets in skirting boards, or brown and black bakelite switches.</li>
<li><strong>Warning signs</strong> &mdash; burning smells, scorch marks, warm sockets, flickering lights or regular tripping.</li>
<li><strong>Not enough sockets</strong> for modern life, with extension leads in every room.</li>
</ul>
<p>Red and black wires on their own aren&rsquo;t a problem &mdash; those were the standard colours in the UK until 2006, so plenty of sound installations still have them.</p>"""),
    ("How old is too old?", """
<p>There&rsquo;s no fixed expiry date, but PVC-insulated wiring installed from the 1960s onwards typically lasts a long time if it hasn&rsquo;t been damaged or overloaded. Wiring from before then, and any installation that has never been tested, is worth checking. An <a href="/eicr-landlord-certificates-cardiff/" class="text-amber-700 font-semibold underline">EICR</a> is the way to find out for sure.</p>"""),
    ("Rewire or just an EICR?", """
<p>If you&rsquo;re not sure, start with an Electrical Installation Condition Report. It tells you the condition of the whole installation and whether anything needs fixing. Sometimes the answer is a new consumer unit or a few repairs rather than a full rewire. If a rewire is needed, the report shows why, and you can use our <a href="/rewire-quote-builder/" class="text-amber-700 font-semibold underline">rewire quote builder</a> to plan it.</p>"""),
]

RC_FAQ = [
    ("How do I know if my house needs rewiring?",
     "Common signs are old rubber or fabric-covered cables, an old fuse box with rewireable fuses, round-pin sockets, scorch marks or warm sockets, and lights that flicker. The only way to know for sure is an Electrical Installation Condition Report (EICR) carried out by a qualified electrician."),
    ("Do red and black wires mean I need a rewire?",
     "Not on their own. Red and black were the standard UK wiring colours until 2006. What matters is the type and condition of the cable, which an EICR will check."),
    ("How often should house wiring be checked?",
     "For owner-occupied homes an EICR is generally recommended every 10 years, and when you buy a property. Rented homes in Wales need one at least every five years."),
    ("Is this checker a substitute for an inspection?",
     "No. It's a quick guide based on what you can see. Only testing by a qualified electrician can confirm the condition of your wiring."),
]
