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
      body = 'A burning smell, scorch marks, warm sockets or a tingle from a switch can mean a dangerous fault. Stop using the affected socket or appliance, switch off that circuit at the fuse box if it’s safe to do so, and get a qualified electrician to look at it as soon as possible. Call us on 07590 275205 – if we can’t get to you quickly, we’ll tell you straight away so you can get someone who can.';
      job = 'Fault finding / repair'; cta = 'Call 07590 275205';
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
    var href = r.urgent ? 'tel:07590275205' : (job === 'Rewire (full or partial)' ? '/rewire-quote-builder/' : '/get-a-quote/?job=' + encodeURIComponent(job) + '&details=' + encodeURIComponent(details));
    h += '<div class="flex flex-wrap gap-3"><a href="' + href + '" class="cta-button text-white px-7 py-3 rounded-lg font-bold">' + cta + ' <i class="fas fa-arrow-right ml-2" aria-hidden="true"></i></a>' +
      '<a href="tel:07590275205" class="px-6 py-3 rounded-lg font-bold border-2 border-slate-300 hover:border-amber-400"><i class="fas fa-phone mr-2" aria-hidden="true"></i>07590 275205</a>' +
      '<button type="button" id="rc-restart" class="px-5 py-3 rounded-lg font-semibold text-gray-600 hover:bg-slate-100">Start again</button></div>';
    P.innerHTML = h;
    P.querySelector('#rc-restart').onclick = function () { A = {}; i = 0; render(); };
  }
  render();
})();