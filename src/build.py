"""Generates the static site (HTML, sitemap, llms.txt) from src/content.py.

Run from the repo root:  npm run build   (or: python3 src/build.py && npx tailwindcss ...)
"""
import datetime
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa: E402,F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
BIZ_ID = SITE + "/#business"
ALL_AREAS = ["Cardiff"] + NEARBY_AREAS


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1) + "</script>"


def business_schema():
    return {
        "@type": "Electrician",
        "@id": BIZ_ID,
        "name": NAME,
        "url": SITE + "/",
        "logo": SITE + "/logo.svg",
        "image": [SITE + "/assets/og-image.jpg", SITE + "/work-3.jpeg", SITE + "/work-7.jpeg", SITE + "/work-1.jpeg"],
        "description": "Local, independent NICEIC registered electrician in Cardiff specialising in rewires, "
                       "consumer unit upgrades, extension and renovation electrics, lighting, EICRs and landlord "
                       "certificates. Works with homeowners, landlords, builders and other trades.",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Cardiff", "addressRegion": "Wales", "addressCountry": "GB"},
        "areaServed": [{"@type": "City", "name": a} if a not in ("Vale of Glamorgan",) else {"@type": "AdministrativeArea", "name": a} for a in ALL_AREAS],
        "knowsAbout": ["House rewiring", "Consumer unit replacement", "Electrical Installation Condition Reports",
                       "Landlord electrical safety certificates", "Extension and renovation electrics",
                       "Kitchen and bathroom electrics", "LED and outdoor lighting", "Fault finding", "BS 7671"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Electrical services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": strip_tags(s["h1"]), "url": f"{SITE}/{s['slug']}/"}} for s in SERVICES],
        },
        "sameAs": [FACEBOOK],
    }


def faq_schema(faq, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def faq_html(faq, heading="Frequently asked questions"):
    items = "\n".join(
        f'<details class="faq card rounded-xl p-5"><summary class="font-bold text-gray-900 cursor-pointer">{html.escape(q)}</summary>'
        f'<p class="text-gray-600 mt-3 leading-relaxed">{html.escape(a)}</p></details>' for q, a in faq)
    return f"""
    <section id="faq" class="py-20 bg-gray-50">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-10"><div class="accent-line mx-auto mb-6"></div>
            <h2 class="text-4xl font-bold text-gray-900">{heading}</h2></div>
            <div class="space-y-3">{items}</div>
        </div>
    </section>"""


NAV_LINKS = [("/#services", "Services"), ("/#work", "Our Work"), ("/builders-trades/", "Builders &amp; Trades"),
             ("/#areas", "Areas"), ("/#quote", "Contact")]


def nav():
    links = "\n".join(f'<a href="{h}" class="nav-link">{t}</a>' for h, t in NAV_LINKS)
    mob = "\n".join(f'<a href="{h}" class="block py-3 border-b border-slate-700 nav-link">{t}</a>' for h, t in NAV_LINKS)
    svc = "\n".join(f'<a href="/{s["slug"]}/" class="block py-3 border-b border-slate-700 nav-link">{s["short"]}</a>' for s in SERVICES if s["slug"] != "builders-trades")
    return f"""
    <a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 bg-white text-slate-900 px-4 py-2 rounded z-[60]">Skip to content</a>
    <nav class="site-nav text-white shadow-lg sticky top-0 z-50" aria-label="Main">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="/" aria-label="{NAME} home"><img src="/logo.svg" alt="{NAME}" width="150" height="50" class="h-11 w-auto"></a>
                <div class="hidden md:flex space-x-7 text-sm font-medium">{links}</div>
                <div class="flex items-center gap-3">
                    <a href="tel:{PHONE_TEL}" class="hidden lg:inline-flex items-center text-sm font-semibold text-amber-400 hover:text-amber-300"><i class="fas fa-phone mr-2" aria-hidden="true"></i>{PHONE_DISPLAY}</a>
                    <a href="/#quote" class="cta-button text-white px-5 py-2 rounded-lg font-semibold text-sm">Get a Quote</a>
                    <button id="menu-btn" class="md:hidden text-white text-2xl px-2" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><i class="fas fa-bars" aria-hidden="true"></i></button>
                </div>
            </div>
        </div>
        <div id="mobile-menu" class="hidden md:hidden bg-slate-900 px-4 pb-4 text-sm">{mob}
            <p class="pt-4 pb-1 text-amber-400 font-semibold uppercase text-xs tracking-wide">Services</p>{svc}
        </div>
    </nav>"""


def footer():
    svc = "\n".join(f'<li><a href="/{s["slug"]}/" class="hover:text-amber-400">{s["card_title"]}</a></li>' for s in SERVICES)
    return f"""
    <footer class="bg-slate-900 text-white py-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-8 pb-8 border-b border-slate-700">
                <div class="md:col-span-1">
                    <img src="/logo.svg" alt="{NAME}" width="150" height="50" class="h-12 w-auto mb-4" loading="lazy">
                    <p class="text-gray-400 leading-relaxed text-sm">Local, independent NICEIC registered electrician in Cardiff. Rewires, renovations, extensions, lighting and testing.</p>
                </div>
                <div>
                    <h2 class="font-bold text-amber-400 mb-4">Services</h2>
                    <ul class="space-y-2 text-gray-400 text-sm">{svc}</ul>
                </div>
                <div>
                    <h2 class="font-bold text-amber-400 mb-4">Areas</h2>
                    <p class="text-gray-400 text-sm leading-6">Cardiff, {", ".join(NEARBY_AREAS)}</p>
                </div>
                <div>
                    <h2 class="font-bold text-amber-400 mb-4">Contact</h2>
                    <ul class="space-y-2 text-gray-400 text-sm">
                        <li><a href="tel:{PHONE_TEL}" class="hover:text-amber-400"><i class="fas fa-phone mr-2" aria-hidden="true"></i>{PHONE_DISPLAY}</a></li>
                        <li><a href="mailto:{EMAIL}" class="hover:text-amber-400 break-all"><i class="fas fa-envelope mr-2" aria-hidden="true"></i>{EMAIL}</a></li>
                        <li><a href="{FACEBOOK}" target="_blank" rel="noopener" class="hover:text-amber-400"><i class="fab fa-facebook-f mr-2" aria-hidden="true"></i>Facebook</a></li>
                        <li><i class="fas fa-location-dot mr-2" aria-hidden="true"></i>Cardiff &amp; surrounding areas</li>
                    </ul>
                </div>
            </div>
            <div class="pt-8 text-center text-gray-400 text-sm">
                <p>&copy; <span id="year">{datetime.date.today().year}</span> {NAME}. NICEIC Registered. Fully insured.</p>
            </div>
        </div>
    </footer>
    <div class="md:hidden fixed bottom-0 inset-x-0 z-50 grid grid-cols-2 bg-slate-900 border-t border-slate-700">
        <a href="tel:{PHONE_TEL}" class="flex items-center justify-center gap-2 py-4 text-white font-bold"><i class="fas fa-phone text-amber-400" aria-hidden="true"></i>Call</a>
        <a href="/#quote" class="flex items-center justify-center gap-2 py-4 font-bold text-white bg-amber-600"><i class="fas fa-file-pen" aria-hidden="true"></i>Get a quote</a>
    </div>"""


SCRIPT = """
    <script>
        var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
        var mb = document.getElementById('menu-btn'), mm = document.getElementById('mobile-menu');
        if (mb) mb.addEventListener('click', function () { var o = mm.classList.toggle('hidden'); mb.setAttribute('aria-expanded', String(!o)); });
        if (mm) mm.addEventListener('click', function (e) { if (e.target.tagName === 'A') mm.classList.add('hidden'); });
        document.querySelectorAll('[data-customer]').forEach(function (a) {
            a.addEventListener('click', function () { var s = document.getElementById('q-customer'); if (s) s.value = a.dataset.customer; });
        });
        var f = document.getElementById('quote-form');
        if (f) f.addEventListener('submit', function (e) {
            e.preventDefault();
            var msg = document.getElementById('q-msg');
            var missing = Array.prototype.filter.call(f.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
            if (missing.length) { msg.textContent = 'Please fill in the fields marked *.'; msg.className = 'text-sm text-red-600'; missing[0].focus(); return; }
            var v = function (n) { return f.elements[n].value.trim(); };
            var subject = 'Quote request: ' + v('job') + ' - ' + v('postcode').toUpperCase();
            var body = ['Name: ' + v('name'), 'Phone: ' + v('phone'), 'I am a: ' + v('customer'), 'Type of work: ' + v('job'),
                'Postcode: ' + v('postcode').toUpperCase(), 'Timescale: ' + v('when'), '', 'About the job:', v('details')].join('\\n');
            window.location.href = 'mailto:EMAIL?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
            msg.textContent = 'Your email app should open now. If it doesn\\u2019t, call us on PHONE.'; msg.className = 'text-sm text-gray-600';
        });
    </script>""".replace("EMAIL", EMAIL).replace("PHONE", PHONE_DISPLAY)


def page(path, title, description, body, schema_graph, og_image="/assets/og-image.jpg", preload=None):
    url = SITE + path
    graph = {"@context": "https://schema.org", "@graph": schema_graph}
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{url}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="theme-color" content="#0f172a">
    <meta name="geo.region" content="GB-CRF">
    <meta name="geo.placename" content="Cardiff">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="en_GB">
    <meta property="og:site_name" content="{NAME}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{SITE}{og_image}">
    <link rel="icon" href="/logo.svg" type="image/svg+xml">
    <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM summary">
    {pre}
    <link rel="stylesheet" href="/assets/styles.css">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    {ld(graph)}
</head>
<body class="bg-gray-50 text-gray-800">
{nav()}
<main id="main">
{body}
</main>
{footer()}
{SCRIPT}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------
def quote_section(default_customer=None, default_job=None):
    def opts(values, default):
        return "".join(f'<option{" selected" if v == default else ""}>{html.escape(v)}</option>' for v in values)
    customers = ["Homeowner", "Landlord / letting agent", "Builder / trade", "Business"]
    jobs = ["Rewire (full or partial)", "Consumer unit upgrade", "Extension / renovation", "Kitchen or bathroom",
            "Lighting (indoor or outdoor)", "EICR / landlord certificate", "Fault finding / repair", "Other"]
    whens = ["Within a month", "1–3 months", "3+ months / planning stage", "Just getting prices"]
    return f"""
    <section id="quote" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid lg:grid-cols-5 gap-10">
                <div class="lg:col-span-2">
                    <div class="accent-line mb-6"></div>
                    <h2 class="text-4xl font-bold text-gray-900 mb-4">Request a quote</h2>
                    <p class="text-gray-600 leading-relaxed mb-8">Tell us about the job and where it is, and we&rsquo;ll get back to you. Photos help &mdash; you can attach them to the email this form creates.</p>
                    <div class="space-y-4">
                        <a href="tel:{PHONE_TEL}" class="flex items-center gap-4 card rounded-xl p-5">
                            <span class="bg-amber-100 w-12 h-12 rounded-lg flex items-center justify-center"><i class="fas fa-phone text-amber-600" aria-hidden="true"></i></span>
                            <span><span class="block text-sm text-gray-500">Call</span><span class="font-bold text-gray-900">{PHONE_DISPLAY}</span></span>
                        </a>
                        <a href="mailto:{EMAIL}" class="flex items-center gap-4 card rounded-xl p-5">
                            <span class="bg-amber-100 w-12 h-12 rounded-lg flex items-center justify-center"><i class="fas fa-envelope text-amber-600" aria-hidden="true"></i></span>
                            <span class="min-w-0"><span class="block text-sm text-gray-500">Email</span><span class="font-bold text-gray-900 break-all">{EMAIL}</span></span>
                        </a>
                        <a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-4 card rounded-xl p-5">
                            <span class="bg-amber-100 w-12 h-12 rounded-lg flex items-center justify-center"><i class="fab fa-facebook-f text-amber-600" aria-hidden="true"></i></span>
                            <span><span class="block text-sm text-gray-500">Facebook</span><span class="font-bold text-gray-900">{NAME}</span></span>
                        </a>
                    </div>
                </div>
                <form id="quote-form" class="lg:col-span-3 card rounded-xl p-6 md:p-8 grid sm:grid-cols-2 gap-5" novalidate>
                    <div><label for="q-name" class="block text-sm font-semibold mb-1">Name *</label><input id="q-name" name="name" class="field" required autocomplete="name"></div>
                    <div><label for="q-phone" class="block text-sm font-semibold mb-1">Phone *</label><input id="q-phone" name="phone" type="tel" class="field" required autocomplete="tel"></div>
                    <div><label for="q-customer" class="block text-sm font-semibold mb-1">I am a&hellip;</label><select id="q-customer" name="customer" class="field">{opts(customers, default_customer)}</select></div>
                    <div><label for="q-job" class="block text-sm font-semibold mb-1">Type of work</label><select id="q-job" name="job" class="field">{opts(jobs, default_job)}</select></div>
                    <div><label for="q-postcode" class="block text-sm font-semibold mb-1">Job postcode *</label><input id="q-postcode" name="postcode" class="field" required autocomplete="postal-code" placeholder="e.g. CF14"></div>
                    <div><label for="q-when" class="block text-sm font-semibold mb-1">When do you need it?</label><select id="q-when" name="when" class="field">{opts(whens, None)}</select></div>
                    <div class="sm:col-span-2"><label for="q-details" class="block text-sm font-semibold mb-1">About the job *</label>
                        <textarea id="q-details" name="details" rows="5" class="field" required placeholder="e.g. 3-bed semi, full rewire and new consumer unit. Kitchen being refitted in the spring."></textarea></div>
                    <div class="sm:col-span-2 flex flex-col sm:flex-row sm:items-center gap-4">
                        <button type="submit" class="cta-button text-white px-8 py-3 rounded-lg font-bold text-lg">Send enquiry</button>
                        <p id="q-msg" class="text-sm text-gray-500" role="status">This opens your email app with the details filled in.</p>
                    </div>
                </form>
            </div>
        </div>
    </section>"""


def areas_section():
    return f"""
    <section id="areas" class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid lg:grid-cols-3 gap-10">
                <div>
                    <div class="accent-line mb-6"></div>
                    <h2 class="text-4xl font-bold text-gray-900 mb-4">Areas we cover</h2>
                    <p class="text-gray-600 leading-relaxed">Based in Cardiff, covering the city and roughly 20 miles around it. For larger projects &mdash; rewires, extensions and renovations &mdash; we&rsquo;re happy to travel further.</p>
                </div>
                <div class="lg:col-span-2 grid sm:grid-cols-2 gap-6">
                    <div class="card rounded-xl p-6"><h3 class="font-bold text-gray-900 mb-3"><i class="fas fa-location-dot text-amber-500 mr-2" aria-hidden="true"></i>Electrician in Cardiff</h3>
                        <p class="text-gray-600 text-sm leading-7">{", ".join(CARDIFF_AREAS)}</p></div>
                    <div class="card rounded-xl p-6"><h3 class="font-bold text-gray-900 mb-3"><i class="fas fa-location-dot text-amber-500 mr-2" aria-hidden="true"></i>Surrounding areas</h3>
                        <p class="text-gray-600 text-sm leading-7">{", ".join(NEARBY_AREAS)}</p></div>
                </div>
            </div>
        </div>
    </section>"""


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------
def home():
    svc_cards = [s for s in SERVICES if s["slug"] in ("rewires-cardiff", "extensions-renovations-electrician-cardiff")]
    body = f"""
    <header class="hero-gradient text-white py-16 md:py-24">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <div class="accent-line mb-6"></div>
                    <p class="text-amber-400 font-semibold tracking-wide uppercase text-sm mb-3">NICEIC registered electrician in Cardiff</p>
                    <h1 class="text-4xl md:text-6xl font-bold mb-6 leading-tight">Rewires, renovations &amp; extensions &mdash; done properly.</h1>
                    <p class="text-lg text-gray-300 mb-8 leading-relaxed max-w-xl">{NAME} is a local, independent electrical business working with homeowners, landlords and builders across Cardiff. Clear written quotes, tidy work, and certification on every job.</p>
                    <div class="flex gap-4 flex-wrap mb-10">
                        <a href="#quote" class="cta-button text-white px-8 py-3 rounded-lg font-bold text-lg">Request a Quote</a>
                        <a href="tel:{PHONE_TEL}" class="border-2 border-amber-400 text-white px-8 py-3 rounded-lg font-bold hover:bg-amber-400 hover:text-slate-900 transition"><i class="fas fa-phone mr-2" aria-hidden="true"></i>{PHONE_DISPLAY}</a>
                    </div>
                    <ul class="grid grid-cols-2 gap-3 text-sm text-gray-200 max-w-md">
                        <li><i class="fas fa-circle-check text-amber-400 mr-2" aria-hidden="true"></i>NICEIC registered</li>
                        <li><i class="fas fa-circle-check text-amber-400 mr-2" aria-hidden="true"></i>Fully insured</li>
                        <li><i class="fas fa-circle-check text-amber-400 mr-2" aria-hidden="true"></i>Certified on completion</li>
                        <li><i class="fas fa-circle-check text-amber-400 mr-2" aria-hidden="true"></i>Trusted by local builders</li>
                    </ul>
                </div>
                <div class="hidden md:block">
                    <div class="photo rounded-xl shadow-2xl aspect-[4/3]"><img src="/work-3.jpeg" width="1200" height="1600" fetchpriority="high" alt="Kitchen extension in Cardiff with recessed downlights and under-cabinet LED lighting fitted by Bailey Electrical"></div>
                </div>
            </div>
        </div>
    </header>

    <section id="services" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-14"><div class="accent-line mx-auto mb-6"></div>
                <h2 class="text-4xl md:text-5xl font-bold text-gray-900">Electrical services in Cardiff</h2>
                <p class="text-gray-600 text-lg mt-4 max-w-2xl mx-auto">We specialise in jobs that need doing properly, from first fix to final certificate.</p></div>
            <div class="grid md:grid-cols-3 gap-8">
                <a href="/rewires-cardiff/" class="card p-8 rounded-xl block">
                    <div class="icon-tile w-14 h-14 rounded-lg flex items-center justify-center mb-5"><i class="fas fa-plug-circle-bolt text-white text-xl" aria-hidden="true"></i></div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">Rewires &amp; consumer units</h3>
                    <p class="text-gray-600 mb-5">Full and partial rewires planned around you, and consumer unit upgrades that bring older homes up to current regulations.</p>
                    <ul class="space-y-2 text-sm text-gray-700 mb-5">
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Full &amp; partial house rewires</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Fuse box &amp; consumer unit replacements</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>New circuits &amp; additional sockets</li>
                    </ul>
                    <span class="text-amber-600 font-semibold text-sm">About rewires <i class="fas fa-arrow-right ml-1" aria-hidden="true"></i></span>
                </a>
                <a href="/extensions-renovations-electrician-cardiff/" class="card p-8 rounded-xl block">
                    <div class="icon-tile w-14 h-14 rounded-lg flex items-center justify-center mb-5"><i class="fas fa-trowel-bricks text-white text-xl" aria-hidden="true"></i></div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">Extensions &amp; renovations</h3>
                    <p class="text-gray-600 mb-5">Complete electrics for kitchens, bathrooms, extensions and refurbishments &mdash; working directly for you or alongside your builder.</p>
                    <ul class="space-y-2 text-sm text-gray-700 mb-5">
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>First &amp; second fix</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Kitchens &amp; bathrooms</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Certification &amp; Building Regs notification</li>
                    </ul>
                    <span class="text-amber-600 font-semibold text-sm">About renovation electrics <i class="fas fa-arrow-right ml-1" aria-hidden="true"></i></span>
                </a>
                <a href="#work" class="card p-8 rounded-xl block">
                    <div class="icon-tile w-14 h-14 rounded-lg flex items-center justify-center mb-5"><i class="fas fa-lightbulb text-white text-xl" aria-hidden="true"></i></div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">Lighting, inside &amp; out</h3>
                    <p class="text-gray-600 mb-5">Lighting that makes a room &mdash; downlights, LED strip and feature lighting, plus garden and patio lighting.</p>
                    <ul class="space-y-2 text-sm text-gray-700 mb-5">
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Downlights &amp; LED upgrades</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Under-cabinet, plinth &amp; mirror lighting</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Garden, patio &amp; outdoor lighting</li>
                    </ul>
                    <span class="text-amber-600 font-semibold text-sm">See lighting projects <i class="fas fa-arrow-right ml-1" aria-hidden="true"></i></span>
                </a>
            </div>
            <div class="mt-10 rounded-xl bg-slate-50 border border-slate-200 p-6 md:p-8">
                <h3 class="font-bold text-gray-900 mb-4">Also available</h3>
                <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-3 text-sm text-gray-700">
                    <a href="/eicr-landlord-certificates-cardiff/" class="hover:text-amber-700"><i class="fas fa-clipboard-check text-amber-500 mr-2" aria-hidden="true"></i>EICRs &amp; electrical testing</a>
                    <a href="/eicr-landlord-certificates-cardiff/" class="hover:text-amber-700"><i class="fas fa-house-user text-amber-500 mr-2" aria-hidden="true"></i>Landlord electrical certificates</a>
                    <a href="/consumer-unit-upgrades-cardiff/" class="hover:text-amber-700"><i class="fas fa-bolt text-amber-500 mr-2" aria-hidden="true"></i>Consumer unit upgrades</a>
                    <p><i class="fas fa-magnifying-glass text-amber-500 mr-2" aria-hidden="true"></i>Fault finding &amp; repairs</p>
                </div>
            </div>
        </div>
    </section>

    <section id="who" class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-14"><div class="accent-line mx-auto mb-6"></div>
                <h2 class="text-4xl md:text-5xl font-bold text-gray-900">Who we work with</h2>
                <p class="text-gray-600 text-lg mt-4 max-w-2xl mx-auto">Most of our work comes from recommendations, repeat customers and the trades we work alongside.</p></div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="card rounded-xl p-6"><i class="fas fa-house text-amber-500 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-gray-900 mb-2">Homeowners</h3><p class="text-gray-600 text-sm">Especially if you&rsquo;re planning a renovation, extension, new kitchen or bathroom, or a rewire.</p></div>
                <a href="/builders-trades/" class="card rounded-xl p-6 block"><i class="fas fa-helmet-safety text-amber-500 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-gray-900 mb-2">Builders &amp; trades</h3><p class="text-gray-600 text-sm">A reliable electrician you can use job after job, fitting in with your programme.</p></a>
                <a href="/eicr-landlord-certificates-cardiff/" class="card rounded-xl p-6 block"><i class="fas fa-key text-amber-500 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-gray-900 mb-2">Landlords &amp; agents</h3><p class="text-gray-600 text-sm">EICRs, landlord certificates and remedial work, with ongoing testing when it&rsquo;s due.</p></a>
                <div class="card rounded-xl p-6"><i class="fas fa-store text-amber-500 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-gray-900 mb-2">Small local businesses</h3><p class="text-gray-600 text-sm">Shops, offices and small premises in and around Cardiff, by arrangement.</p></div>
            </div>
        </div>
    </section>

    <section id="work" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-14"><div class="accent-line mx-auto mb-6"></div>
                <h2 class="text-4xl md:text-5xl font-bold text-gray-900">Recent projects</h2>
                <p class="text-gray-600 text-lg mt-4">A few jobs we&rsquo;re proud of.</p></div>
            <div class="space-y-10">
                <article class="card rounded-xl overflow-hidden"><div class="grid md:grid-cols-5">
                    <div class="md:col-span-3 h-80 md:h-[26rem] grid grid-cols-3 grid-rows-2 gap-1">
                        <div class="photo col-span-2 row-span-2"><img src="/work-4.jpeg" width="1200" height="1600" alt="Kitchen island with downlights and under-cabinet LED lighting" loading="lazy"></div>
                        <div class="photo"><img src="/work-6.jpeg" width="1200" height="1600" alt="Open-plan kitchen-diner with recessed downlights" loading="lazy"></div>
                        <div class="photo"><img src="/work-3.jpeg" width="1200" height="1600" alt="Kitchen with under-cabinet LED strip lighting" loading="lazy"></div>
                    </div>
                    <div class="md:col-span-2 p-8 flex flex-col justify-center">
                        <p class="text-amber-600 font-semibold text-sm uppercase tracking-wide mb-2">Kitchen renovation</p>
                        <h3 class="text-2xl font-bold text-gray-900 mb-3">Open-plan kitchen-diner</h3>
                        <p class="text-gray-600">Full electrics for a new open-plan kitchen: recessed downlights, under-cabinet LED strip, and power for the island and appliances.</p>
                    </div></div></article>
                <article class="card rounded-xl overflow-hidden"><div class="grid md:grid-cols-5">
                    <div class="md:col-span-2 p-8 flex flex-col justify-center order-2 md:order-1">
                        <p class="text-amber-600 font-semibold text-sm uppercase tracking-wide mb-2">Bathroom renovation</p>
                        <h3 class="text-2xl font-bold text-gray-900 mb-3">Feature-lit bathroom</h3>
                        <p class="text-gray-600">Backlit LED mirror, recessed shower lighting, LED plinth lighting and a heated towel rail &mdash; all installed to bathroom zone regulations.</p>
                    </div>
                    <div class="md:col-span-3 h-80 md:h-[26rem] grid grid-cols-3 grid-rows-2 gap-1 order-1 md:order-2">
                        <div class="photo col-span-2 row-span-2"><img src="/work-7.jpeg" width="720" height="960" alt="Bathroom with backlit LED mirror, shower downlight and plinth lighting" loading="lazy"></div>
                        <div class="photo"><img src="/work-11.jpeg" width="1024" height="1365" alt="Backlit LED bathroom mirror" loading="lazy"></div>
                        <div class="photo"><img src="/work-10.jpeg" width="720" height="960" alt="Walk-in shower with recessed lighting and heated towel rail" loading="lazy"></div>
                    </div></div></article>
                <article class="card rounded-xl overflow-hidden"><div class="grid md:grid-cols-5">
                    <div class="md:col-span-3 grid grid-cols-2 gap-1">
                        <div class="photo h-56 md:h-72"><img src="/work-1.jpeg" width="1600" height="1200" alt="Patio with lit steps, wall lights and uplit trees at night" loading="lazy"></div>
                        <div class="photo h-56 md:h-72"><img src="/work-5.jpeg" width="1600" height="900" alt="Garden with spike lights and uplighting at night" loading="lazy"></div>
                    </div>
                    <div class="md:col-span-2 p-8 flex flex-col justify-center">
                        <p class="text-amber-600 font-semibold text-sm uppercase tracking-wide mb-2">Outdoor lighting</p>
                        <h3 class="text-2xl font-bold text-gray-900 mb-3">Garden &amp; patio lighting</h3>
                        <p class="text-gray-600">Step lights, fence and wall lighting, and tree uplighting to make the garden usable after dark.</p>
                    </div></div></article>
            </div>
        </div>
    </section>

    <section id="trade" class="hero-gradient text-white py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid lg:grid-cols-2 gap-12 items-center">
                <div>
                    <div class="accent-line mb-6"></div>
                    <p class="text-amber-400 font-semibold tracking-wide uppercase text-sm mb-3">For builders &amp; trades</p>
                    <h2 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">An electrician you can put on your jobs.</h2>
                    <p class="text-gray-300 text-lg leading-relaxed mb-8">We work with builders, kitchen and bathroom fitters, carpenters and other trades across Cardiff. We turn up when we say, work around your programme, and leave the paperwork sorted.</p>
                    <div class="flex flex-wrap gap-4">
                        <a href="#quote" data-customer="Builder / trade" class="cta-button inline-block text-white px-8 py-3 rounded-lg font-bold text-lg">Talk to us about your next job</a>
                        <a href="/builders-trades/" class="inline-block border-2 border-amber-400 text-white px-6 py-3 rounded-lg font-bold hover:bg-amber-400 hover:text-slate-900 transition">More for trades</a>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-5">
                    <div class="bg-white/5 border border-white/10 rounded-xl p-6"><i class="fas fa-calendar-check text-amber-400 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-lg mb-1">Reliable &amp; on time</h3><p class="text-gray-300 text-sm">First and second fix booked in around your schedule &mdash; no holding up the plasterer.</p></div>
                    <div class="bg-white/5 border border-white/10 rounded-xl p-6"><i class="fas fa-file-signature text-amber-400 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-lg mb-1">Certificates handled</h3><p class="text-gray-300 text-sm">Electrical installation certificates and Building Regs notification done for you.</p></div>
                    <div class="bg-white/5 border border-white/10 rounded-xl p-6"><i class="fas fa-people-group text-amber-400 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-lg mb-1">Easy to work with</h3><p class="text-gray-300 text-sm">Clear communication with you and your client, and a tidy site when we leave.</p></div>
                    <div class="bg-white/5 border border-white/10 rounded-xl p-6"><i class="fas fa-shield-halved text-amber-400 text-2xl mb-3" aria-hidden="true"></i><h3 class="font-bold text-lg mb-1">Registered &amp; insured</h3><p class="text-gray-300 text-sm">NICEIC registered with full public liability insurance.</p></div>
                </div>
            </div>
        </div>
    </section>

    <section id="about" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="photo rounded-xl shadow-lg aspect-[4/3]"><img src="/work-2.jpeg" width="1536" height="1024" alt="{NAME} – finished kitchen with downlights" loading="lazy"></div>
                <div>
                    <div class="accent-line mb-6"></div>
                    <h2 class="text-4xl font-bold text-gray-900 mb-6">How we work</h2>
                    <p class="text-gray-700 text-lg mb-8 leading-relaxed">{NAME} is a local, independent business. When you get in touch, you deal directly with the electrician doing the work &mdash; from the first visit to the final certificate. We take on fewer jobs and do them properly, rather than rushing from one to the next.</p>
                    <div class="space-y-4">
                        <div class="flex gap-4"><div class="bg-amber-100 rounded-lg w-12 h-12 flex items-center justify-center flex-shrink-0"><i class="fas fa-file-invoice text-amber-600" aria-hidden="true"></i></div><div><h3 class="font-bold text-gray-900">Clear written quotes</h3><p class="text-gray-600 text-sm">A proper scope of work and a fixed price before we start, so there are no surprises.</p></div></div>
                        <div class="flex gap-4"><div class="bg-amber-100 rounded-lg w-12 h-12 flex items-center justify-center flex-shrink-0"><i class="fas fa-broom text-amber-600" aria-hidden="true"></i></div><div><h3 class="font-bold text-gray-900">Respect for your home</h3><p class="text-gray-600 text-sm">Dust sheets down, mess cleared up, and work planned so you can keep living in the house.</p></div></div>
                        <div class="flex gap-4"><div class="bg-amber-100 rounded-lg w-12 h-12 flex items-center justify-center flex-shrink-0"><i class="fas fa-comments text-amber-600" aria-hidden="true"></i></div><div><h3 class="font-bold text-gray-900">Straight communication</h3><p class="text-gray-600 text-sm">You&rsquo;ll know when we&rsquo;re coming, what we&rsquo;re doing, and what it costs.</p></div></div>
                        <div class="flex gap-4"><div class="bg-amber-100 rounded-lg w-12 h-12 flex items-center justify-center flex-shrink-0"><i class="fas fa-certificate text-amber-600" aria-hidden="true"></i></div><div><h3 class="font-bold text-gray-900">Certified &amp; insured</h3><p class="text-gray-600 text-sm">NICEIC registered, fully insured, and every job certified on completion.</p></div></div>
                        <div class="flex gap-4"><div class="bg-amber-100 rounded-lg w-12 h-12 flex items-center justify-center flex-shrink-0"><i class="fas fa-calendar-days text-amber-600" aria-hidden="true"></i></div><div><h3 class="font-bold text-gray-900">Planned work, not rushed call-outs</h3><p class="text-gray-600 text-sm">We focus on planned projects rather than 24/7 emergencies, so we can turn up when we say and give each job the time it needs.</p></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="reviews" class="py-16 bg-gray-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="accent-line mx-auto mb-6"></div>
            <h2 class="text-4xl font-bold text-gray-900 mb-4">What our customers say</h2>
            <p class="text-gray-600 text-lg mb-8">Most of our work comes from recommendations. Read what customers have said about us on Google.</p>
            <!-- To feature real reviews, copy them word-for-word from Google with the reviewer's name as shown there. Never invent or edit reviews. -->
            <div class="flex flex-wrap justify-center gap-4">
                <a href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener noreferrer" class="cta-button text-white px-7 py-3 rounded-lg font-bold"><i class="fab fa-google mr-2" aria-hidden="true"></i>Read our Google reviews</a>
                <a href="{GOOGLE_WRITE_REVIEW}" target="_blank" rel="noopener noreferrer" class="border-2 border-amber-500 text-amber-700 px-7 py-3 rounded-lg font-bold hover:bg-amber-500 hover:text-white transition"><i class="fas fa-star mr-2" aria-hidden="true"></i>Leave a review</a>
            </div>
        </div>
    </section>
    {areas_section()}
    {faq_html(HOME_FAQ)}
    {quote_section()}
    """
    graph = [
        business_schema(),
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "inLanguage": "en-GB", "publisher": {"@id": BIZ_ID}},
        {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Electrician in Cardiff – Rewires, Renovations & Extensions",
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": BIZ_ID}, "dateModified": TODAY, "inLanguage": "en-GB"},
        faq_schema(HOME_FAQ, SITE + "/"),
    ]
    return page("/", "Electrician in Cardiff | Rewires, Renovations &amp; Extensions | Bailey Electrical",
                "NICEIC registered electrician in Cardiff. Rewires, consumer unit upgrades, extension and renovation electrics, lighting, EICRs and landlord certificates. Trusted by local builders. Call 07590 275205.",
                body, graph, preload="/work-3.jpeg")


# ---------------------------------------------------------------------------
# Service pages
# ---------------------------------------------------------------------------
def service_page(s):
    path = f"/{s['slug']}/"
    url = SITE + path
    sections = "\n".join(
        f'<section class="mb-12"><h2 class="text-3xl font-bold text-gray-900 mb-4">{h}</h2><div class="prose-body">{b}</div></section>'
        for h, b in s["sections"])
    others = "\n".join(
        f'<li><a href="/{o["slug"]}/" class="hover:text-amber-700"><i class="fas fa-angle-right text-amber-500 mr-2" aria-hidden="true"></i>{o["card_title"]}</a></li>'
        for o in SERVICES if o["slug"] != s["slug"])
    customer = "Builder / trade" if s["slug"] == "builders-trades" else ("Landlord / letting agent" if "eicr" in s["slug"] else None)
    job = {"rewires-cardiff": "Rewire (full or partial)", "consumer-unit-upgrades-cardiff": "Consumer unit upgrade",
           "extensions-renovations-electrician-cardiff": "Extension / renovation",
           "eicr-landlord-certificates-cardiff": "EICR / landlord certificate"}.get(s["slug"])
    body = f"""
    <header class="hero-gradient text-white py-14 md:py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-10 items-center">
            <div>
                <nav aria-label="Breadcrumb" class="text-sm text-gray-400 mb-6"><a href="/" class="hover:text-amber-400">Home</a> <span class="mx-2">/</span> <span class="text-gray-200">{s['short']}</span></nav>
                <p class="text-amber-400 font-semibold tracking-wide uppercase text-sm mb-3">{s['kicker']}</p>
                <h1 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">{s['h1']}</h1>
                <p class="text-lg text-gray-300 mb-8 leading-relaxed">{s['lead']}</p>
                <div class="flex gap-4 flex-wrap">
                    <a href="#quote" class="cta-button text-white px-8 py-3 rounded-lg font-bold text-lg">Request a Quote</a>
                    <a href="tel:{PHONE_TEL}" class="border-2 border-amber-400 text-white px-8 py-3 rounded-lg font-bold hover:bg-amber-400 hover:text-slate-900 transition"><i class="fas fa-phone mr-2" aria-hidden="true"></i>{PHONE_DISPLAY}</a>
                </div>
            </div>
            <div class="hidden md:block photo rounded-xl shadow-2xl aspect-[4/3]"><img src="/{s['image']}" alt="{s['image_alt']}" fetchpriority="high"></div>
        </div>
    </header>
    <div class="bg-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-3 gap-12">
            <article class="lg:col-span-2">{sections}</article>
            <aside class="space-y-6">
                <div class="card rounded-xl p-6">
                    <h2 class="font-bold text-gray-900 mb-3">Why {NAME}</h2>
                    <ul class="space-y-2 text-sm text-gray-700">
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>NICEIC registered &amp; fully insured</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Clear, fixed written quotes</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Tidy, respectful work</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Certified &amp; notified on completion</li>
                        <li><i class="fas fa-check text-amber-500 mr-2" aria-hidden="true"></i>Trusted by local builders</li>
                    </ul>
                    <a href="#quote" class="cta-button block text-center text-white px-6 py-3 rounded-lg font-bold mt-5">Get a quote</a>
                </div>
                <div class="card rounded-xl p-6">
                    <h2 class="font-bold text-gray-900 mb-3">Other services</h2>
                    <ul class="space-y-2 text-sm text-gray-700">{others}</ul>
                </div>
                <div class="card rounded-xl p-6">
                    <h2 class="font-bold text-gray-900 mb-3">Areas covered</h2>
                    <p class="text-sm text-gray-600 leading-6">Cardiff ({", ".join(CARDIFF_AREAS[:8])} and more), {", ".join(NEARBY_AREAS)}. Further for larger projects.</p>
                </div>
            </aside>
        </div>
    </div>
    {faq_html(s['faq'])}
    {quote_section(customer, job)}
    """
    graph = [
        {"@type": "Service", "@id": url + "#service", "name": strip_tags(s["h1"]), "serviceType": s["service_type"],
         "description": strip_tags(s["lead"]), "url": url, "provider": {"@id": BIZ_ID},
         "areaServed": [{"@type": "City", "name": a} for a in ALL_AREAS]},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": strip_tags(s["title"]), "about": {"@id": url + "#service"},
         "isPartOf": {"@id": SITE + "/#website"}, "dateModified": TODAY, "inLanguage": "en-GB"},
        crumbs_schema([("Home", "/"), (s["short"], path)]),
        faq_schema(s["faq"], url),
        {"@type": "Electrician", "@id": BIZ_ID, "name": NAME, "url": SITE + "/", "telephone": PHONE_INTL},
    ]
    return page(path, s["title"], s["description"], body, graph, preload="/" + s["image"])


def not_found():
    body = f"""
    <section class="py-24 bg-white text-center"><div class="max-w-xl mx-auto px-4">
        <h1 class="text-5xl font-bold text-gray-900 mb-4">Page not found</h1>
        <p class="text-gray-600 mb-8">Sorry, that page doesn&rsquo;t exist. You can go back to the home page or call us on {PHONE_DISPLAY}.</p>
        <a href="/" class="cta-button text-white px-8 py-3 rounded-lg font-bold">Go to the home page</a>
    </div></section>"""
    return page("/404.html", "Page not found | Bailey Electrical", "Page not found.", body, [business_schema()]).replace(
        'content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex"')


# ---------------------------------------------------------------------------
# llms.txt  – plain-English summary for AI assistants
# ---------------------------------------------------------------------------
def llms_txt():
    lines = [
        f"# {NAME}",
        "",
        f"> {NAME} is a local, independent, NICEIC registered electrician based in Cardiff, Wales. It specialises in "
        "house rewires, consumer unit (fuse box) upgrades, electrics for extensions, kitchens, bathrooms and renovations, "
        "and indoor and outdoor lighting. It also carries out EICRs and landlord electrical certificates. It works with "
        "homeowners, landlords and letting agents, builders and other trades, and small local businesses.",
        "",
        "## Key facts",
        f"- Business name: {NAME}",
        "- Type: Domestic electrician / electrical contractor",
        "- Registration: NICEIC registered; full public liability insurance",
        "- Based in: Cardiff, Wales, UK",
        f"- Areas covered: Cardiff ({', '.join(CARDIFF_AREAS)}) and roughly 20 miles around, including {', '.join(NEARBY_AREAS)}. Travels further for larger projects.",
        f"- Phone: {PHONE_DISPLAY} ({PHONE_INTL})",
        f"- Email: {EMAIL}",
        f"- Website: {SITE}/",
        f"- Facebook: {FACEBOOK}",
        "- Quotes: free, fixed written quotes with a clear scope of work",
        "- Best suited to: planned work such as rewires, renovations, extensions, consumer unit upgrades, lighting projects and landlord testing. Does not offer a 24/7 emergency service.",
        "- Works with builders: yes — first and second fix around the build programme, certification and Building Regulations notification handled",
        "",
        "## Services",
    ]
    for s in SERVICES:
        lines.append(f"- [{strip_tags(s['h1'])}]({SITE}/{s['slug']}/): {strip_tags(s['lead'])}")
    lines += ["- Lighting: downlights, LED upgrades, under-cabinet, plinth and mirror lighting, garden, patio and outdoor lighting",
              "- Also: fault finding and repairs, new circuits and additional sockets, small commercial work by arrangement", "",
              "## Frequently asked questions"]
    for q, a in HOME_FAQ:
        lines += [f"### {q}", a, ""]
    lines += ["## Contact", f"Call {PHONE_DISPLAY}, email {EMAIL}, or use the quote form at {SITE}/#quote", ""]
    return "\n".join(lines)


def sitemap():
    urls = ["/"] + [f"/{s['slug']}/" for s in SERVICES]
    items = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u == '/' else '0.8'}</priority></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("wrote", rel)


if __name__ == "__main__":
    write("index.html", home())
    for s in SERVICES:
        write(f"{s['slug']}/index.html", service_page(s))
    write("404.html", not_found())
    write("llms.txt", llms_txt())
    write("sitemap.xml", sitemap())
